# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['JvavDK27.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/logo.ico', 'assets')],
    hiddenimports=['urllib', 'urllib.request', 'urllib.parse', 'subprocess', 'json', 'datetime', 'math', 'random', 'pathlib', 'collections', 'itertools', 'functools', 'operator', 'statistics', 'string', 're', 'base64', 'hashlib', 'argparse', 'time', 'platform', 'inspect'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jvav_dk27',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\logo.ico',
)
