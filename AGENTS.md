# AGENTS.md

JVAV is a Python-implemented "brainwave" programming language (`.jvav` files interpreted by `src/JvavDK27.py`) plus a hand-written static HTML/CSS/JS release site. No package manager; only PyInstaller for packaging.

## Layout
- `src/JvavDK27.py` — the only live interpreter (DK27 v5). `JvavDK25.py` / `JvavDK26.py` are legacy; don't touch.
- `*.html` at repo root and `downloads/index.html` — static site pages for downloads/versions/changelog.
- `examples/*.jvav` — sample programs. `tests/test_repl_function.py` — the test suite.
- `*.spec` at root — PyInstaller configs. `jvav_dk27.spec` builds the current release.

## Language quirk
`.jvav` reverses Python builtins: `print`→`tnirp`, `len`→`nel`, `range`→`egnar`, `str`→`rts`, `dict`→`tcid`. All code runs in the `SafeEvaluator` sandbox in `JvavDK27.py`. Tests and examples must use the reversed names.

## Commands
- Run tests (plain assert self-test, no pytest): `python tests\test_repl_function.py`
- Run package-manager tests: `python tests\test_jvavpkg.py`
- Run a script: `python src\JvavDK27.py -f file.jvav`
- Run one line: `python src\JvavDK27.py -c "tnirp('hi')"`
- REPL: `python src\JvavDK27.py` · self-check: `python src\JvavDK27.py info`
- Build: `python -m PyInstaller jvav_dk27.spec --clean --noconfirm`, then copy `dist\jvav_dk27.exe` to `downloads\`. Build `jvavpkg.exe` from `jvavpkg.spec` the same way. `build/` and `dist/` are gitignored.
- Package manager: `python src\jvavpkg.py <info|install|uninstall|list|update>` (one package per GitHub repo; repo files direct, git tag = version; >100MB assets via `jvavpkg.links` external links with mandatory SHA256).

## Gotchas
- CLI is only `-c`, `-f`, and `info` (anything else drops into the REPL); `main()` (JvavDK27.py:888). Some old docs referenced `[init|build|run|verify]` project commands — they don't exist.
- Release info (version, SHA256, test counts) is duplicated across `README.md`, `src/verify_production_status.py`, `src/report.py`, and several HTML pages — keep them in sync on version bumps.
- The current test suite has 9 package-manager tests (`tests/test_jvavpkg.py`) plus 5 interpreter tests (`tests/test_repl_function.py`).
- `jvav_dk27.spec` bundles `assets/logo.ico` and lists `hiddenimports` for the module system; update both if imports are added. `jvavpkg.spec` builds the standalone package manager.
- Package-manager `jvavpkg.json` dependency keys are `owner/repo` (short names resolve via local `registry.json` after first install).
- `JvavDK27.py` rewraps stdout/stderr to UTF-8 on Windows at import (~line 31); `src/report.py`, `src/verify_production_status.py`, and `examples/PROJECT_SUMMARY.py` do the same — other `.py` files contain Chinese text that may render as mojibake — don't "fix" or re-encode them.
