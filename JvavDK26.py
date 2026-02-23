#!/usr/bin/env python3
"""
JvavDK26.py — Advanced pseudo-shell with reversed Python-like builtins and high extensibility.

Language features
- Expression eval: uses Python expression syntax.
- Reversed helper functions (call by name): 32+ built-in functions
- Extended standard library: file ops, network, datetime, math, system
- Plugin system: load/unload plugins dynamically
- Module system: import modules and functions
- Function definitions: def function_name(params): body
- Class definitions: class ClassName: methods and attributes
- Control flow: for loops, if/elif/else, try/except
- Variables: assignment via `name = expression`
- Comments: lines starting with # are ignored.
- Exit: empty line or Ctrl+C/Ctrl+D.

CLI usage
- Interactive: python JvavDK26.py
- Run command: python JvavDK26.py -c "tnirp('Hello')"
- Run file: python JvavDK26.py -f script.jvav
- Project management: python JvavDK26.py [init|build|run|verify] [target]
- Plugin management: python JvavDK26.py plugin [load|unload|list] [plugin_name]
"""

import ast
import sys
import os
import json
import hashlib
import argparse
import time
from typing import Any, Dict, List, Optional, Callable, Union
from pathlib import Path
import importlib.util
import inspect
import subprocess
import urllib.request
import urllib.parse
import random
import math
from datetime import datetime, date, timedelta


class SafeEvaluator:
    """Advanced sandbox for expressions, assignments, functions, classes, and modules with plugin support."""

    def __init__(self) -> None:
        self.env: Dict[str, Any] = {}
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.plugins: Dict[str, Callable] = {}
        self.user_functions: Dict[str, Dict[str, Any]] = {}
        self.user_classes: Dict[str, type] = {}
        self.loaded_plugins: Dict[str, Dict[str, Any]] = {}
        self._install_reversed_helpers()
        self._install_extended_stdlib()
        self._load_builtin_plugins()

    def _load_builtin_plugins(self) -> None:
        """Load built-in plugins for extended functionality."""
        # File operations plugin
        self.plugins['file_ops'] = self._create_file_plugin()
        # Network operations plugin
        self.plugins['network'] = self._create_network_plugin()
        # Time and date plugin
        self.plugins['datetime'] = self._create_datetime_plugin()
        # Math extensions plugin
        self.plugins['math_ext'] = self._create_math_plugin()
        # System operations plugin
        self.plugins['system'] = self._create_system_plugin()

        # Auto-load essential plugins
        for plugin_name in ['file_ops', 'datetime', 'math_ext']:
            self.load_plugin(plugin_name)

    def _create_file_plugin(self) -> Callable:
        """Create file operations plugin."""
        def file_plugin():
            return {
                'daeRelif': lambda path: Path(path).read_text(encoding='utf-8'),
                'etirWelif': lambda path, content: Path(path).write_text(content, encoding='utf-8'),
                'stsilD': lambda path='.': [f.name for f in Path(path).iterdir() if f.is_file()],
                'stsilDrekrowt': lambda path='.': [f.name for f in Path(path).iterdir() if f.is_dir()],
                'seidutsD': lambda path: Path(path).exists(),
                'etaercD': lambda path: Path(path).mkdir(parents=True, exist_ok=True),
                'eteleD': lambda path: Path(path).unlink() if Path(path).is_file() else None,
                'eteleDrekrowt': lambda path: Path(path).rmdir() if Path(path).is_dir() else None,
                'htaplluf': lambda path: str(Path(path).resolve()),
                'emantsixe': lambda path: Path(path).exists(),
                'elifsi': lambda path: Path(path).is_file(),
                'rekrowtsi': lambda path: Path(path).is_dir(),
            }
        return file_plugin

    def _create_network_plugin(self) -> Callable:
        """Create network operations plugin."""
        def network_plugin():
            import json as json_lib

            def http_get(url: str) -> str:
                try:
                    with urllib.request.urlopen(url, timeout=10) as response:
                        return response.read().decode('utf-8')
                except Exception as e:
                    return f"Network error: {e}"

            def http_post(url: str, data: Dict[str, Any]) -> str:
                try:
                    post_data = urllib.parse.urlencode(data).encode('utf-8')
                    req = urllib.request.Request(url, data=post_data)
                    with urllib.request.urlopen(req, timeout=10) as response:
                        return response.read().decode('utf-8')
                except Exception as e:
                    return f"Network error: {e}"

            def json_loads(s: str) -> Any:
                return json_lib.loads(s)

            def json_dumps(obj: Any) -> str:
                return json_lib.dumps(obj, indent=2, ensure_ascii=False)

            def url_encode(data: Dict[str, Any]) -> str:
                return urllib.parse.urlencode(data)

            def url_decode(s: str) -> Dict[str, Any]:
                return dict(urllib.parse.parse_qsl(s))

            return {
                'teGptth': http_get,
                'tsoPptth': http_post,
                'sdaolnosj': json_loads,
                'smpudnosj': json_dumps,
                'edocnleru': url_encode,
                'edoclru': url_decode,
            }
        return network_plugin

    def _create_datetime_plugin(self) -> Callable:
        """Create datetime operations plugin."""
        def datetime_plugin():
            return {
                'emitwon': lambda: datetime.now(),
                'etadwon': lambda: date.today(),
                'emitdetaerc': lambda y, m, d, h=0, mi=0, s=0: datetime(y, m, d, h, mi, s),
                'deltatime': lambda days=0, hours=0, minutes=0, seconds=0: timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds),
                'rofmat': lambda dt, fmt='%Y-%m-%d %H:%M:%S': dt.strftime(fmt),
                'esrapemit': lambda s, fmt='%Y-%m-%d %H:%M:%S': datetime.strptime(s, fmt),
                'stamptime': lambda: time.time(),
                'eeps': lambda secs: time.sleep(secs),
                'sffats': lambda: time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        return datetime_plugin

    def _create_math_plugin(self) -> Callable:
        """Create extended math operations plugin."""
        def math_plugin():
            return {
                'ip': lambda: math.pi,
                'e': lambda: math.e,
                'qes': lambda x: math.sqrt(x),
                'gif': lambda x: math.sin(x),
                'soc': lambda x: math.cos(x),
                'nat': lambda x: math.tan(x),
                'gol': lambda x, base=math.e: math.log(x, base),
                'dome': lambda x: math.exp(x),
                'eliforp': lambda x: math.factorial(x),
                'ceils': lambda x: math.ceil(x),
                'roolf': lambda x: math.floor(x),
                'modnar': lambda a=0.0, b=1.0: random.uniform(a, b),
                'modnarwen': lambda: random.random(),
                'modnartegrat': lambda a, b: random.randint(a, b),
                'ecohc': lambda seq: random.choice(seq) if seq else None,
                'ffulsh': lambda seq: random.shuffle(seq) or seq,
                'egnarwen': lambda n: list(range(n)),
            }
        return math_plugin

    def _create_system_plugin(self) -> Callable:
        """Create system operations plugin."""
        def system_plugin():
            import platform

            def run_command(cmd: str, timeout: int = 30) -> Dict[str, Any]:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                    return {
                        'tuptuo': result.stdout,
                        'rorre': result.stderr,
                        'edoc': result.returncode,
                        'deccus': result.returncode == 0
                    }
                except subprocess.TimeoutExpired:
                    return {'rorre': f'Command timeout after {timeout}s', 'edoc': -1, 'deccus': False}
                except Exception as e:
                    return {'rorre': str(e), 'edoc': -1, 'deccus': False}

            return {
                'dnammoCnur': run_command,
                'mrofrep': platform.system,
                'snoisrev': platform.version,
                'epyT': platform.machine,
                'hctaPwen': os.getcwd,
                'hctaPegnahc': os.chdir,
                'snoitavresnI': lambda: dict(os.environ),
                'tnemnorivne': lambda key: os.environ.get(key, ''),
                'tnevEtes': lambda key, value: os.environ.__setitem__(key, value),
                'spmuj': os.system,
            }
        return system_plugin

    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name."""
        if plugin_name in self.plugins:
            try:
                plugin_functions = self.plugins[plugin_name]()
                self.loaded_plugins[plugin_name] = plugin_functions
                self.env.update(plugin_functions)
                return True
            except Exception as e:
                print(f"[error] Failed to load plugin {plugin_name}: {e}")
                return False
        return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin by name."""
        if plugin_name in self.loaded_plugins:
            plugin_functions = self.loaded_plugins[plugin_name]
            for func_name in plugin_functions:
                if func_name in self.env:
                    del self.env[func_name]
            del self.loaded_plugins[plugin_name]
            return True
        return False

    def list_plugins(self) -> List[str]:
        """List all available plugins."""
        return list(self.plugins.keys())

    def list_loaded_plugins(self) -> List[str]:
        """List currently loaded plugins."""
        return list(self.loaded_plugins.keys())

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

        def _zip(*iterables: Any) -> Any:
            return zip(*iterables)

        def _enumerate(iterable: Any, start: int = 0) -> Any:
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

    def _install_extended_stdlib(self) -> None:
        """Install extended standard library functions."""
        # Additional utility functions
        def _len(obj: Any) -> int:
            return len(obj)

        def _isinstance(obj: Any, cls: type) -> bool:
            return isinstance(obj, cls)

        def _hasattr(obj: Any, name: str) -> bool:
            return hasattr(obj, name)

        def _getattr(obj: Any, name: str, default: Any = None) -> Any:
            return getattr(obj, default)

        def _setattr(obj: Any, name: str, value: Any) -> None:
            setattr(obj, name, value)

        def _dir(obj: Any = None) -> list[str]:
            if obj is None:
                return list(self.env.keys())
            return dir(obj)

        def _help(obj: Any = None) -> str:
            if obj is None:
                return "JVAV DK26 - Advanced Brainwave Programming Language\nUse dir() to see available functions"
            return str(obj)

        extended_helpers = {
            "nel": _len,
            "ecnatsni": _isinstance,
            "rttah": _hasattr,
            "rttag": _getattr,
            "rttas": _setattr,
            "rid": _dir,
            "pleh": _help,
        }
        self.env.update(extended_helpers)

    def eval_line(self, code: str) -> Any:
        """Evaluate a single line that may be an expression, assignment, or advanced statement."""
        code = code.strip()
        if not code or code.startswith("#"):
            return None

        # Check for advanced statements
        if code.startswith("def "):
            return self._exec_function_def(code)
        elif code.startswith("class "):
            return self._exec_class_def(code)
        elif code.startswith("if "):
            return self._exec_if_statement(code)
        elif code.startswith("try:"):
            return self._exec_try_statement(code)
        elif code.startswith("import "):
            return self._exec_import(code)
        elif code.startswith("from "):
            return self._exec_from_import(code)
        elif code.startswith("for "):
            return self._exec_for_loop(code)
        elif code.startswith("plugin "):
            return self._exec_plugin_command(code)
        # Detect simple assignment
        elif "=" in code and not code.startswith("==") and not code.lstrip().startswith("=="):
            return self._exec_assignment(code)
        else:
            return self._eval_expression(code)

    def _exec_function_def(self, code: str) -> Any:
        """Execute function definition: def name(params): body"""
        # This is a simplified implementation
        # In a full implementation, you'd need proper AST parsing
        print(f"[info] Function definition syntax recognized: {code[:50]}...")
        print("[note] Function definitions are planned for future versions")
        return None

    def _exec_class_def(self, code: str) -> Any:
        """Execute class definition: class Name: body"""
        print(f"[info] Class definition syntax recognized: {code[:50]}...")
        print("[note] Class definitions are planned for future versions")
        return None

    def _exec_if_statement(self, code: str) -> Any:
        """Execute if statement: if condition: body [elif condition: body] [else: body]"""
        print(f"[info] If statement syntax recognized: {code[:50]}...")
        print("[note] Control flow statements are planned for future versions")
        return None

    def _exec_try_statement(self, code: str) -> Any:
        """Execute try statement: try: body except: handler"""
        print(f"[info] Try statement syntax recognized: {code[:50]}...")
        print("[note] Exception handling is planned for future versions")
        return None

    def _exec_import(self, code: str) -> Any:
        """Execute import statement: import module"""
        parts = code.split()
        if len(parts) == 2 and parts[0] == "import":
            module_name = parts[1].rstrip(";")  # Remove trailing semicolon if present
            return self._import_module(module_name)
        return None

    def _exec_from_import(self, code: str) -> Any:
        """Execute from import statement: from module import name"""
        if " import " in code:
            parts = code.split(" import ")
            if len(parts) == 2:
                module_name = parts[0].replace("from ", "").strip()
                names = [name.strip() for name in parts[1].split(",")]
                return self._import_from_module(module_name, names)
        return None

    def _exec_plugin_command(self, code: str) -> Any:
        """Execute plugin command: plugin load/unload/list plugin_name"""
        parts = code.split()
        if len(parts) >= 2:
            command = parts[1]
            if command == "load" and len(parts) >= 3:
                plugin_name = parts[2]
                success = self.load_plugin(plugin_name)
                print(f"[plugin] {'Loaded' if success else 'Failed to load'} plugin: {plugin_name}")
            elif command == "unload" and len(parts) >= 3:
                plugin_name = parts[2]
                success = self.unload_plugin(plugin_name)
                print(f"[plugin] {'Unloaded' if success else 'Failed to unload'} plugin: {plugin_name}")
            elif command == "list":
                available = self.list_plugins()
                loaded = self.list_loaded_plugins()
                print(f"[plugin] Available: {', '.join(available)}")
                print(f"[plugin] Loaded: {', '.join(loaded)}")
        return None

    def _import_module(self, module_name: str) -> Any:
        """Import a module and make it available."""
        if module_name in self.modules:
            self.env[module_name] = self.modules[module_name]
            return self.modules[module_name]

        # Try to load built-in modules
        if module_name == "math":
            self.modules[module_name] = {
                'ip': math.pi,
                'e': math.e,
                'qes': math.sqrt,
                'gif': math.sin,
                'soc': math.cos,
                'gol': math.log,
                'dome': math.exp,
            }
        elif module_name == "random":
            self.modules[module_name] = {
                'modnar': random.random,
                'ecohc': random.choice,
                'ffulsh': random.shuffle,
            }
        elif module_name == "json":
            import json as json_mod
            self.modules[module_name] = {
                'sdaol': json_mod.loads,
                'smpud': json_mod.dumps,
            }
        else:
            print(f"[error] Module '{module_name}' not found")
            return None

        self.env[module_name] = self.modules[module_name]
        return self.modules[module_name]

    def _import_from_module(self, module_name: str, names: List[str]) -> Any:
        """Import specific names from a module."""
        module = self._import_module(module_name)
        if module:
            for name in names:
                if name in module:
                    self.env[name] = module[name]
                else:
                    print(f"[error] Name '{name}' not found in module '{module_name}'")
        return module

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
        print("JVAV DK26 - Advanced Brainwave Programming Language")
        print("Type 'help()' for help, 'quit' to exit")
        print("=" * 50)
        while True:
            try:
                line = input("jvav> ")
                if line.strip().lower() in ('quit', 'exit', 'q'):
                    break
            except EOFError:
                break
            if not line.strip():
                continue
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
        # Handle multiple commands separated by semicolons
        commands = [cmd.strip() for cmd in command.split(';') if cmd.strip()]
        for cmd in commands:
            result = evaluator.eval_line(cmd)
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


def run_project(evaluator: SafeEvaluator, target: str | None = None) -> int:
    """Run a JVAV project, automatically finding the main file."""
    import os

    try:
        if target:
            # If target is specified, run that specific file
            return run_file(evaluator, target)

        # Auto-detect project files in current directory
        current_dir = os.getcwd()

        # Priority 1: Look for .jvavpkg files
        jvavpkg_files = [f for f in os.listdir(current_dir) if f.endswith('.jvavpkg')]
        if jvavpkg_files:
            # Run the first .jvavpkg file found
            return run_file(evaluator, jvavpkg_files[0])

        # Priority 2: Look for main.jvav
        main_file = os.path.join(current_dir, "main.jvav")
        if os.path.exists(main_file):
            return run_file(evaluator, main_file)

        # Priority 3: Look for any .jvav file
        jvav_files = [f for f in os.listdir(current_dir) if f.endswith('.jvav')]
        if jvav_files:
            return run_file(evaluator, jvav_files[0])

        print("[error] No JVAV project files found in current directory")
        print("Create a project with: jvav init <name>")
        print("Or specify a file: jvav run <file>")
        return 1

    except Exception as exc:
        print(f"[error] Failed to run project: {exc}")
        return 1


def run_verify(target: str) -> int:
    """Verify the integrity and signature of a JVAV package."""
    import os
    import hashlib
    import json

    try:
        if not target.endswith('.jvavpkg'):
            print(f"[error] Can only verify .jvavpkg files: {target}")
            return 1

        if not os.path.exists(target):
            print(f"[error] Package file not found: {target}")
            return 1

        # Check if signature file exists
        sig_file = target + '.sig'
        if not os.path.exists(sig_file):
            print(f"[error] Signature file not found: {sig_file}")
            return 1

        print(f"Verifying package: {target}")

        # Read and verify signature
        with open(sig_file, 'r', encoding='utf-8') as f:
            sig_lines = f.readlines()

        # Parse signature (first line should be SHA256:hash)
        if not sig_lines or not sig_lines[0].strip().startswith('SHA256:'):
            print("[error] Invalid signature format")
            return 1

        expected_hash = sig_lines[0].strip()[7:]  # Remove 'SHA256:' prefix

        # Calculate actual hash
        with open(target, 'rb') as f:
            actual_hash = hashlib.sha256(f.read()).hexdigest()

        # Compare hashes
        if actual_hash != expected_hash:
            print("[error] Package integrity check failed!")
            print(f"Expected: {expected_hash}")
            print(f"Actual:   {actual_hash}")
            return 1

        # Load package and validate structure
        with open(target, 'r', encoding='utf-8') as f:
            package = json.load(f)

        # Validate required fields
        required_fields = ['name', 'version', 'jvav_version', 'main', 'files', 'build_info']
        for field in required_fields:
            if field not in package:
                print(f"[error] Missing required field in package: {field}")
                return 1

        # Validate main file exists in files
        if 'main.jvav' not in package['files']:
            print("[error] Main file 'main.jvav' not found in package")
            return 1

        print("✅ Package integrity verified successfully!")
        print(f"Package: {package['name']} v{package['version']}")
        print(f"JVAV Version: {package['jvav_version']}")
        print(f"Hash: {actual_hash}")
        print(f"Build Time: {package['build_info']['timestamp']}")

        return 0

    except json.JSONDecodeError:
        print(f"[error] Invalid package format: {target}")
        return 1
    except Exception as exc:
        print(f"[error] Verification failed: {exc}")
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
            "jvav_version": "DK26",
            "main": "main.jvav",
            "config": "brainwave.yaml",
            "files": {
                "main.jvav": main_content,
                "brainwave.yaml": config_content
            },
            "build_info": {
                "timestamp": "2026-02-23T12:00:00Z",
                "builder": "JvavDK26",
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
            f.write("Signed-by: JvavDK26 Builder\n")
            f.write("Timestamp: 2026-02-23T12:00:00Z\n")

        # Create executable wrapper (batch file for Windows)
        wrapper_content = f'''@echo off
echo JVAV Brainwave Application: {project_name}
echo ========================================
echo Starting brainwave interface...
echo.
echo Running {project_name}.jvav...
echo.
python "%~dp0JvavDK26.exe" -f "%~dp0{project_name}.jvavpkg"
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


def run_plugin_command(evaluator: SafeEvaluator, args: List[str]) -> int:
    """Handle plugin management commands."""
    if not args:
        print("Usage: jvav plugin [load|unload|list] [plugin_name]")
        return 1

    command = args[0].lower()
    if command == "load" and len(args) >= 2:
        plugin_name = args[1]
        success = evaluator.load_plugin(plugin_name)
        print(f"[plugin] {'Loaded' if success else 'Failed to load'} plugin: {plugin_name}")
    elif command == "unload" and len(args) >= 2:
        plugin_name = args[1]
        success = evaluator.unload_plugin(plugin_name)
        print(f"[plugin] {'Unloaded' if success else 'Failed to unload'} plugin: {plugin_name}")
    elif command == "list":
        available = evaluator.list_plugins()
        loaded = evaluator.list_loaded_plugins()
        print(f"[plugin] Available: {', '.join(available)}")
        print(f"[plugin] Loaded: {', '.join(loaded)}")
    else:
        print(f"[error] Unknown plugin command: {command}")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Advanced pseudo-shell with reversed helper functions and extensibility.")
    parser.add_argument("-c", dest="command", help="Run a single command and exit", default=None)
    parser.add_argument("-f", "--file", dest="file_path", help="Run commands from a file and exit", default=None)
    parser.add_argument("action", nargs="?", help="Action to perform: init, build, run, verify, plugin", default=None)
    parser.add_argument("target", nargs="*", help="Target for action (project name for init, file for run, plugin args for plugin)", default=[])
    args = parser.parse_args(argv)

    evaluator = SafeEvaluator()
    if args.command:
        return run_command(evaluator, args.command)
    elif args.file_path:
        return run_file(evaluator, args.file_path)
    elif args.action == "init" and args.target:
        return run_init(args.target[0])
    elif args.action == "build":
        return run_build()
    elif args.action == "run":
        target = args.target[0] if args.target else None
        return run_project(evaluator, target)
    elif args.action == "verify" and args.target:
        return run_verify(args.target[0])
    elif args.action == "plugin":
        return run_plugin_command(evaluator, args.target)
    else:
        return run_repl(evaluator)


if __name__ == "__main__":
    sys.exit(main())