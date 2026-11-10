---
name: install-cli-agents
description: |
  安装终端 coding agent CLI：opencode、qoder、codebuddy、mcode。当用户说"安装 opencode /
  qoder / codebuddy / mcode"、"把这些 CLI 装上"、"升级 agent CLI"时使用。
---

# Install CLI Agents

逐个执行安装命令，按退出码报告成败，不做额外校验。

## Procedure

1. 按表格逐个执行安装命令（用户点名某几个就只装那几个）：

   | agent | 安装命令 |
   | --- | --- |
   | opencode | `npm install -g @opencode/cli` |
   | qoder | `irm https://qoder.com.cn/install.ps1 \| iex` |
   | codebuddy | `npm install -g @tencent-ai/codebuddy-code` |
   | mcode | `npm install -g @minimax-ai/code` |

2. 以命令退出码判断成败。不跑 `--version`、不查 PATH、不做其他校验。
3. 汇报每个 agent 的安装结果。

## Output contract

- 一行一个 agent：成功 / 失败。
- 失败的项附上完整安装命令，告知用户可自行在终端重试。

## Failure handling

- 单个失败继续装其余的，最后统一汇报，不中途整体放弃。
- 失败后不自动重试、不自动修复（不改 npm config、不动执行策略、不提权）。
- npm 报 EACCES/EPERM → 提示用管理员终端重跑；`irm | iex` 被执行策略拦截 → 报告并请用户
  确认是否放宽；网络失败 → 报告并建议重试。
- qoder 装完的命令名是 `qoderclicn`（不是 `qoder`）；"脚本跑完但命令找不到"通常是新开的
  终端没继承 PATH，重开终端即可。

## Windows (win32) platform notes

- `irm ... | iex` 是 PowerShell 专有写法；三个 `npm install -g` 跨平台通用。
- macOS/Linux 上 qoder 的安装方式未核实，先查官方文档，不要把 `.ps1` 的 URL 直接换成
  `curl ... | bash`。
