# JVAV — 脑波原生开发平台（Real Project）

一个纯三剑客（HTML/CSS/JS）构成的现代站点，用于发布 JVAV 真实项目的下载、版本与文档信息。页面以居中横幅、充足留白和清爽排版呈现，重点强调可验证的发布链路。

> **JVAV DK 27 现已定位为「Turing 完备脑波编程语言」**：所有 `.jvav` 脚本由运行时解释执行，提供 160+ 倒序函数库、完整控制流、递归函数支持。v5 版本完全修复了 REPL 函数作用域问题，完整支持递归算法。

## 快速开始
1) 打开 `index.html` 即可浏览主页。
2) 访问 `downloads/` 获取最新 JVAV DK 27 v5 解释器，直接运行体验脑波原生开发。
3) 查看 `versions.html`、`changelog.html`、`about.html`、`help.html` 获取版本、更新、理念与上手信息。
4) 参考 `examples/` 目录下的示例程序快速上手。

## 结构
- `index.html` 主页
- `downloads/` 下载页（含最新 `jvav_dk27.exe`）
- `versions.html` 版本中心（DK25/DK26/DK27）
- `changelog.html` 更新日志（v1-v5 历史）
- `about.html` 项目简介
- `help.html` 快速上手
- `assets/` 样式与 Logo
- `examples/` 示例程序库
- `src/` 解释器源码
- `tests/` 测试文件

## 发布校验
- 当前发行：JVAV DK 27 v6
- 状态：✅ Production Ready · Turing 完备脑波编程语言
- SHA256: `1D29F00D214C8A744623BCDAA83DE1FB4997601EA351427F597095E81EFDCAFD`
- 功能：160+ 倒序函数、完整递归、所有控制流、REPL 交互
- 测试：8/8 单元测试通过

## 包管理器
`jvavpkg.exe`（`src/jvavpkg.py`）—— 基于 GitHub 仓库文件的 JVAV 包管理器。

- 一包一仓库，Git tag = 版本；仓库文件直存，>100MB 资产走 `jvavpkg.links` 外链（强制 SHA256）
- 命令：`info` / `install` / `uninstall` / `list` / `update`
- 支持依赖解析、版本约束、循环与冲突检测；安装到全局 `~/.jvav/packages/` 或项目 `.jvav/packages/`
- 测试：11/11 包管理测试通过（`python tests\test_jvavpkg.py`）
