# AI Agents 配置

这个仓库用于存放通用 AI Agent 行为准则和可复用 Skills。

## 内容

- `AGENTS.md`：面向所有 AI Agent 的通用行为准则，强调先理解再编码、简单优先、外科手术式修改和目标驱动执行。
- `skills/`：面向所有 AI Agent 的可复用 Skills 配置。
- `skills/config-folder-path-color/`：生成当前工作区的 VS Code `folder-path-color` 配置。
- `skills/config-android-repo-mirror/`：为 Android/Gradle 项目配置阿里云 Maven 镜像，将 `google()`、`mavenCentral()`、`jcenter()` 仓库替换为镜像地址（附带 `mirror_gradle_repos.py` 脚本）。
- `skills/install-cli-agents/`：安装终端 coding agent CLI（opencode、qoder、codebuddy、mcode）。
- `skills/run-cli-agent-task/`：把 opencode、qoder、codebuddy、mcode 当作子智能体执行用户指定的任务。

## 文件放置

将本仓库中的配置文件同步到对应工具使用的配置目录中，统一放在通用 AI Agent 目录：

```text
~/.agents/AGENTS.md
~/.agents/skills
```

即 `AGENTS.md` 复制为 `~/.agents/AGENTS.md`，`skills/` 下的各 skill 目录复制到 `~/.agents/skills/` 下。
