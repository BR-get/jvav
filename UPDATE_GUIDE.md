# JVAV 更新 / 发布指南

本文档描述修改解释器或发布新版（version bump）时必须执行的完整流程，以及所有需要同步修改的文件、哈希和校验命令。**版本信息没有单一源头**，散落在多个文件中，遗漏任何一处都会造成页面与产物不一致。

> 当前版本：DK27 v6 · 发布日期 2026-08-08 · 产物 `downloads/jvav_dk27.exe`

## 1. 修改解释器代码

唯一在运行的源码是 `src/JvavDK27.py`（DK27 v5）。`src/JvavDK25.py`、`src/JvavDK26.py` 是遗留版本，**不要改动**。

关键代码位置：
- 倒序内置函数表：`SafeEvaluator._install_reversed_helpers()`（新增函数在这里加）
- 倒序关键字映射：`run_file` 内的 `_KW_MAP`（`JvavDK27.py:824`），当前支持 `esle/elihw/rof/yrt/tpecxe/fi/ni/ton/nruter`（对应 `else/while/for/except/if/in/not/return`）
- CLI 入口：`main()`（`JvavDK27.py:888`），仅支持 `-c`、`-f`、`info`；其余输入进入 REPL

若新增了 `import`，必须同步更新 `jvav_dk27.spec` 的 `hiddenimports` 列表（PyInstaller 依赖它），并确认 `assets/logo.ico` 仍在 `datas` 中。

## 2. 修改后必须通过的验证

```powershell
python tests\test_repl_function.py                          # 单元测试（无 pytest，assert 自测）
python src\JvavDK27.py -c "tnirp('hi')"                     # 单行命令
python src\JvavDK27.py info                                 # 自检
# 逐个运行所有示例，全部必须退出码 0：
Get-ChildItem examples -Filter *.jvav | % { python src\JvavDK27.py -f $_.FullName }
```

注意：示例和测试文件使用倒序内置函数（`tnirp/nel/egnar/rts/tcid`）和倒序关键字（`fi/esle/rof/elihw/yrt/tpecxe/ni/ton`），不要改成 Python 原名。

## 3. 构建与哈希

```powershell
python -m PyInstaller jvav_dk27.spec --clean --noconfirm
Copy-Item dist\jvav_dk27.exe downloads\jvav_dk27.exe -Force
(Get-FileHash downloads\jvav_dk27.exe -Algorithm SHA256).Hash
```

`build/` 和 `dist/` 已 gitignore，**不要提交**；只提交 `downloads/jvav_dk27.exe`。

当前产物的实际哈希（用于核对文档是否过期）：
- `downloads/jvav_dk27.exe` → `EB2A09C9F5497FD95EDCE23E0CDE12D567E2214146FA549BFB36E24E2372CCE8`（与文档一致 ✓）
- `downloads/jvav_dk26.exe` → `031821EEE4DABF1BF9BFA7F4273577096E9AED9352CBEB5B422825E8B8495380`（文档写的是 `519A1288...`，两者不符，见第 5 节）

## 4. 发布时必须同步修改的文件清单

按从上到下的顺序逐一核对，任何版本号 / 日期 / SHA256 / 测试数变化都要改：

| 文件 | 需要改的内容 | 位置 |
|---|---|---|
| `src/JvavDK27.py` | 代码逻辑、倒序函数/关键字表 | — |
| `jvav_dk27.spec` | 新增 import 时更新 `hiddenimports` | — |
| `README.md` | SHA256、版本、发布日期、测试数 | L26-29 |
| `src/verify_production_status.py` | `version`、`release_date`、`sha256`、`JvavDK27.py` 行数、`test_results` | L10-11、L71、L76、L101-107 |
| `src/report.py` | SHA256、版本、日期、文件大小 | L19、L27、L72-78 |
| `index.html` | banner 日期、最新发布节 | L28、L63-64 |
| `downloads/index.html` | DK27 行：SHA256、日期、文件大小 | L30、L39-40 |
| `versions.html` | DK27 发布日期 | L32 |
| `changelog.html` | 顶部最新版本条目（含测试数） | L29-38 |
| `help.html` | banner 版本、FAQ 中的 SHA256、安装验证节 SHA256 | L24、L42、L320、L376 |
| `about.html` | 版本与特性描述 | L38 |
| `jvav27v5.md` | 特性描述（版本无关，按需） | — |
| `downloads/archive/index.html` | 仅当把 DK27 归档进 archive 时 | — |
| `downloads/jvav_dk27.exe` | 新构建的二进制 | — |

## 5. 已解决的历史不一致

v6（2026-08-08）发布时已同步修复：测试数（10/10→5/5）、发布日期、文件大小（9.1→8.7 MB）、DK26 哈希（`519A1288...`→`031821EE...`，与 `downloads/jvav_dk26.exe` 实际值一致）、插件数（6→7）、GBK 控制台编码（`report.py`/`verify_production_status.py`/`PROJECT_SUMMARY.py` 已加入 UTF-8 重包裹）。后续改动注意保持第 4 节清单中各文件的数值一致即可。

## 6. 完整发布流程（checklist）

1. 在 `src/JvavDK27.py` 完成代码修改
2. 跑第 2 节全部验证（测试 + 全部示例）
3. 在 `changelog.html` 顶部新增版本条目
4. 按第 3 节重新构建 exe 并计算新 SHA256
5. 按第 4 节清单同步更新所有文档中的版本号 / 日期 / 哈希 / 测试数 / 文件大小
6. 运行 `python src\verify_production_status.py` 与 `python src\report.py` 核对输出（这两个脚本及 `examples/PROJECT_SUMMARY.py` 自带 UTF-8 重包裹，GBK 控制台可直接运行）
7. 提交变更（只提交源码、spec、文档与 `downloads/*.exe`，不提交 `build/`、`dist/`）
