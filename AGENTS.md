# AGENTS.md

JVAV is a Python-implemented "brainwave" programming language (`.jvav` files interpreted by `src/JvavDK27.py`, currently DK27 **v6**) plus a hand-written static HTML/CSS/JS release site and a GitHub-based package manager (`src/jvavpkg.py`). Packaging is PyInstaller only.

## Layout
- `src/JvavDK27.py` — the only live interpreter (DK27 v6). `JvavDK25.py` / `JvavDK26.py` are legacy; don't touch.
- `src/jvavpkg.py` — package manager (info/install/uninstall/list/update). Installs to `~/.jvav/packages/` (global) or `./.jvav/packages/` (project-local).
- `*.html` at repo root + `downloads/index.html` + `downloads/archive/index.html` — static site. `help.html` is the main doc; `help-pkg.html`/`help-cli.html`/`help-protocol.html`/`help-security.html` are sub-docs linked via a shared `.doc-nav` tab bar (active page highlighted).
- `examples/*.jvav` — sample programs. `tests/test_repl_function.py` (interpreter) + `tests/test_jvavpkg.py` (package manager) — plain-assert self-tests, no pytest.
- `*.spec` at root — PyInstaller configs. `jvav_dk27.spec` builds the interpreter, `jvavpkg.spec` builds the package manager.

## Language quirk
`.jvav` reverses Python builtins: `print`→`tnirp`, `len`→`nel`, `range`→`egnar`, `str`→`rts`, `dict`→`tcid`, and **`sum`→`mus`** (this is the corrected form — older files used the wrong `nus`; keep `mus`). All code runs in the `SafeEvaluator` sandbox in `JvavDK27.py`. Tests and examples must use the reversed names.

## Commands
- Run interpreter tests: `python tests\test_repl_function.py` (8 tests)
- Run package-manager tests: `python tests\test_jvavpkg.py` (9 tests; offline, uses a fake GitHub client)
- Run a script: `python src\JvavDK27.py -f file.jvav` · one line: `-c "tnirp('hi')"` · REPL: no args · self-check: `info`
- Package manager: `python src\jvavpkg.py <info|install|uninstall|list|update|pack>` — one package per GitHub repo; repo files direct (no Releases), git tag = version; >100MB assets via `jvavpkg.links` external links with mandatory SHA256. `pack` packages local `*.jvav` into a `.jvavpkg`.
- Build: `python -m PyInstaller jvav_dk27.spec --clean --noconfirm` then copy `dist\jvav_dk27.exe` → `downloads\`. Build `jvavpkg.exe` from `jvavpkg.spec` the same way. `build/` and `dist/` are gitignored.
- Nuitka pilot (both exes verified): `python -m nuitka --onefile --assume-yes-for-downloads --no-deployment-flag=self-execution --output-dir=nuitka_build --output-filename=<name>_nuitka.exe src\<file>.py` — auto-downloads Dependency Walker + Zig (no MSVC needed on this box; `--mingw64` is unsupported on Python 3.13). The `--no-deployment-flag=self-execution` flag is required for the interpreter (else `-c`/`-f` args are rejected as self-recursion). Builds ~24% smaller, ~50% faster startup than PyInstaller. `jvav_dk27` and `jvavpkg` Nuitka builds passed function + sandbox verification. Copy to `downloads\`. `nuitka_build/` is gitignored.

## Gotchas
- CLI is only `-c`, `-f`, `info`; anything else drops into the REPL. `main()` is JvavDK27.py:991. Docs referencing `[init|build|run|verify]` commands are fictional — don't resurrect them.
- Release info (version, SHA256, test counts) is duplicated across `README.md`, `src/verify_production_status.py`, `src/report.py`, and several HTML pages — keep in sync on version bumps. Rebuilding `jvav_dk27.exe` or `jvavpkg.exe` changes its SHA256; update all copies.
- Test counts are currently 8 interpreter + 11 package-manager (19 total). Update these numbers anywhere they appear when adding tests.
- Package-manager `jvavpkg.json` dependency keys are `owner/repo`; short names only resolve after first install writes them to local `registry.json`.
- `jvav_dk27.spec` bundles `assets/logo.ico` and lists `hiddenimports`; update both if imports are added. `jvavpkg.spec` builds the standalone package manager.
- The interpreter auto-discovers jvavpkg-installed `library`/`plugin` packages (from `~/.jvav/packages` and `./.jvav/packages`) as loadable plugins — `plugin load <name>` injects their `src/*.jvav` functions into `env`. Program-type packages are not loaded as plugins.
- `.jvav` sandbox blocks attribute access in exec mode — package/library source must not use `.method()` calls (e.g. no `dict.setdefault`), use reversed helpers instead.
- `JvavDK27.py` rewraps stdout/stderr to UTF-8 on Windows at import (~line 31); `src/report.py`, `src/verify_production_status.py`, `examples/PROJECT_SUMMARY.py`, and `src/jvavpkg.py` do the same. Other `.py` files contain Chinese text that may render as mojibake in this shell — don't "fix" or re-encode them.
