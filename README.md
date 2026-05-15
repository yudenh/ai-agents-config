# AI Agents 配置

这个仓库用于存放 AI 编码代理的通用行为准则和可复用技能配置。

## 内容

- `AGENTS.md`：面向 AI 编码代理的通用行为准则，强调先理解再编码、简单优先、外科手术式修改和目标驱动执行。
- `skills/config-folder-path-color/`：生成当前工作区的 VS Code `folder-path-color` 配置。
- `skills/config-android-repo-mirror/`：为 Android/Gradle 项目配置阿里云 Maven 镜像，替换 `google()` 和 `mavenCentral()` 仓库。

## 文件放置

将本仓库中的配置文件放到支持 agents 和 skills 的 AI 编码工具配置目录中。

`skills` 目录可以放入用户主目录下的 `.agents` 目录中，Codex 和 OpenCode 均可使用：

```text
~/.agents/skills
```

对于 Codex，将 `AGENTS.md` 放在：

```text
~/.codex/AGENTS.md
```

对于 OpenCode，将 `AGENTS.md` 放在：

```text
~/.config/opencode/AGENTS.md
```

## 行为准则

`AGENTS.md` 基于 Andrej Karpathy 提出的四条核心准则整理，定义了以下原则：

1. 先思考再编码。
2. 简单优先。
3. 外科手术式修改。
4. 目标驱动执行。

这些原则用于减少 AI 编码过程中的误判、过度设计和无关改动。

## 维护建议

- 技能说明应保持简洁、明确、可执行。
- 新增技能时，应包含触发场景、执行步骤和注意事项。
- 修改行为准则时，应优先保持稳定性和一致性。
