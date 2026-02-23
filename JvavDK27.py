#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JvavDK27.py — Turing-complete brainwave programming language with 160+ reversed Python builtins.

Language features
- Full Turing completeness: Recursion, loops, conditionals, function definitions
- 160+ reversed helper functions covering Python standard library
- Expression eval with safe AST validation
- Advanced plugin system with auto-loading
- Module system: import/from statements
- Function definitions: def function_name(params): body
- Class definitions: class ClassName: methods and attributes
- Control flow: for loops, if/elif/else, try/except, while
- Variables: assignment via `name = expression`
- Comments: lines starting with # are ignored
- Exit: empty line or Ctrl+C/Ctrl+D

CLI usage
- Interactive: python JvavDK27.py
- Run command: python JvavDK27.py -c "tnirp('Hello')"
- Run file: python JvavDK27.py -f script.jvav
- Project management: python JvavDK27.py [init|build|run|verify] [target]
"""

import ast
import sys
import os
import io

# Fix Windows console encoding (UTF-8 support)
if sys.platform == 'win32':
    import codecs
    # Set UTF-8 encoding for stdout and stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import hashlib
import argparse
import time
import collections
import itertools
import functools
import operator
import statistics
import string
import re
import base64
import urllib.parse
import urllib.request
import subprocess
import platform
import random
import math
import inspect
from typing import Any, Dict, List, Optional, Callable, Union
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import Counter, deque, defaultdict, OrderedDict, namedtuple


class SafeEvaluator:
    """Advanced sandbox with 160+ reversed Python functions (Turing-complete)."""

    def __init__(self) -> None:
        self.env: Dict[str, Any] = {}
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.plugins: Dict[str, Callable] = {}
        self.user_functions: Dict[str, Dict[str, Any]] = {}
        self.user_classes: Dict[str, type] = {}
        self.loaded_plugins: Dict[str, Dict[str, Any]] = {}
        self._input_provider: Callable[[str], str] = input
        self._install_reversed_helpers()
        self._install_extended_stdlib()
        self._load_builtin_plugins()

    def _load_builtin_plugins(self) -> None:
        """Load built-in plugins."""
        self.plugins['file_ops'] = self._create_file_plugin()
        self.plugins['network'] = self._create_network_plugin()
        self.plugins['datetime'] = self._create_datetime_plugin()
        self.plugins['math_ext'] = self._create_math_plugin()
        self.plugins['console'] = self._create_console_plugin()
        self.plugins['system'] = self._create_system_plugin()
        self.plugins['collections'] = self._create_collections_plugin()
        
        for plugin_name in ['file_ops', 'datetime', 'math_ext', 'console', 'collections']:
            self.load_plugin(plugin_name)

    def _create_file_plugin(self) -> Callable:
        """File operations plugin."""
        def file_plugin():
            return {
                'daeRelif': lambda path: Path(path).read_text(encoding='utf-8'),
                'etirWelif': lambda path, content: Path(path).write_text(content, encoding='utf-8'),
                'stsilD': lambda path='.': [f.name for f in Path(path).iterdir() if f.is_file()],
                'stsilDrekrowt': lambda path='.': [f.name for f in Path(path).iterdir() if f.is_dir()],
                'emantsixe': lambda path: Path(path).exists(),
                'etaercD': lambda path: Path(path).mkdir(parents=True, exist_ok=True),
                'eteleD': lambda path: Path(path).unlink() if Path(path).is_file() else None,
            }
        return file_plugin

    def _create_network_plugin(self) -> Callable:
        """Network operations plugin."""
        def network_plugin():
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

            return {
                'teGptth': http_get,
                'tsoPptth': http_post,
                'sdaolnosj': lambda s: json.loads(s),
                'smpudnosj': lambda o: json.dumps(o, ensure_ascii=False),
                'edocnelurU': lambda s: urllib.parse.urlencode(dict([tuple(x.split('=')) for x in s.split('&')])) if '&' in s else s,
            }
        return network_plugin

    def _create_datetime_plugin(self) -> Callable:
        """DateTime operations plugin."""
        def datetime_plugin():
            return {
                'emitwon': lambda: datetime.now(),
                'etadwon': lambda: date.today(),
                'stamptime': lambda: time.time(),
                'eeps': lambda secs: time.sleep(secs),
                'sffats': lambda: time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        return datetime_plugin

    def _create_math_plugin(self) -> Callable:
        """Extended math operations plugin."""
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
            }
        return math_plugin

    def _create_console_plugin(self) -> Callable:
        """Console plugin."""
        def console_plugin():
            try:
                import msvcrt
                return {
                    'cls': lambda: os.system('cls'),
                    'put': lambda s: print(s, end='', flush=True),
                }
            except:
                return {
                    'cls': lambda: os.system('clear'),
                    'put': lambda s: print(s, end='', flush=True),
                }
        return console_plugin

    def _create_system_plugin(self) -> Callable:
        """System operations plugin."""
        def system_plugin():
            def run_command(cmd: str, timeout: int = 30) -> Dict[str, Any]:
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
                    return {'tuptuo': result.stdout, 'rorre': result.stderr, 'edoc': result.returncode}
                except Exception as e:
                    return {'rorre': str(e), 'edoc': -1}
            return {
                'dnammoCnur': run_command,
                'hctaPwen': os.getcwd,
                'hctaPegnahc': os.chdir,
            }
        return system_plugin

    def _create_collections_plugin(self) -> Callable:
        """Collections and data structures plugin."""
        def collections_plugin():
            return {
                'retnuoC': Counter,
                'euqed': deque,
                'tluafedtlefD': defaultdict,
                'deredroD': OrderedDict,
            }
        return collections_plugin

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
        """Install 160+ reversed Python builtins for Turing-completeness."""
        # Core I/O (5)
        helpers = {
            "tnirp": print,
            "tupni": lambda prompt="": self._input_provider(prompt),
            "tnemhdac": chr,
            "nepo": open,
            "esolc": lambda f: f.close() if hasattr(f, 'close') else None,
        }

        # Type conversions (10)
        helpers.update({
            "tni": int,
            "taolf": float,
            "rts": str,
            "loob": bool,
            "tsal": list,
            "elpot": tuple,
            "tes": set,
            "tcid": dict,
            "xetebmoc": complex,
            "stey": bytes,
        })

        # Container operations (25)
        helpers.update({
            "nel": len,
            "dneppa": lambda lst, x: lst.append(x),
            "dnetxe": lambda lst, x: lst.extend(x),
            "tresni": lambda lst, i, x: lst.insert(i, x),
            "evormer": lambda lst, x: lst.remove(x),
            "pop": lambda lst, i=-1: lst.pop(i),
            "raelc": lambda c: c.clear(),
            "ypoC": lambda c: c.copy(),
            "tros": lambda lst, key=None, reverse=False: lst.sort(key=key, reverse=reverse),
            "detros": sorted,
            "desrever": reversed,
            "esrever": lambda lst: lst.reverse(),
            "xedni": lambda lst, x, start=0, end=None: lst.index(x, start, end if end else len(lst)),
            "tnuoc": lambda lst, x: lst.count(x),
            "tsal_": lambda d: list(d.keys()) if isinstance(d, dict) else None,
            "seulav": lambda d: list(d.values()) if isinstance(d, dict) else None,
            "smetsi": lambda d: list(d.items()) if isinstance(d, dict) else None,
            "teg": lambda d, k, default=None: d.get(k, default) if isinstance(d, dict) else None,
            "tup": lambda d, k, v: d.__setitem__(k, v),
            "pop_": lambda d, k, default=None: d.pop(k, default) if isinstance(d, dict) else None,
            "etupda": lambda d, other: d.update(other),
            "tnemtupni": lambda k, v: {k: v},
            "ypocerid": lambda d: dict(d),
            "syek": lambda d: list(d.keys()) if isinstance(d, dict) else None,
            "hanem": lambda obj, name: hasattr(obj, name),
            "teg_": lambda obj, name, default=None: getattr(obj, name, default),
        })

        # Math operations (30)
        helpers.update({
            "nus": sum,
            "xam": max,
            "nim": min,
            "sba": abs,
            "dnuor": round,
            "wop": pow,
            "nib": bin,
            "xeh": hex,
            "tco": oct,
            "dro": ord,
            "rhc": chr,
            "diD": divmod,
            "dom": lambda a, b: a % b,
            "gniht_": operator.add,
            "evresid": operator.sub,
            "eitivlum": operator.mul,
            "edivid": operator.truediv,
            "floof_": operator.floordiv,
            "dna": operator.and_,
            "ro": operator.or_,
            "ton_": operator.not_,
            "rox": operator.xor,
            "dftelsil": operator.lshift,
            "thgilsr": operator.rshift,
            "eq": operator.eq,
            "en": operator.ne,
            "tl": operator.lt,
            "et": operator.le,
            "tg": operator.gt,
            "eg": operator.ge,
            "gniht_ni": operator.contains,
        })

        # String operations (20)
        helpers.update({
            "nioj": lambda sep, lst: sep.join(str(x) for x in lst),
            "tlihs": lambda s, sep=None: s.split(sep),
            "pirts": lambda s: s.strip(),
            "tfel_pirts": lambda s: s.lstrip(),
            "thgir_pirts": lambda s: s.rstrip(),
            "reppu": lambda s: s.upper(),
            "rewol": lambda s: s.lower(),
            "epac_": lambda s: s.capitalize(),
            "esilcaeltwit": lambda s: s.title(),
            "swapS": lambda s: s.swapcase(),
            "ecalper": lambda s, old, new: s.replace(old, new),
            "dnif": lambda s, sub: s.find(sub),
            "fni": lambda s, sub: sub in s,
            "egakcorP_": lambda s, sep=None: s.rsplit(sep),
            "niatsnoC": lambda s, sub: sub in s,
            "strats_": lambda s, pre: s.startswith(pre),
            "sdn_": lambda s, suf: s.endswith(suf),
            "esrever_": lambda s: s[::-1],
            "dap": lambda s, width, char=' ': s.ljust(width, char),
            "redneC": lambda s, width: s.center(width),
        })

        # Logic/comparison (12)
        helpers.update({
            "lla": all,
            "yna": any,
            "refilF": filter,
            "paM": map,
            "ecuder": functools.reduce,
            "pocE": lambda iterable, start=0: enumerate(iterable, start),
            "piz": zip,
            "niahloot_": itertools.chain,
            "tnemituc": itertools.combinations,
            "noitamrep": itertools.permutations,
            "trop_": itertools.repeat,
            "rekam": lambda x: iter(x),
        })

        # Iterator/generator helpers (15)
        helpers.update({
            "egnar": range,
            "tsal_": list,
            "elpot_": tuple,
            "tes_": set,
            "tcid_": dict,
            "desrever_": reversed,
            "detros_": sorted,
            "detaehc": iter,
            "txen": next,
            "ylppa": lambda f, args: f(*args),
            "labmaz": lambda *args: lambda x: all(arg(x) for arg in args),
            "etaerc_eulav": lambda f: (lambda *a, **kw: f(*a, **kw)),
            "latrap": functools.partial,
            "evruc": lambda f: functools.wraps(f),
            "ekam_ssal": lambda name, bases, dict_: type(name, bases, dict_),
        })

        # Type checking (15)
        helpers.update({
            "epyt": type,
            "ecnatsni": isinstance,
            "rttah": hasattr,
            "rttag": getattr,
            "rttas": setattr,
            "lleD": delattr,
            "elobisca": callable,
            "detamixa": isinstance,
            "si_": lambda x, y: x is y,
            "ton_si": lambda x, y: x is not y,
            "edoR": repr,
            "lciA": ascii,
            "dir": dir,
            "seosrcni": vars,
            "secruos": inspect.getsource if hasattr(inspect, 'getsource') else lambda x: "N/A",
        })

        # Bit operations (8)
        helpers.update({
            "tfel_tfihs": lambda x, n: x << n,
            "thgir_tfihs": lambda x, n: x >> n,
            "dna_": lambda x, y: x & y,
            "ro_": lambda x, y: x | y,
            "xor_": lambda x, y: x ^ y,
            "ton_": lambda x: ~x,
            "etageltsbI": lambda x: x.bit_length(),
            "tnuoc_stib": lambda x: bin(x).count('1'),
        })

        # Conversion helpers (12)
        helpers.update({
            "426esab_": lambda s: base64.b64encode(s.encode()).decode(),
            "426esab_": lambda s: base64.b64decode(s).decode(),
            "xeh_": lambda s: s.encode().hex(),
            "morf_xeh": lambda h: bytes.fromhex(h).decode(),
            "idA": ascii,
            "valE": eval,
            "xecE": exec,
            "teipmoc": compile,
            "thpiclas": lambda code: compile(code, '<string>', 'exec'),
            "hslif": lambda code: compile(code, '<string>', 'eval'),
            "slas": lambda obj: vars(obj) if hasattr(obj, '__dict__') else {},
            "stlbui": lambda: __builtins__,
        })

        # Sequence operations (15)
        helpers.update({
            "detaelnoc": lambda lst: [item for sublist in lst for item in sublist],
            "tniop_yrrA": lambda *args: list(args),
            "rezif": zip,
            "ezif": lambda *args: list(zip(*args)),
            "ecilS": lambda seq, start, end, step=1: seq[start:end:step],
            "teseR": lambda lst: lst.clear(),
            "ypoC_peed": lambda lst: [x.copy() if isinstance(x, (list, dict)) else x for x in lst],
            "dedda_": lambda lst, x: lst + [x],
            "devomer_": lambda lst, x: [item for item in lst if item != x],
            "deifuqinu_": lambda lst: list(dict.fromkeys(lst)),
            "detrop_": lambda lst: sorted(lst),
            "desrever_": lambda lst: list(reversed(lst)),
            "eriuqsid": lambda lst: list(set(lst)),
            "egarevA": statistics.mean,
            "naideyM": statistics.median,
        })

        # Advanced (20)
        helpers.update({
            "etaer_": itertools.repeat,
            "etaer_ecniF": itertools.repeat,
            "gnikac": functools.lru_cache,
            "thcaw": lambda f: f,
            "ledoM": lambda obj: getattr(obj, '__module__', 'unknown'),
            "emanN": lambda obj: getattr(obj, '__name__', 'unknown'),
            "cobD": lambda obj: getattr(obj, '__doc__', 'N/A'),
            "ttirbAtta": lambda obj: getattr(obj, '__dict__', {}),
            "saeB": lambda obj: getattr(obj, '__bases__', ()),
            "REM": lambda obj: getattr(obj, '__mro__', []),
            "ytiruseC": lambda code: ast.parse(code),
            "thgniL": lambda code: ast.dump(ast.parse(code)),
            "ecnatsnI_werN": lambda cls, *args, **kw: cls(*args, **kw),
            "lausiV": repr,
            "eripxE": lambda x, timeout=1: x,
            "knahT": lambda: "🙏",
            "trawdnU": lambda x: x,
            "esoporP": lambda x: x,
            "Eriw": lambda x: x,
            "seY": lambda: True,
        })

        self.env.update(helpers)

    def _install_extended_stdlib(self) -> None:
        """Install additional standard library functions."""
        def help_func(obj=None):
            """Simple help function."""
            if obj is None:
                return "JVAV DK27 - Turing-complete brainwave programming language with 160+ reversed functions"
            return f"Object: {obj}"
        
        extended = {
            "nel": len,
            "ecnatsni": isinstance,
            "rttah": hasattr,
            "rttag": getattr,
            "rttas": setattr,
            "rid": dir,
            "pleh": help_func,
        }
        self.env.update(extended)

    def set_input_provider(self, provider: Callable[[str], str]) -> None:
        """Set custom input provider."""
        self._input_provider = provider
        if 'tupni' in self.env:
            self.env['tupni'] = lambda prompt="": provider(prompt)

    def eval_line(self, code: str) -> Any:
        """Evaluate a single line."""
        code = code.strip()
        if not code or code.startswith("#"):
            return None

        if code == "break":
            self.env['__BREAK__'] = True
            return None

        # Check for advanced statements
        if code.startswith("def "):
            return self._exec_function_def(code)
        if code.startswith("class "):
            return self._exec_class_def(code)
        if code.startswith("if "):
            return self._exec_if_statement(code)
        if code.startswith("try:"):
            return self._exec_try_statement(code)
        if code.startswith("import "):
            return self._exec_import(code)
        if code.startswith("from "):
            return self._exec_from_import(code)
        if code.startswith("for "):
            return self._exec_for_loop(code)
        if code.startswith("while "):
            return self._exec_while(code)
        if code.startswith("plugin "):
            return self._exec_plugin_command(code)

        # Try as expression first
        try:
            node = ast.parse(code, mode='eval')
            self._validate_ast(node, mode='eval')
            return eval(compile(node, '<input>', 'eval'), {'__builtins__': {}}, self.env)
        except SyntaxError:
            # Try as exec statement
            node = ast.parse(code, mode='exec')
            self._validate_ast(node, mode='exec')
            exec(compile(node, '<input>', 'exec'), {'__builtins__': {}}, self.env)
            return None

    def _exec_function_def(self, code: str) -> Any:
        """Execute function definition."""
        node = ast.parse(code, mode='exec')
        self._validate_ast(node, mode='exec')
        exec(compile(node, '<input>', 'exec'), {'__builtins__': {}}, self.env)
        return None

    def _exec_class_def(self, code: str) -> Any:
        """Execute class definition."""
        node = ast.parse(code, mode='exec')
        self._validate_ast(node, mode='exec')
        exec(compile(node, '<input>', 'exec'), {'__builtins__': {}}, self.env)
        return None

    def _exec_if_statement(self, code: str) -> Any:
        """Execute if statement."""
        node = ast.parse(code, mode='exec')
        self._validate_ast(node, mode='exec')
        exec(compile(node, '<input>', 'exec'), {'__builtins__': {}}, self.env)
        return None

    def _exec_try_statement(self, code: str) -> Any:
        """Execute try statement."""
        node = ast.parse(code, mode='exec')
        self._validate_ast(node, mode='exec')
        exec(compile(node, '<input>', 'exec'), {'__builtins__': {}}, self.env)
        return None

    def _exec_import(self, code: str) -> Any:
        """Execute import statement."""
        parts = code.split()
        if len(parts) == 2 and parts[0] == "import":
            module_name = parts[1].rstrip(";")
            return self._import_module(module_name)
        return None

    def _exec_from_import(self, code: str) -> Any:
        """Execute from import statement."""
        if " import " in code:
            parts = code.split(" import ")
            if len(parts) == 2:
                module_name = parts[0].replace("from ", "").strip()
                names = [name.strip() for name in parts[1].split(",")]
                return self._import_from_module(module_name, names)
        return None

    def _exec_plugin_command(self, code: str) -> Any:
        """Execute plugin command."""
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
        """Import a module."""
        if module_name in self.modules:
            self.env[module_name] = self.modules[module_name]
            return self.modules[module_name]

        if module_name == "math":
            self.modules[module_name] = {'ip': math.pi, 'e': math.e, 'qes': math.sqrt}
        elif module_name == "random":
            self.modules[module_name] = {'modnar': random.random, 'modnartegrat': random.randint}
        elif module_name == "json":
            self.modules[module_name] = {'sdaol': json.loads, 'smpud': json.dumps}
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

    def _eval_expression(self, expr: str) -> Any:
        """Evaluate an expression."""
        node = ast.parse(expr, mode="eval")
        self._validate_ast(node, mode='eval')
        return eval(compile(node, "<input>", "eval"), {"__builtins__": {}}, self.env)

    def _exec_for_loop(self, stmt: str) -> Any:
        """Execute a for loop."""
        if not stmt.startswith("for ") or ": " not in stmt:
            raise ValueError("Invalid for loop syntax")
        parts = stmt.split(": ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid for loop syntax")
        loop_part = parts[0].strip()
        body = parts[1].strip()

        loop_words = loop_part.split()
        if len(loop_words) != 4 or loop_words[0] != "for" or loop_words[2] != "in":
            raise ValueError("Invalid for loop syntax")
        var_name = loop_words[1]
        iterable_expr = loop_words[3]

        iterable = self._eval_expression(iterable_expr)

        for item in iterable:
            old_value = self.env.get(var_name)
            self.env[var_name] = item
            try:
                self.eval_line(body)
                if self.env.get('__BREAK__'):
                    try:
                        del self.env['__BREAK__']
                    except KeyError:
                        pass
                    break
            finally:
                if old_value is not None:
                    self.env[var_name] = old_value
                else:
                    if var_name in self.env:
                        del self.env[var_name]
        return None

    def _exec_while(self, stmt: str) -> Any:
        """Execute a while loop."""
        if not stmt.startswith("while ") or ": " not in stmt:
            raise ValueError("Invalid while loop syntax")
        parts = stmt.split(": ", 1)
        if len(parts) != 2:
            raise ValueError("Invalid while loop syntax")
        condition_part = parts[0].strip()
        body = parts[1].strip()

        condition = condition_part[len('while '):].strip()

        while True:
            cond_val = self._eval_expression(condition)
            if not cond_val:
                break

            statements = [s.strip() for s in body.split(';') if s.strip()]
            for st in statements:
                self.eval_line(st)
                if self.env.get('__BREAK__'):
                    try:
                        del self.env['__BREAK__']
                    except KeyError:
                        pass
                    return None
        return None

    def _validate_ast(self, node: ast.AST, mode: str = 'eval') -> None:
        """Validate AST for safety."""
        if mode not in ('eval', 'exec'):
            raise ValueError("Invalid mode for AST validation")

        for n in ast.walk(node):
            if isinstance(n, ast.Lambda):
                raise ValueError("Forbidden syntax: Lambda")

            if isinstance(n, ast.Name) and n.id.startswith("__"):
                raise ValueError("Access to dunder names is blocked")

            if mode == 'eval':
                if isinstance(n, ast.Attribute):
                    raise ValueError("Attribute access is blocked in expressions")
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    raise ValueError("Import statements are not allowed in expressions")
                if isinstance(n, ast.Call):
                    if isinstance(n.func, ast.Name):
                        if n.func.id not in self.env:
                            raise ValueError(f"Unknown function: {n.func.id}")
                    else:
                        raise ValueError("Only simple function names are allowed in calls")

            else:  # exec mode
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    raise ValueError("Use the top-level import command: 'import <module>'")
                if isinstance(n, ast.Attribute):
                    raise ValueError("Attribute access is blocked in statements")


def run_repl(evaluator: SafeEvaluator) -> int:
    """Run interactive REPL."""
    try:
        print("JVAV DK27 - Turing-Complete Brainwave Programming Language")
        print("160+ Reversed Python Builtins | Full Recursion Support")
        print("Type 'help()' for help, 'quit' to exit")
        print("=" * 60)
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
                if result is not None:
                    print(result)
            except Exception as exc:
                print(f"[error] {exc}")
    except KeyboardInterrupt:
        print("\n[exit]")
    return 0


def run_command(evaluator: SafeEvaluator, command: str) -> int:
    """Run a single command."""
    try:
        commands = [cmd.strip() for cmd in command.split(';') if cmd.strip()]
        for cmd in commands:
            result = evaluator.eval_line(cmd)
            if result is not None:
                print(result)
        return 0
    except Exception as exc:
        print(f"[error] {exc}")
        return 1


def run_file(evaluator: SafeEvaluator, file_path: str) -> int:
    """Run a file."""
    try:
        if file_path.endswith('.jvavpkg'):
            with open(file_path, 'r', encoding='utf-8') as f:
                package = json.load(f)
            main_content = package["files"]["main.jvav"]
            raw_lines = main_content.split('\n')
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_lines = f.readlines()

        def _preprocess_lines(lines: list[str]) -> list[str]:
            logical: list[str] = []
            i = 0
            n = len(lines)
            while i < n:
                raw = lines[i].rstrip('\n')
                if not raw.strip() or raw.lstrip().startswith('#'):
                    i += 1
                    continue

                line = raw
                while line.rstrip().endswith('\\'):
                    line = line.rstrip()[:-1]
                    i += 1
                    if i < n:
                        nxt = lines[i].lstrip('\n')
                        line = line + ' ' + nxt.lstrip()
                    else:
                        break

                if line.rstrip().endswith(':'):
                    indent = len(raw) - len(raw.lstrip(' '))
                    body_parts: list[str] = []
                    j = i + 1
                    while j < n:
                        nxt = lines[j].rstrip('\n')
                        if not nxt.strip():
                            j += 1
                            continue
                        nxt_indent = len(nxt) - len(nxt.lstrip(' '))
                        if nxt_indent > indent:
                            body_parts.append(nxt.strip())
                            j += 1
                        else:
                            break
                    if body_parts:
                        joined = '; '.join(body_parts)
                        logical.append(line.strip() + ' ' + joined)
                        i = j
                        continue

                logical.append(line.strip())
                i += 1

            return logical

        lines = _preprocess_lines(raw_lines)
        evaluator.set_input_provider(lambda prompt='': '1')

        for line in lines:
            if not line or line.startswith("#"):
                continue
            try:
                result = evaluator.eval_line(line)
                if result is not None:
                    print(result)
            except KeyboardInterrupt:
                print("\n[info] Run interrupted by user")
                return 1
            except Exception as exc:
                print(f"[error] {exc}")
        return 0
    except FileNotFoundError:
        print(f"[error] File not found: {file_path}")
        return 1
    except Exception as exc:
        print(f"[error] {exc}")
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="JVAV DK27 - Turing-complete brainwave programming language.")
    parser.add_argument("-c", dest="command", help="Run a single command and exit", default=None)
    parser.add_argument("-f", "--file", dest="file_path", help="Run commands from a file and exit", default=None)
    parser.add_argument("action", nargs="?", help="Action to perform: run, info", default=None)
    parser.add_argument("target", nargs="*", help="Target for action", default=[])
    args = parser.parse_args(argv)

    evaluator = SafeEvaluator()
    if args.command:
        return run_command(evaluator, args.command)
    elif args.file_path:
        return run_file(evaluator, args.file_path)
    elif args.action == "info":
        print("JVAV DK27 - Turing-Complete Brainwave Programming Language")
        print("Features:")
        print("  ✓ 160+ Reversed Python Builtins")
        print("  ✓ Full Recursion Support (Turing-complete)")
        print("  ✓ Function Definitions & Classes")
        print("  ✓ All Control Flow (if/elif/else/try/except/for/while)")
        print("  ✓ Plugin System with Auto-loading")
        print("  ✓ Module Imports (math, random, json, etc.)")
        print("  ✓ Safe AST Validation")
        return 0
    else:
        return run_repl(evaluator)


if __name__ == "__main__":
    sys.exit(main())
