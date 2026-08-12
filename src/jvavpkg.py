#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jvavpkg.py - JVAV 包管理器 (P1/P2)

一包一仓库，仓库文件直存，Git tag = 版本。
>100MB 资产不进仓库，通过 jvavpkg.links 外链下载（强制 SHA256 校验）。

命令:
  jvavpkg.py info <name|owner/repo> [--version <tag>]
  jvavpkg.py install <name> [--version <tag>] [--local]
  jvavpkg.py uninstall <name> [--local]
  jvavpkg.py list [--local]
  jvavpkg.py update [name] [--local]
  jvavpkg.py pack [src] [--name <n>] [--version <v>] [--main <f>] [--out <p>]

环境变量:
  GITHUB_TOKEN  可选，提升 GitHub API 限流（匿名 60/h -> 5000/h）

包仓库布局:
  <repo>/
    jvavpkg.json        清单
    jvavpkg.links       超 100MB 资产外链（# 文件名<TAB>SHA256<TAB>URL）
    dist/<name>-<ver>-win64.exe      program 二进制
    dist/<name>-<ver>-src.jvavpkg    library/plugin 源码包

安装位置:
  global: ~/.jvav/packages/<name>/
  local : <cwd>/.jvav/packages/<name>/
"""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Fix Windows console encoding (UTF-8 support)
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
MANIFEST_FILE = "jvavpkg.json"
LINKS_FILE = "jvavpkg.links"
PLATFORM = "win64"


class JVAVPkgError(Exception):
    """Package manager error."""


def _version_tuple(tag: str) -> tuple:
    """Convert a git tag like v1.2.3 into a sortable version tuple."""
    nums = re.findall(r"\d+", tag.lstrip("vV"))
    nums = nums[:3]
    while len(nums) < 3:
        nums.append("0")
    return tuple(int(x) for x in nums)


def _satisfies(version_tag: str, constraint: str) -> bool:
    """Check whether a version tag satisfies a semver-ish constraint.

    Supports comma-separated clauses: '>=1.0.0,<2.0.0'.
    Ops: >=, <=, ==/=/<>, >, <. Bare or * / latest / any -> unconstrained.
    """
    if not constraint or not constraint.strip():
        return True
    clauses = [c.strip() for c in constraint.split(",") if c.strip()]
    for clause in clauses:
        if clause in ("*", "latest", "any", ">=0.0.0"):
            continue
        m = re.match(r"^\s*(>=|<=|==|=|<>|>|<)?\s*([vV]?\d[\w.]*)\s*$", clause)
        if not m:
            continue  # unknown clause syntax: be permissive
        op = m.group(1) or "=="
        target = m.group(2)
        v = _version_tuple(version_tag)
        t = _version_tuple(target)
        if op == ">=":
            ok = v >= t
        elif op == "<=":
            ok = v <= t
        elif op == ">":
            ok = v > t
        elif op == "<":
            ok = v < t
        else:
            ok = v == t
        if not ok:
            return False
    return True


class GitHubClient:
    """Minimal GitHub REST API client (urllib only, no third-party deps)."""

    def __init__(self, token: Optional[str] = None) -> None:
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "jvavpkg",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def _request(self, url: str) -> bytes:
        req = urllib.request.Request(url, headers=self.headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise JVAVPkgError(f"404 Not Found: {url}")
            if e.code == 403:
                raise JVAVPkgError(
                    f"403 rate limited or forbidden: {url}. "
                    "Set GITHUB_TOKEN to raise the API limit."
                )
            raise JVAVPkgError(f"HTTP {e.code} for {url}: {e.reason}")

    def get_json(self, url: str) -> Any:
        return json.loads(self._request(url).decode("utf-8"))

    def get_tags(self, owner: str, repo: str) -> List[str]:
        """List all git tag names (paginated)."""
        tags: List[str] = []
        url: Optional[str] = f"{API_BASE}/repos/{owner}/{repo}/tags?per_page=100&page=1"
        while url:
            data = self.get_json(url)
            tags.extend(t["name"] for t in data)
            link = None
            # crude pagination via Link header is skipped; 100 tags is plenty for P1/P2
            url = None
        return tags

    def get_raw(self, owner: str, repo: str, ref: str, path: str) -> bytes:
        """Download a small repo file at a ref via raw.githubusercontent.com."""
        url = f"{RAW_BASE}/{owner}/{repo}/{ref}/{path}"
        return self._request(url)

    def get_url(self, url: str) -> bytes:
        """Download from an arbitrary URL (external links)."""
        return self._request(url)


class PackageManager:
    """JVAV package manager core."""

    def __init__(self, scope: str = "global", token: Optional[str] = None) -> None:
        self.scope = scope
        self.github = GitHubClient(token)
        if scope == "global":
            self.root = Path.home() / ".jvav"
        else:
            self.root = Path.cwd() / ".jvav"
        self.packages_dir = self.root / "packages"
        self.registry_path = self.root / "registry.json"
        self.lock_path = self.root / "jvavpkg.lock.json"
        self.packages_dir.mkdir(parents=True, exist_ok=True)

    # ---------- local state ----------

    def _load_json(self, path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return default

    def _save_json(self, path: Path, data: Any) -> None:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_registry(self) -> Dict[str, str]:
        return self._load_json(self.registry_path, {})

    def save_registry(self, registry: Dict[str, str]) -> None:
        self._save_json(self.registry_path, registry)

    def load_lock(self) -> Dict[str, Any]:
        return self._load_json(self.lock_path, {})

    def save_lock(self, lock: Dict[str, Any]) -> None:
        self._save_json(self.lock_path, lock)

    # ---------- resolution ----------

    def resolve_repo(self, name: str) -> str:
        """Resolve a short name to owner/repo via registry; owner/repo passes through."""
        if "/" in name:
            return name
        registry = self.load_registry()
        if name in registry:
            return registry[name]
        raise JVAVPkgError(
            f"Unknown package '{name}'. Use 'owner/repo' or install once to register it."
        )

    def pick_version(self, owner: str, repo: str, version: str = "latest") -> str:
        """Resolve a version string to a git tag ref."""
        tags = self.github.get_tags(owner, repo)
        if not tags:
            raise JVAVPkgError(f"No git tags found in {owner}/{repo}")
        if version and version.lower() != "latest":
            if version not in tags:
                raise JVAVPkgError(
                    f"Version '{version}' not found in {owner}/{repo}. "
                    f"Available: {', '.join(sorted(tags, key=_version_tuple))}"
                )
            return version
        return max(tags, key=_version_tuple)

    # ---------- remote manifest / links ----------

    def load_manifest(self, owner: str, repo: str, ref: str) -> Dict[str, Any]:
        try:
            data = self.github.get_raw(owner, repo, ref, MANIFEST_FILE)
            return json.loads(data.decode("utf-8"))
        except JVAVPkgError:
            raise JVAVPkgError(
                f"Manifest '{MANIFEST_FILE}' not found in {owner}/{repo}@{ref}"
            )

    def fetch_dependency_repo(self, dep: str, via: str) -> str:
        """Resolve a dependency key (short name or owner/repo) to owner/repo.

        `via` is the parent package name used in error messages.
        """
        if "/" in dep:
            return dep
        registry = self.load_registry()
        if dep in registry:
            return registry[dep]
        raise JVAVPkgError(
            f"Dependency '{dep}' (required by '{via}') is unknown. "
            "Install 'owner/repo' once to register it, or declare it as 'owner/repo'."
        )

    def pick_version_satisfying(self, owner: str, repo: str, constraint: str, via: str) -> str:
        """Pick the highest tag satisfying a constraint; latest for unconstrained."""
        tags = self.github.get_tags(owner, repo)
        if not tags:
            raise JVAVPkgError(f"No git tags found in {owner}/{repo}")
        if not constraint or constraint.strip() in ("*", "latest", "any", ">=0.0.0"):
            return max(tags, key=_version_tuple)
        candidates = [t for t in tags if _satisfies(t, constraint)]
        if not candidates:
            raise JVAVPkgError(
                f"No version of '{repo}' satisfies '{constraint}' "
                f"(required by '{via}'). Tags: {', '.join(sorted(tags, key=_version_tuple))}"
            )
        return max(candidates, key=_version_tuple)

    def resolve_dependencies(
        self, owner: str, repo: str, ref: str, constraint: str
    ) -> Dict[str, Dict[str, Any]]:
        """BFS dependency resolution with cycle & conflict detection.

        Returns {package_name: {"repo":..., "ref":..., "constraint":..., "manifest":...}}
        including the root package itself.
        """
        resolved: Dict[str, Dict[str, Any]] = {}
        visited: Dict[str, str] = {}  # package_name -> ref (conflict detection)
        queue: List[tuple] = [(owner, repo, ref, constraint, None)]  # ...parent for cycle msg
        seen_edges: set = set()

        # Cycle detection via BFS parent chain (state while expanding)
        visiting: List[str] = []

        def _expand(o: str, r: str, version_ref: str, cons: str, parent: Optional[str]) -> None:
            manifest = self.load_manifest(o, r, version_ref)
            name = manifest.get("name", r)

            if name in visiting:
                chain = " -> ".join(visiting[visiting.index(name):] + [name])
                raise JVAVPkgError(f"Circular dependency detected: {chain}")

            if name in visited:
                prev_ref = visited[name]
                if not _satisfies(prev_ref, cons):
                    raise JVAVPkgError(
                        f"Version conflict for '{name}': already {prev_ref} "
                        f"but '{cons}' required (by '{parent}')"
                    )
                # already resolved at a compatible version
                if name not in resolved:
                    resolved[name] = {
                        "repo": f"{o}/{r}",
                        "ref": prev_ref,
                        "constraint": cons,
                        "manifest": manifest,
                    }
                return

            visiting.append(name)
            visited[name] = version_ref
            resolved[name] = {
                "repo": f"{o}/{r}",
                "ref": version_ref,
                "constraint": cons,
                "manifest": manifest,
            }

            # Conflict vs already-installed packages (separate from this graph)
            if parent is not None:
                lock = self.load_lock()
                if name in lock:
                    installed_ref = lock[name]["version"]
                    if not _satisfies(installed_ref, cons):
                        raise JVAVPkgError(
                            f"Version conflict for '{name}': installed {installed_ref} "
                            f"does not satisfy '{cons}' (required by '{parent}')"
                        )

            for dep, dep_cons in (manifest.get("dependencies", {}) or {}).items():
                dep_repo = self.fetch_dependency_repo(dep, via=name)
                dep_owner, dep_name = dep_repo.split("/", 1)
                dep_ref = self.pick_version_satisfying(dep_owner, dep_name, dep_cons, via=name)
                _expand(dep_owner, dep_name, dep_ref, dep_cons, parent=name)

            visiting.pop()

        _expand(owner, repo, ref, constraint, parent=None)
        return resolved

    def load_links(self, owner: str, repo: str, ref: str) -> Dict[str, Dict[str, str]]:
        """Parse jvavpkg.links into {filename: {sha256, url}}."""
        try:
            data = self.github.get_raw(owner, repo, ref, LINKS_FILE).decode("utf-8")
        except JVAVPkgError:
            return {}
        links: Dict[str, Dict[str, str]] = {}
        for line in data.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 3:
                links[parts[0]] = {"sha256": parts[1].lower(), "url": parts[2]}
        return links

    # ---------- commands ----------

    def cmd_info(self, name: str, version: str = "latest") -> None:
        repo = self.resolve_repo(name)
        owner, repo_name = repo.split("/", 1)
        ref = self.pick_version(owner, repo_name, version)
        manifest = self.load_manifest(owner, repo_name, ref)
        links = self.load_links(owner, repo_name, ref)

        print(f"name        : {manifest.get('name', repo_name)}")
        print(f"repo        : {owner}/{repo_name}")
        print(f"version     : {ref}")
        print(f"type        : {manifest.get('type', 'library')}")
        print(f"description : {manifest.get('description', '-')}")
        print(f"author      : {manifest.get('author', '-')}")
        print(f"license     : {manifest.get('license', '-')}")
        deps = manifest.get("dependencies", {}) or {}
        print(f"dependencies: {', '.join(f'{k}{v}' for k, v in deps.items()) or 'none'}")
        for platform, assets in manifest.get("assets", {}).items():
            for kind, rel_path in assets.items():
                marker = " [external]" if Path(rel_path).name in links else ""
                print(f"asset       : {platform}/{kind} -> {rel_path}{marker}")

    def cmd_list(self) -> None:
        lock = self.load_lock()
        if not lock:
            print("No packages installed.")
            return
        for pkg_name in sorted(lock):
            info = lock[pkg_name]
            print(f"{pkg_name}  {info.get('version', '?')}  ({info.get('type', '?')})  from {info.get('repo', '?')}")

    def cmd_install(self, name: str, version: str = "latest") -> None:
        repo = self.resolve_repo(name)
        owner, repo_name = repo.split("/", 1)
        print(f"[install] resolving {repo} ...")
        if version and version.lower() != "latest" and version not in self.github.get_tags(owner, repo_name):
            raise JVAVPkgError(f"Version '{version}' not found in {owner}/{repo_name}")
        constraint = "latest" if (not version or version.lower() == "latest") else version
        ref = self.pick_version(owner, repo_name, version)

        graph = self.resolve_dependencies(owner, repo_name, ref, constraint)
        root_pkg = graph[next(iter(graph))]
        root_key = root_pkg["manifest"].get("name", repo_name)

        # install dependencies first (deterministic order), then root
        for pkg_name in sorted(graph):
            info = graph[pkg_name]
            if pkg_name == root_key and info["repo"] == repo:
                continue
            print(f"[install] dependency: {pkg_name}")
            self._install_one(pkg_name, info["repo"], info["ref"], info["constraint"], info["manifest"])
        self._install_one(root_key, repo, ref, constraint, root_pkg["manifest"])

    def cmd_update(self, name: Optional[str] = None) -> None:
        """Update installed packages to the latest compatible version."""
        lock = self.load_lock()
        targets = [name] if name else list(lock.keys())
        if not targets:
            print("Nothing to update.")
            return
        for pkg_name in targets:
            if pkg_name not in lock:
                raise JVAVPkgError(f"'{pkg_name}' is not installed")
            info = lock[pkg_name]
            repo = info["repo"]
            owner, repo_name = repo.split("/", 1)
            constraint = info.get("constraint", "latest")
            new_ref = self.pick_version_satisfying(owner, repo_name, constraint, via=pkg_name)
            if new_ref == info["version"]:
                print(f"[update] {pkg_name} already at {new_ref}")
                continue
            print(f"[update] {pkg_name}: {info['version']} -> {new_ref}")
            manifest = self.load_manifest(owner, repo_name, new_ref)
            # re-resolve deps in case they changed
            graph = self.resolve_dependencies(owner, repo_name, new_ref, constraint)
            for dep_name in sorted(graph):
                dep = graph[dep_name]
                if dep_name == pkg_name and dep["repo"] == repo:
                    continue
                self._install_one(dep_name, dep["repo"], dep["ref"], dep["constraint"], dep["manifest"])
            self._install_one(pkg_name, repo, new_ref, constraint, manifest)

    def _install_one(
        self,
        pkg_name: str,
        repo: str,
        ref: str,
        constraint: str,
        manifest: Dict[str, Any],
    ) -> None:
        """Download, verify, extract and register a single package."""
        owner, repo_name = repo.split("/", 1)
        pkg_type = manifest.get("type", "library")
        if pkg_type not in ("program", "library", "plugin"):
            raise JVAVPkgError(f"Invalid type '{pkg_type}' in manifest of {pkg_name}")

        assets = manifest.get("assets", {}).get(PLATFORM, {})
        asset_rel = assets.get("program") if pkg_type == "program" else assets.get("source")
        if not asset_rel:
            raise JVAVPkgError(
                f"No '{'program' if pkg_type == 'program' else 'source'}' asset "
                f"for platform '{PLATFORM}' in {pkg_name}@{ref}"
            )
        basename = Path(asset_rel).name
        links = self.load_links(owner, repo_name, ref)

        print(f"[install] {pkg_name}@{ref} (type={pkg_type})")
        print(f"[install] downloading {basename} ...")
        if basename in links:
            entry = links[basename]
            print(f"[install] external link -> {entry['url']}")
            data = self.github.get_url(entry["url"])
            actual = hashlib.sha256(data).hexdigest()
            expected = entry["sha256"]
            if actual != expected:
                raise JVAVPkgError(
                    f"SHA256 mismatch for {basename}: got {actual}, expected {expected}"
                )
            print(f"[install] SHA256 verified: {actual}")
        else:
            data = self.github.get_raw(owner, repo_name, ref, asset_rel)

        dest = self.packages_dir / pkg_name
        dest.mkdir(parents=True, exist_ok=True)
        self._install_asset(dest, pkg_type, basename, data)
        self._save_json(dest / "manifest.json", manifest)

        registry = self.load_registry()
        registry[pkg_name] = repo
        self.save_registry(registry)

        lock = self.load_lock()
        lock[pkg_name] = {
            "repo": repo,
            "version": ref,
            "constraint": constraint,
            "type": pkg_type,
            "scope": self.scope,
            "installed_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.save_lock(lock)
        print(f"[install] done: {dest}")

    def cmd_uninstall(self, name: str) -> None:
        lock = self.load_lock()
        if name not in lock:
            raise JVAVPkgError(f"'{name}' is not installed")
        dest = self.packages_dir / name
        if dest.exists():
            shutil.rmtree(dest)
        del lock[name]
        self.save_lock(lock)
        print(f"[uninstall] removed {name}")

    def _install_asset(self, dest: Path, pkg_type: str, basename: str, data: bytes) -> None:
        """Place downloaded bytes according to package type."""
        if pkg_type == "program":
            bin_dir = dest / "bin"
            bin_dir.mkdir(parents=True, exist_ok=True)
            (bin_dir / basename).write_bytes(data)
            return

        # library / plugin -> extract .jvavpkg source, or copy raw file
        src_dir = dest / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        if basename.endswith(".jvavpkg"):
            try:
                pkg = json.loads(data.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pkg = None
            if isinstance(pkg, dict) and isinstance(pkg.get("files"), dict):
                for fname, content in pkg["files"].items():
                    fpath = src_dir / fname
                    fpath.parent.mkdir(parents=True, exist_ok=True)
                    fpath.write_text(content, encoding="utf-8")
                return
        (src_dir / basename).write_bytes(data)

    def cmd_pack(
        self,
        src: str = ".",
        name: Optional[str] = None,
        version: str = "1.0.0",
        main: Optional[str] = None,
        out: Optional[str] = None,
    ) -> None:
        """Package local *.jvav files into a standard .jvavpkg source package."""
        src_dir = Path(src)
        if not src_dir.is_dir():
            raise JVAVPkgError(f"Source directory not found: {src}")

        jvav_files = sorted(
            p for p in src_dir.iterdir()
            if p.is_file() and p.suffix == ".jvav"
        )
        if not jvav_files:
            raise JVAVPkgError(f"No .jvav files found in {src}")

        pkg_name = name or src_dir.name
        pkg_version = version if version.startswith("v") else f"v{version}"

        # pick main file: explicit, main.jvav, or first .jvav
        if main:
            main_file = main
            if not (src_dir / main_file).exists():
                raise JVAVPkgError(f"Main file not found: {main_file}")
        elif (src_dir / "main.jvav").exists():
            main_file = "main.jvav"
        else:
            main_file = jvav_files[0].name

        files: Dict[str, str] = {}
        for f in jvav_files:
            files[f.name] = f.read_text(encoding="utf-8")

        package = {
            "name": pkg_name,
            "version": pkg_version.lstrip("v"),
            "jvav_version": "DK27",
            "main": main_file,
            "files": files,
            "build_info": {
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "builder": "jvavpkg",
                "platform": "windows-x64",
            },
        }

        out_path = out or str(src_dir / "dist" / f"{pkg_name}-{pkg_version.lstrip('v')}-src.jvavpkg")
        out_dir = Path(out_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(
            json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        print(f"[pack] packaged {pkg_name}@{pkg_version}")
        print(f"[pack] files: {', '.join(files.keys())}")
        print(f"[pack] main : {main_file}")
        print(f"[pack] output: {out_path}")
        print(f"[pack] manifest hint (add to jvavpkg.json assets.win64.source):")
        print(f"        dist/{Path(out_path).name}")


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--version", default="latest", help="git tag / version (default: latest)")
    parser.add_argument("--local", action="store_true", help="install into current project (.jvav/)")
    parser.add_argument("--token", default=None, help="GitHub token (or set GITHUB_TOKEN)")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="JVAV package manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="show package info")
    p_info.add_argument("name", help="package short name or owner/repo")
    _add_common(p_info)

    p_list = sub.add_parser("list", help="list installed packages")
    p_list.add_argument("--local", action="store_true", help="show project-local packages")

    p_install = sub.add_parser("install", help="install a package")
    p_install.add_argument("name", help="package short name or owner/repo")
    _add_common(p_install)

    p_uninstall = sub.add_parser("uninstall", help="remove an installed package")
    p_uninstall.add_argument("name", help="installed package name")
    p_uninstall.add_argument("--local", action="store_true", help="uninstall from project-local scope")

    p_update = sub.add_parser("update", help="update installed packages to latest compatible")
    p_update.add_argument("name", nargs="?", default=None, help="package name (default: all)")
    p_update.add_argument("--local", action="store_true", help="update project-local packages")

    p_pack = sub.add_parser("pack", help="package local .jvav files into a .jvavpkg")
    p_pack.add_argument("src", nargs="?", default=".", help="source directory containing .jvav files")
    p_pack.add_argument("--name", default=None, help="package name (default: dir name)")
    p_pack.add_argument("--version", default="1.0.0", help="package version (default: 1.0.0)")
    p_pack.add_argument("--main", default=None, help="main file name (default: main.jvav or first .jvav)")
    p_pack.add_argument("--out", default=None, help="output path (default: dist/<name>-<ver>-src.jvavpkg)")

    args = parser.parse_args(argv)
    token = getattr(args, "token", None) or os.environ.get("GITHUB_TOKEN")
    scope = "local" if getattr(args, "local", False) else "global"
    pm = PackageManager(scope=scope, token=token)

    try:
        if args.command == "info":
            pm.cmd_info(args.name, args.version)
        elif args.command == "list":
            pm.cmd_list()
        elif args.command == "install":
            pm.cmd_install(args.name, args.version)
        elif args.command == "uninstall":
            pm.cmd_uninstall(args.name)
        elif args.command == "update":
            pm.cmd_update(args.name)
        elif args.command == "pack":
            pm.cmd_pack(args.src, name=args.name, version=args.version,
                        main=args.main, out=args.out)
        return 0
    except JVAVPkgError as e:
        print(f"[error] {e}")
        return 1
    except urllib.error.URLError as e:
        print(f"[error] network failure: {e.reason}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
