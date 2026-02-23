# JVAV — 脑波原生开发平台（Real Project）

一个纯三剑客（HTML/CSS/JS）构成的现代站点，用于发布 JVAV 真实项目的下载、版本与文档信息。页面以居中横幅、充足留白和清爽排版呈现，重点强调可验证的发布链路。

## 快速开始
1) 打开 `index.html` 即可浏览主页。
2) 访问 `downloads/` 获取 JVAV DK 25 安装包，并按页内指引校验 SHA256。
3) 查看 `versions.html`、`changelog.html`、`about.html`、`help.html` 获取版本、更新、理念与上手信息。

## 结构
- `index.html` 主页
- `downloads/` 下载页与存档页（含 `jvav.exe`）
- `versions.html` 版本中心（DK/SE）
- `changelog.html` 更新日志
- `about.html` 项目简介
- `help.html` 快速上手
- `assets/` 样式与 Logo

## 发布校验
- 当前发行：JVAV DK 25
- SHA256：C93DD534F13D618A7112BA3C201AF422C3F58FD92CF435EC13D7849D4FAC4891
- 校验命令：`certutil -hashfile jvav.exe SHA256`
