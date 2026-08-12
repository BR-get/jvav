"""Self-test suite for the JVAV package manager (P1-P4).

Run: python tests/test_jvavpkg.py
Uses a fake GitHub client serving from an in-memory repo tree, so no network needed.
"""

import sys
import os
import json
import tempfile
import shutil
import hashlib
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import jvavpkg
from jvavpkg import PackageManager, JVAVPkgError, _version_tuple, _satisfies


# ---------------------------------------------------------------------------
# Fake GitHub client serving from an in-memory dict {tag: {path: bytes}}
# ---------------------------------------------------------------------------

def make_source_pkg(name, files, type="plugin", deps=None, version="1.0.0"):
    """Build a .jvavpkg source package bytes."""
    pkg = {
        "name": name,
        "version": version,
        "jvav_version": "DK27",
        "main": list(files)[0] if files else "main.jvav",
        "files": files,
        "build_info": {"timestamp": "2026-08-10T00:00:00Z", "builder": "jvavpkg", "platform": "windows-x64"},
    }
    return json.dumps(pkg, ensure_ascii=False).encode("utf-8")


def make_manifest(name, type="plugin", deps=None, source_path=None):
    m = {
        "name": name,
        "type": type,
        "description": name,
        "version": "1.0.0",
        "dependencies": deps or {},
        "assets": {"win64": {"source": source_path or f"dist/{name}-src.jvavpkg"}},
    }
    return json.dumps(m, ensure_ascii=False).encode("utf-8")


class FakeRepo:
    """A single package repo: tags -> {path: bytes}."""

    def __init__(self, name, owner="BR-get"):
        self.owner = owner
        self.name = name
        self.tags = {}  # tag -> {path: bytes}
        self.registry = {}  # dep short name -> owner/repo (for fetch_dependency_repo)

    def add(self, tag, files_by_path):
        self.tags[tag] = files_by_path

    def add_standard(self, tag, pkg_name, files, type="plugin", deps=None, version="1.0.0"):
        src_path = f"dist/{pkg_name}-{version}-src.jvavpkg"
        self.add(tag, {
            "jvavpkg.json": make_manifest(pkg_name, type=type, deps=deps, source_path=src_path),
            src_path: make_source_pkg(pkg_name, files, type=type, deps=deps, version=version),
        })
        self.registry.setdefault(pkg_name, f"{self.owner}/{self.name}")


class FakeGitHub:
    def __init__(self, repos):
        self.repos = repos  # {name: FakeRepo}

    def _repo(self, owner, name):
        for r in self.repos.values():
            if r.owner == owner and r.name == name:
                return r
        raise JVAVPkgError(f"repo {owner}/{name} not found")

    def get_tags(self, owner, repo):
        return sorted(self._repo(owner, repo).tags.keys(), key=_version_tuple)

    def get_raw(self, owner, repo, ref, path):
        repo_obj = self._repo(owner, repo)
        tag = repo_obj.tags.get(ref)
        if not tag or path not in tag:
            raise JVAVPkgError(f"404 Not Found: {owner}/{repo}@{ref}/{path}")
        return tag[path]

    def get_url(self, url):
        raise JVAVPkgError(f"unexpected external URL in test: {url}")


# ---------------------------------------------------------------------------
# Helper to build an isolated PackageManager
# ---------------------------------------------------------------------------

class TestPM(PackageManager):
    def __init__(self, github, scope="global"):
        self.scope = scope
        self.github = github
        tmp = tempfile.mkdtemp()
        self._tmp = tmp
        from pathlib import Path
        self.root = Path(tmp) / ".jvav"
        self.packages_dir = self.root / "packages"
        self.registry_path = self.root / "registry.json"
        self.lock_path = self.root / "jvavpkg.lock.json"
        self.packages_dir.mkdir(parents=True, exist_ok=True)

    def cleanup(self):
        shutil.rmtree(self._tmp, ignore_errors=True)


def make_two_sum_repo():
    r = FakeRepo("two_sum")
    files = {"two_sum.jvav": "tnirp('two_sum')\n"}
    r.add_standard("v1.0.0", "two_sum", files)
    return r


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_version_tuple_and_satisfies():
    assert _version_tuple("v1.2.3") == (1, 2, 3)
    assert _version_tuple("1.10.0") > _version_tuple("1.9.9")
    assert _version_tuple("v2") == (2, 0, 0)
    assert _satisfies("v1.2.0", ">=1.0.0")
    assert not _satisfies("v0.9.0", ">=1.0.0")
    assert _satisfies("v1.2.0", "<2.0.0")
    assert _satisfies("v1.2.3", "==1.2.3")
    assert _satisfies("v9.9.9", "*")
    assert _satisfies("v1.2.3", "")


def test_basic_install_uninstall_list():
    gh = FakeGitHub({"two_sum": make_two_sum_repo()})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/two_sum")
    lock = pm.load_lock()
    assert "two_sum" in lock
    assert lock["two_sum"]["version"] == "v1.0.0"
    assert lock["two_sum"]["constraint"] == "latest"
    src = os.path.join(pm.packages_dir, "two_sum", "src", "two_sum.jvav")
    assert os.path.exists(src), "source file extracted"
    # short-name resolution via registry
    assert pm.load_registry()["two_sum"] == "BR-get/two_sum"
    # list
    pm.cmd_list()
    # uninstall
    pm.cmd_uninstall("two_sum")
    assert "two_sum" not in pm.load_lock()
    pm.cleanup()


def test_install_with_version_constraint():
    r = make_two_sum_repo()
    r.add_standard("v1.1.0", "two_sum", {"two_sum.jvav": "tnirp('v2')\n"}, version="1.1.0")
    gh = FakeGitHub({"two_sum": r})
    pm = TestPM(gh)
    pm2 = TestPM(gh)
    pm2.cmd_install("BR-get/two_sum", "v1.0.0")
    assert pm2.load_lock()["two_sum"]["version"] == "v1.0.0"
    assert pm2.load_lock()["two_sum"]["constraint"] == "v1.0.0"
    pm.cleanup()
    pm2.cleanup()


def test_dependency_install():
    lib = FakeRepo("jvav-utils")
    lib.add_standard("v1.0.0", "jvav-utils", {"utils.jvav": "def util(): return 1\n"})
    app = FakeRepo("app")
    app.add_standard("v1.0.0", "app", {"main.jvav": "tnirp('app')\n"},
                     deps={"BR-get/jvav-utils": ">=1.0.0"})
    gh = FakeGitHub({"jvav-utils": lib, "app": app})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/app")
    lock = pm.load_lock()
    assert "app" in lock
    assert "jvav-utils" in lock, "dependency auto-installed"
    assert lock["jvav-utils"]["version"] == "v1.0.0"
    utils_src = os.path.join(pm.packages_dir, "jvav-utils", "src", "utils.jvav")
    assert os.path.exists(utils_src)
    pm.cleanup()


def test_dependency_constraint_selects_version():
    lib = FakeRepo("jvav-utils")
    lib.add_standard("v1.0.0", "jvav-utils", {"u.jvav": "v1"})
    lib.add_standard("v2.0.0", "jvav-utils", {"u.jvav": "v2"}, version="2.0.0")
    lib.add_standard("v3.0.0", "jvav-utils", {"u.jvav": "v3"}, version="3.0.0")
    app = FakeRepo("app")
    app.add_standard("v1.0.0", "app", {"main.jvav": "x\n"},
                     deps={"BR-get/jvav-utils": ">=2.0.0,<3.0.0"})
    gh = FakeGitHub({"jvav-utils": lib, "app": app})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/app")
    lock = pm.load_lock()
    assert lock["jvav-utils"]["version"] == "v2.0.0", lock["jvav-utils"]["version"]
    pm.cleanup()


def test_dependency_conflict():
    a = FakeRepo("dep-a")
    a.add_standard("v1.0.0", "dep-a", {"a.jvav": "a"})
    a.add_standard("v2.0.0", "dep-a", {"a.jvav": "a2"}, version="2.0.0")
    root = FakeRepo("root")
    root.add_standard("v1.0.0", "root", {"m.jvav": "m"},
                      deps={"BR-get/dep-a": ">=1.0.0,<2.0.0"})
    other = FakeRepo("other")
    other.add_standard("v1.0.0", "other", {"o.jvav": "o"},
                       deps={"BR-get/dep-a": ">=2.0.0"})
    # root -> dep-a<2 ; other -> dep-a>=2 ; install root, then other
    gh = FakeGitHub({"dep-a": a, "root": root, "other": other})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/root")
    # installing 'other' needs dep-a>=2, but dep-a is pinned to 1.x -> conflict
    try:
        pm.cmd_install("BR-get/other")
        raise AssertionError("expected version conflict error")
    except JVAVPkgError as e:
        assert "conflict" in str(e).lower(), str(e)
    pm.cleanup()


def test_circular_dependency():
    a = FakeRepo("cyc-a")
    a.add_standard("v1.0.0", "cyc-a", {"a.jvav": "a"}, deps={"BR-get/cyc-b": "*"})
    b = FakeRepo("cyc-b")
    b.add_standard("v1.0.0", "cyc-b", {"b.jvav": "b"}, deps={"BR-get/cyc-a": "*"})
    gh = FakeGitHub({"cyc-a": a, "cyc-b": b})
    pm = TestPM(gh)
    try:
        pm.cmd_install("BR-get/cyc-a")
        raise AssertionError("expected circular dependency error")
    except JVAVPkgError as e:
        assert "circular" in str(e).lower(), str(e)
    pm.cleanup()


def test_update():
    r = FakeRepo("two_sum")
    r.add_standard("v1.0.0", "two_sum", {"two_sum.jvav": "tnirp('v1')\n"})
    gh = FakeGitHub({"two_sum": r})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/two_sum")
    assert pm.load_lock()["two_sum"]["version"] == "v1.0.0"
    # a new version is released
    r.add_standard("v1.1.0", "two_sum", {"two_sum.jvav": "tnirp('v2')\n"}, version="1.1.0")
    pm.cmd_update()
    assert pm.load_lock()["two_sum"]["version"] == "v1.1.0", pm.load_lock()["two_sum"]["version"]
    # update again -> no-op
    pm.cmd_update("two_sum")
    pm.cleanup()


def test_update_respects_constraint():
    r = make_two_sum_repo()
    r.add_standard("v1.1.0", "two_sum", {"t.jvav": "1.1"}, version="1.1.0")
    r.add_standard("v2.0.0", "two_sum", {"t.jvav": "2.0"}, version="2.0.0")
    gh = FakeGitHub({"two_sum": r})
    pm = TestPM(gh)
    pm.cmd_install("BR-get/two_sum", "v1.0.0")
    # constrain to <2.0.0 then update -> stays 1.x
    lock = pm.load_lock()
    lock["two_sum"]["constraint"] = "<2.0.0"
    pm.save_lock(lock)
    pm.cmd_update()
    assert pm.load_lock()["two_sum"]["version"] == "v1.1.0"
    pm.cleanup()


def test_pack_creates_valid_package():
    tmp = tempfile.mkdtemp()
    try:
        for fn, content in [("main.jvav", "tnirp('hi')\n"), ("util.jvav", "def util(): return 1\n")]:
            with open(os.path.join(tmp, fn), "w", encoding="utf-8") as f:
                f.write(content)
        pm = TestPM(FakeGitHub({}))
        pm.cmd_pack(tmp, name="demo", version="1.2.3")
        pkg_path = os.path.join(tmp, "dist", "demo-1.2.3-src.jvavpkg")
        assert os.path.exists(pkg_path), "package file should exist"
        pkg = json.load(open(pkg_path, encoding="utf-8"))
        assert pkg["name"] == "demo"
        assert pkg["version"] == "1.2.3"
        assert pkg["jvav_version"] == "DK27"
        assert pkg["main"] == "main.jvav"
        assert set(pkg["files"].keys()) == {"main.jvav", "util.jvav"}
        assert pkg["files"]["main.jvav"] == "tnirp('hi')\n"
        assert "build_info" in pkg and "timestamp" in pkg["build_info"]
        pm.cleanup()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_pack_main_detection():
    """Without --main, main.jvav is preferred; otherwise first .jvav is used."""
    tmp = tempfile.mkdtemp()
    try:
        with open(os.path.join(tmp, "a.jvav"), "w", encoding="utf-8") as f:
            f.write("x = 1\n")
        with open(os.path.join(tmp, "b.jvav"), "w", encoding="utf-8") as f:
            f.write("y = 2\n")
        pm = TestPM(FakeGitHub({}))
        pm.cmd_pack(tmp, name="demo2", out=os.path.join(tmp, "demo2.jvavpkg"))
        pkg = json.load(open(os.path.join(tmp, "demo2.jvavpkg"), encoding="utf-8"))
        assert pkg["main"] == "a.jvav", f"first .jvav selected, got {pkg['main']}"
        pm.cleanup()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    tests = [
        test_version_tuple_and_satisfies,
        test_basic_install_uninstall_list,
        test_install_with_version_constraint,
        test_dependency_install,
        test_dependency_constraint_selects_version,
        test_dependency_conflict,
        test_circular_dependency,
        test_update,
        test_update_respects_constraint,
        test_pack_creates_valid_package,
        test_pack_main_detection,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as exc:
            import traceback
            traceback.print_exc()
            print(f"  FAIL  {t.__name__}: {exc}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)
