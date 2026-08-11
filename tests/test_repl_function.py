"""Minimal self-test for JVAV DK27 — REPL function scope (v5 fix).

Run: python tests/test_repl_function.py
"""

import sys
import os
import json
import shutil
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from JvavDK27 import SafeEvaluator


def test_basic_reversed_fn():
    """160+ reversed builtins should work."""
    e = SafeEvaluator()
    assert e.eval_line('tnirp("hello")') is None  # print returns None


def test_function_definition():
    """def should create callable functions in shared env."""
    e = SafeEvaluator()
    e.eval_line('def add(a, b): return a + b')
    result = e.eval_line('add(2, 3)')
    assert result == 5, f"expected 5, got {result}"


def test_recursive_function():
    """Factorial via recursion — the v5 REPL scope fix."""
    e = SafeEvaluator()
    e.eval_line('def fact(n): return 1 if n <= 1 else n * fact(n-1)')
    result = e.eval_line('fact(5)')
    assert result == 120, f"expected 120, got {result}"


def test_multi_call_shared_scope():
    """Variables defined in earlier REPL lines are visible to later ones."""
    e = SafeEvaluator()
    e.eval_line('x = 10')
    e.eval_line('y = x + 5')
    result = e.eval_line('y')
    assert result == 15, f"expected 15, got {result}"


def test_fibonacci():
    """Deeper recursion: fibonacci(8) = 21."""
    e = SafeEvaluator()
    e.eval_line('def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)')
    result = e.eval_line('fib(8)')
    assert result == 21, f"expected 21, got {result}"


def _make_pkg(cwd, name, src_code):
    """Create a jvavpkg-installed library/plugin in cwd/.jvav/packages/<name>."""
    pkg_dir = os.path.join(cwd, '.jvav', 'packages', name)
    src_dir = os.path.join(pkg_dir, 'src')
    os.makedirs(src_dir, exist_ok=True)
    manifest = {
        "name": name,
        "type": "plugin",
        "assets": {"win64": {"source": f"dist/{name}-1.0.0-src.jvavpkg"}},
    }
    with open(os.path.join(pkg_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False)
    with open(os.path.join(src_dir, 'main.jvav'), 'w', encoding='utf-8') as f:
        f.write(src_code)


def test_package_plugin_discovery():
    """Packages installed by jvavpkg appear as available plugins."""
    tmp = tempfile.mkdtemp()
    try:
        _make_pkg(tmp, 'demo_math', "def dbod(x):\n    return x * 2\n")
        old = os.getcwd()
        try:
            os.chdir(tmp)
            e = SafeEvaluator()
            assert 'demo_math' in e.list_plugins(), f"demo_math missing in {e.list_plugins()}"
        finally:
            os.chdir(old)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_package_plugin_load_unload():
    """Loading a package injects its functions; unloading removes them."""
    tmp = tempfile.mkdtemp()
    try:
        _make_pkg(tmp, 'demo_math', "def dbod(x):\n    return x * 2\n\ndef gnis(s):\n    return s[::-1]\n")
        old = os.getcwd()
        try:
            os.chdir(tmp)
            e = SafeEvaluator()
            assert e.load_plugin('demo_math'), "load should succeed"
            assert e.env.get('dbod')(21) == 42, "dbod(21) should be 42"
            assert e.env.get('gnis')('abc') == 'cba', "gnis('abc') should be 'cba'"
            assert 'demo_math' in e.list_loaded_plugins()
            assert e.unload_plugin('demo_math')
            assert 'dbod' not in e.env, "dbod should be removed after unload"
        finally:
            os.chdir(old)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_package_plugin_missing():
    """Loading an unknown plugin returns False."""
    e = SafeEvaluator()
    assert e.load_plugin('no_such_plugin') is False


if __name__ == '__main__':
    tests = [
        test_basic_reversed_fn,
        test_function_definition,
        test_recursive_function,
        test_multi_call_shared_scope,
        test_fibonacci,
        test_package_plugin_discovery,
        test_package_plugin_load_unload,
        test_package_plugin_missing,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {t.__name__}: {exc}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)
