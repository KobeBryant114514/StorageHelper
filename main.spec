# -*- mode: python ; coding: utf-8 -*-
import fnmatch
from PyInstaller.utils.hooks import collect_dynamic_libs

EXCLUDE_DLLS = [
    "api-ms-win-crt-conio-l1-1-0.dll",
    "api-ms-win-crt-convert-l1-1-0.dll",
    "api-ms-win-crt-environment-l1-1-0",
    "api-ms-win-crt-filesystem-l1-1-0.dll",
    "api-ms-win-crt-heap-l1-1-0.dll",
    "api-ms-win-crt-locale-l1-1-0.dll",
    "api-ms-win-crt-math-l1-1-0.dll",
    "api-ms-win-crt-process-l1-1-0.dll",
    "api-ms-win-crt-runtime-l1-1-0.dll",
    "api-ms-win-crt-stdio-l1-1-0.dll",
    "api-ms-win-crt-string-l1-1-0.dll",
    "api-ms-win-crt-time-l1-1-0.dll",
    "api-ms-win-crt-utility-l1-1-0.dll",
]


def _collect_extensions(modules):
    result = []
    for m in modules:
        result += collect_dynamic_libs(m, search_patterns=["*.pyd", "*.so"])
    return result


def _fix_binaries(binaries):
    binaries = [
        b
        for b in binaries
        if not any(fnmatch.fnmatch(b[0], pat) for pat in EXCLUDE_DLLS)
    ]
    return binaries


a = Analysis(
    ["main.py"],
    pathex=["."],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    binaries=_collect_extensions(["rapidnbt", "leveldb"]),
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "email",
        "random",
        "logging",
        "urllib",
        "socket",
        "base64",
        "selectors",
        "subprocess",
        "textwrap",
        "tarfile",
        "argparse",
        "py_compile",
        "calendar",
        "copy",
        "csv",
        "datetime",
        "dataclasses",
        "bz2",
        "gettext",
        "getopt",
        "pickle",
        "lzma",
        "quopri",
        "string",
        "stringprep",
        "tracemalloc",
        "threading",
        "inspect",
        "ast",
        "token",
        "tokenize",
        "unicodedata",
        "_socket",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
    optimize=2,
)

a.binaries = _fix_binaries(a.binaries)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="StorageHelper",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon="assets/icon.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
