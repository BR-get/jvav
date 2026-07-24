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
- Init project: python JvavDK25.py init myproject
- Build project: python JvavDK25.py build
- Run project: python JvavDK25.py run main.jvav
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
        # Check if it's a .jvavpkg file
        if file_path.endswith('.jvavpkg'):
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                package = json.load(f)

            # Extract main file content
            main_content = package["files"]["main.jvav"]
            lines = main_content.split('\n')
        else:
            # Regular .jvav file
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


def run_init(project_name: str) -> int:
    """Initialize a new JVAV project."""
    import os
    import shutil

    try:
        # Check if project directory already exists
        if os.path.exists(project_name):
            print(f"[error] Project '{project_name}' already exists")
            return 1

        # Create project directory
        os.makedirs(project_name)
        print(f"Created project directory: {project_name}")

        # Create main.jvav file
        main_content = f'''# {project_name}.jvav - Main project file
# This is the entry point for your JVAV brainwave application

# Welcome message
tnirp("Hello from {project_name}!")

# Basic brainwave interface setup
sensitivity = 0.8
threshold = 0.5
channels = 8

tnirp("Brainwave configuration loaded:")
tnirp("Sensitivity: " + rts(sensitivity))
tnirp("Threshold: " + rts(threshold))
tnirp("Channels: " + rts(channels))

# Example: Process some neural data
neural_data = [0.1, 0.3, 0.7, 0.2, 0.9, 0.4, 0.6, 0.8]
tnirp("Neural activity levels:")
for i in egnar(nel(neural_data)): tnirp("Channel " + rts(i) + ": " + rts(neural_data[i]))

# Calculate average activity
avg_activity = mus(neural_data) / nel(neural_data)
tnirp("Average neural activity: " + rts(dnuor(avg_activity, 3)))
'''
        with open(os.path.join(project_name, "main.jvav"), 'w', encoding='utf-8') as f:
            f.write(main_content)
        print("Created main.jvav")

        # Create brainwave.yaml config file
        config_content = '''# Brainwave Interface Configuration
# This file configures the EEG adapter and neural processing parameters

brainwave:
  adapter: "eeg_adapter_v2"
  sampling_rate: 256
  channels: 8
  sensitivity: 0.8
  threshold: 0.5
  filters:
    - type: "bandpass"
      low_freq: 1.0
      high_freq: 40.0
    - type: "notch"
      freq: 50.0

security:
  signature_required: true
  hash_algorithm: "SHA256"
  verify_on_load: true

logging:
  level: "INFO"
  file: "brainwave.log"
'''
        with open(os.path.join(project_name, "brainwave.yaml"), 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("Created brainwave.yaml")

        # Create README.md
        readme_content = f'''# {project_name}

A JVAV brainwave application project.

## Getting Started

1. Connect your EEG device
2. Configure brainwave.yaml for your hardware
3. Run the application:
   ```
   jvav run main.jvav
   ```

## Building

To build a distributable package:
```
jvav build
```

## Project Structure

- `main.jvav` - Main application entry point
- `brainwave.yaml` - EEG adapter configuration
- `dist/` - Built distributables (after build)

## Brainwave Functions

This project uses JVAV's reversed built-in functions:
- `tnirp()` - Print output
- `mus()` - Sum values
- `egnar()` - Create ranges
- `nel()` - Get length
- `dnuor()` - Round numbers

See the JVAV documentation for the complete function reference.
'''
        with open(os.path.join(project_name, "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("Created README.md")

        # Create dist directory
        os.makedirs(os.path.join(project_name, "dist"))
        print("Created dist/ directory")

        print(f"\nProject '{project_name}' initialized successfully!")
        print(f"Enter the directory: cd {project_name}")
        print("Run the project: jvav run main.jvav")
        print("Build the project: jvav build")

        return 0

    except Exception as exc:
        print(f"[error] Failed to initialize project: {exc}")
        return 1


def run_build() -> int:
    """Build the current JVAV project."""
    import os
    import hashlib
    import json

    try:
        # Check if we're in a project directory
        if not os.path.exists("main.jvav"):
            print("[error] No main.jvav found. Are you in a JVAV project directory?")
            return 1

        if not os.path.exists("brainwave.yaml"):
            print("[error] No brainwave.yaml found. Are you in a JVAV project directory?")
            return 1

        project_name = os.path.basename(os.getcwd())
        print(f"Building project: {project_name}")

        # Create dist directory if it doesn't exist
        dist_dir = "dist"
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)

        # Read main.jvav
        with open("main.jvav", 'r', encoding='utf-8') as f:
            main_content = f.read()

        # Read brainwave.yaml
        with open("brainwave.yaml", 'r', encoding='utf-8') as f:
            config_content = f.read()

        # Create package structure
        package = {
            "name": project_name,
            "version": "1.0.0",
            "jvav_version": "DK25",
            "main": "main.jvav",
            "config": "brainwave.yaml",
            "files": {
                "main.jvav": main_content,
                "brainwave.yaml": config_content
            },
            "build_info": {
                "timestamp": "2026-02-23T12:00:00Z",
                "builder": "JvavDK25",
                "platform": "windows-x64"
            }
        }

        # Add any additional .jvav files
        for file in os.listdir("."):
            if file.endswith(".jvav") and file != "main.jvav":
                with open(file, 'r', encoding='utf-8') as f:
                    package["files"][file] = f.read()

        # Create package file
        package_file = os.path.join(dist_dir, f"{project_name}.jvavpkg")
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False)

        # Calculate hash
        with open(package_file, 'rb') as f:
            package_hash = hashlib.sha256(f.read()).hexdigest()

        # Create signature file
        sig_file = os.path.join(dist_dir, f"{project_name}.jvavpkg.sig")
        with open(sig_file, 'w', encoding='utf-8') as f:
            f.write(f"SHA256:{package_hash}\n")
            f.write("Signed-by: JvavDK25 Builder\n")
            f.write("Timestamp: 2026-02-23T12:00:00Z\n")

        # Create executable wrapper (batch file for Windows)
        wrapper_content = f'''@echo off
echo JVAV Brainwave Application: {project_name}
echo ========================================
echo Starting brainwave interface...
echo.
echo Running {project_name}.jvav...
echo.
python "%~dp0JvavDK25.exe" -f "%~dp0{project_name}.jvavpkg"
echo.
echo Application finished.
pause
'''
        wrapper_file = os.path.join(dist_dir, f"run_{project_name}.bat")
        with open(wrapper_file, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)

        print(f"Package created: {package_file}")
        print(f"Signature created: {sig_file}")
        print(f"Runner created: {wrapper_file}")
        print(f"Package hash: {package_hash}")
        print("\nBuild completed successfully!")
        print(f"Run with: dist\\run_{project_name}.bat")

        return 0

    except Exception as exc:
        print(f"[error] Build failed: {exc}")
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pseudo-shell with reversed helper functions.")
    parser.add_argument("-c", dest="command", help="Run a single command and exit", default=None)
    parser.add_argument("-f", "--file", dest="file_path", help="Run commands from a file and exit", default=None)
    parser.add_argument("action", nargs="?", help="Action to perform: init, build, run", default=None)
    parser.add_argument("target", nargs="?", help="Target for action (project name for init, file for run)", default=None)
    args = parser.parse_args(argv)

    evaluator = SafeEvaluator()
    if args.command:
        return run_command(evaluator, args.command)
    elif args.file_path:
        return run_file(evaluator, args.file_path)
    elif args.action == "init" and args.target:
        return run_init(args.target)
    elif args.action == "build":
        return run_build()
    elif args.action == "run" and args.target:
        return run_file(evaluator, args.target)
    else:
        return run_repl(evaluator)


if __name__ == "__main__":
    sys.exit(main())
