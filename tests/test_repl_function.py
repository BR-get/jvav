"""Minimal self-test for JVAV DK27 — REPL function scope (v5 fix).

Run: python tests/test_repl_function.py
"""

import sys
import os
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


if __name__ == '__main__':
    tests = [
        test_basic_reversed_fn,
        test_function_definition,
        test_recursive_function,
        test_multi_call_shared_scope,
        test_fibonacci,
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
