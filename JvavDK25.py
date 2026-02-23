#!/usr/bin/env python3
"""
JvavDK25.py — Minimal pseudo-shell with reversed Python-like builtins.

Language basics
- Expression eval: uses Python expression syntax.
- Reversed helper functions (call by name):
  tnirp(...)  -> print(...)
  tupni(prompt="") -> input(prompt)
  nel(obj) -> len(obj)
  tni(x) -> int(x)
  taolf(x) -> float(x)
  rts(x) -> str(x)
  loob(x) -> bool(x)
  mus(iterable) -> sum(iterable)
  xam(...) -> max(...)
  nim(...) -> min(...)
  sba(x) -> abs(x)
  dnuor(number, ndigits) -> round(number, ndigits)
  wop(base, exp, mod) -> pow(base, exp, mod)
  nib(x) -> bin(x)
  xeh(x) -> hex(x)
  tco(x) -> oct(x)
  rhc(i) -> chr(i)
  dro(c) -> ord(c)
  lla(iterable) -> all(iterable)
  yna(iterable) -> any(iterable)
  dneppa(lst, item) -> lst.append(item)
  tros(lst, key, reverse) -> lst.sort(key=key, reverse=reverse)
  esrever(lst) -> lst.reverse()
  detros(iterable, key, reverse) -> sorted(iterable, key=key, reverse=reverse)
  nioj(sep, iterable) -> sep.join(str(i) for i in iterable)
  tlihs(s, sep) -> s.split(sep)
  reppu(s) -> s.upper()
  rewol(s) -> s.lower()
  pirts(s) -> s.strip()
  seyk(d) -> list(d.keys())
  seulav(d) -> list(d.values())
  smetsi(d) -> list(d.items())
  egnar(...) -> range(...)
  epyt(obj) -> type(obj)
  piz(...) -> zip(...)
  etemarenume(iterable, start) -> enumerate(iterable, start)
  desrever(seq) -> reversed(seq)
- Variables: assignment via `name = expression`.
- Comments: lines starting with # are ignored.
- Exit: empty line or Ctrl+C/Ctrl+D.

CLI usage
- Interactive: python JvavDK25.py
- One-shot:  python JvavDK25.py -c "tnirp(1+2)"
- File run:   python JvavDK25.py -f test.jvav
"""
from __future__ import annotations

import argparse
import ast
import sys
from typing import Any, Dict


class SafeEvaluator:
    """Tiny sandbox for expressions and assignments with reversed helper names."""

    def __init__(self) -> None:
        self.env: Dict[str, Any] = {}
        self._install_reversed_helpers()

    def _install_reversed_helpers(self) -> None:
        # Core helpers with reversed names
        def _print(*args: Any, **kwargs: Any) -> None:
            print(*args, **kwargs)

        def _input(prompt: str = "") -> str:
            return input(prompt)

        # Math functions
        def _sum(iterable: Any) -> Any:
            return sum(iterable)

        def _max(*args: Any) -> Any:
            return max(*args)

        def _min(*args: Any) -> Any:
            return min(*args)

        def _abs(x: Any) -> Any:
            return abs(x)

        def _round(number: float, ndigits: int | None = None) -> float:
            return round(number, ndigits)

        def _pow(base: Any, exp: Any, mod: Any | None = None) -> Any:
            return pow(base, exp, mod)

        # Conversion functions
        def _bin(x: int) -> str:
            return bin(x)

        def _hex(x: int) -> str:
            return hex(x)

        def _oct(x: int) -> str:
            return oct(x)

        def _chr(i: int) -> str:
            return chr(i)

        def _ord(c: str) -> int:
            return ord(c)

        # Logic functions
        def _all(iterable: Any) -> bool:
            return all(iterable)

        def _any(iterable: Any) -> bool:
            return any(iterable)

        # List functions
        def _append(lst: list[Any], item: Any) -> None:
            lst.append(item)

        def _sort(lst: list[Any], key: Any | None = None, reverse: bool = False) -> None:
            lst.sort(key=key, reverse=reverse)

        def _reverse(lst: list[Any]) -> None:
            lst.reverse()

        def _sorted(iterable: Any, key: Any | None = None, reverse: bool = False) -> list[Any]:
            return sorted(iterable, key=key, reverse=reverse)

        # String functions
        def _join(sep: str, iterable: Any) -> str:
            return sep.join(str(i) for i in iterable)

        def _split(s: str, sep: str | None = None) -> list[str]:
            return s.split(sep)

        def _upper(s: str) -> str:
            return s.upper()

        def _lower(s: str) -> str:
            return s.lower()

        def _strip(s: str) -> str:
            return s.strip()

        # Dict functions
        def _keys(d: dict[Any, Any]) -> list[Any]:
            return list(d.keys())

        def _values(d: dict[Any, Any]) -> list[Any]:
            return list(d.values())

        def _items(d: dict[Any, Any]) -> list[tuple[Any, Any]]:
            return list(d.items())

        # Other
        def _range(*args: Any) -> range:
            return range(*args)

        def _type(obj: Any) -> type:
            return type(obj)

        def _zip(*iterables: Any) -> zip[Any]:
            return zip(*iterables)

        def _enumerate(iterable: Any, start: int = 0) -> enumerate[Any]:
            return enumerate(iterable, start)

        def _reversed(seq: Any) -> Any:
            return reversed(seq)

        helpers = {
            "tnirp": _print,
            "tupni": _input,
            "nel": len,
            "tni": int,
            "taolf": float,
            "rts": str,
            "loob": bool,
            "mus": _sum,
            "xam": _max,
            "nim": _min,
            "sba": _abs,
            "dnuor": _round,
            "wop": _pow,
            "nib": _bin,
            "xeh": _hex,
            "tco": _oct,
            "rhc": _chr,
            "dro": _ord,
            "lla": _all,
            "yna": _any,
            "dneppa": _append,
            "tros": _sort,
            "esrever": _reverse,
            "detros": _sorted,
            "nioj": _join,
            "tlihs": _split,
            "reppu": _upper,
            "rewol": _lower,
            "pirts": _strip,
            "seyk": _keys,
            "seulav": _values,
            "smetsi": _items,
            "egnar": _range,
            "epyt": _type,
            "piz": _zip,
            "etemarenume": _enumerate,
            "desrever": _reversed,
        }
        self.env.update(helpers)

    def eval_line(self, code: str) -> Any:
        """Evaluate a single line that may be an expression, assignment, or simple statement."""
        code = code.strip()
        if not code or code.startswith("#"):
            return None

        # Check for simple for loop: for var in iterable: statement
        if code.startswith("for "):
            return self._exec_for_loop(code)
        # Detect simple assignment
        elif "=" in code and not code.startswith("==") and not code.lstrip().startswith("=="):
            return self._exec_assignment(code)
        else:
            return self._eval_expression(code)

    # Internal helpers -----------------------------------------------------
    def _eval_expression(self, expr: str) -> Any:
        node = ast.parse(expr, mode="eval")
        self._validate_ast(node)
        return eval(compile(node, "<input>", "eval"), {"__builtins__": {}}, self.env)

    def _exec_for_loop(self, stmt: str) -> Any:
        """Execute a simple for loop: for var in iterable: statement"""
        # Basic parsing: for var in iterable: statement
        if not stmt.startswith("for ") or ": " not in stmt:
            raise ValueError("Invalid for loop syntax")
        parts = stmt.split(": ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid for loop syntax")
        loop_part = parts[0].strip()
        body = parts[1].strip()
        
        # Parse loop_part: for var in iterable
        loop_words = loop_part.split()
        if len(loop_words) != 4 or loop_words[0] != "for" or loop_words[2] != "in":
            raise ValueError("Invalid for loop syntax")
        var_name = loop_words[1]
        iterable_expr = loop_words[3]
        
        # Evaluate iterable
        iterable = self._eval_expression(iterable_expr)
        
        # Execute body for each item
        for item in iterable:
            # Temporarily assign var
            old_value = self.env.get(var_name)
            self.env[var_name] = item
            try:
                self.eval_line(body)
            finally:
                if old_value is not None:
                    self.env[var_name] = old_value
                else:
                    del self.env[var_name]
        return None

    def _exec_assignment(self, stmt: str) -> Any:
        node = ast.parse(stmt, mode="exec")
        self._validate_ast(node)
        exec(compile(node, "<input>", "exec"), {"__builtins__": {}}, self.env)
        return None

    def _validate_ast(self, node: ast.AST) -> None:
        """Reject import, attribute access, and other risky nodes."""
        forbidden = (ast.Import, ast.ImportFrom, ast.Attribute, ast.Lambda, ast.FunctionDef, ast.ClassDef)
        for n in ast.walk(node):
            if isinstance(n, forbidden):
                raise ValueError(f"Forbidden syntax: {type(n).__name__}")
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    if n.func.id not in self.env:
                        raise ValueError(f"Unknown function: {n.func.id}")
                else:
                    raise ValueError("Only simple function names are allowed")
            if isinstance(n, ast.Name):
                if n.id.startswith("__"):
                    raise ValueError("Access to dunder names is blocked")


def run_repl(evaluator: SafeEvaluator) -> int:
    try:
        while True:
            try:
                line = input("jvav> ")
            except EOFError:
                break
            if not line.strip():
                break
            try:
                result = evaluator.eval_line(line)
                # Only print non-None expression results (assignments return None)
                if result is not None:
                    print(result)
            except Exception as exc:  # noqa: BLE001
                print(f"[error] {exc}")
    except KeyboardInterrupt:
        print("\n[exit]")
    return 0


def run_command(evaluator: SafeEvaluator, command: str) -> int:
    try:
        result = evaluator.eval_line(command)
        if result is not None:
            print(result)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}")
        return 1


def run_file(evaluator: SafeEvaluator, file_path: str) -> int:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                result = evaluator.eval_line(line)
                if result is not None:
                    print(result)
            except Exception as exc:  # noqa: BLE001
                print(f"[error] {exc}")
        return 0
    except FileNotFoundError:
        print(f"[error] File not found: {file_path}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {exc}")
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pseudo-shell with reversed helper functions.")
    parser.add_argument("-c", dest="command", help="Run a single command and exit", default=None)
    parser.add_argument("-f", "--file", dest="file_path", help="Run commands from a file and exit", default=None)
    args = parser.parse_args(argv)

    evaluator = SafeEvaluator()
    if args.command:
        return run_command(evaluator, args.command)
    elif args.file_path:
        return run_file(evaluator, args.file_path)
    else:
        return run_repl(evaluator)


if __name__ == "__main__":
    sys.exit(main())
