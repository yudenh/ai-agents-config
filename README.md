# AI Agents 配置

这个仓库用于存放通用 AI Agent 行为准则、可复用 Skills，以及 OpenCode/Kilo Agents 配置。

## 内容

- `AGENTS.md`：面向所有 AI Agent 的通用行为准则，强调先理解再编码、简单优先、外科手术式修改和目标驱动执行。
- `agents/`：OpenCode/Kilo Markdown Agent 配置源文件。
- `.kilo/agent/`：Kilo 可直接加载的 Agent 配置。
- `skills/`：面向所有 AI Agent 的可复用 Skills 配置。
- `skills/config-folder-path-color/`：生成当前工作区的 VS Code `folder-path-color` 配置。
- `skills/config-android-repo-mirror/`：为 Android/Gradle 项目配置阿里云 Maven 镜像，替换 `google()` 和 `mavenCentral()` 仓库。

## 依赖

`agents/document-processor.md` 依赖以下两个命令行工具：

- `office-tools`：用于文档格式转换、DOCX/PDF 图片水印、PDF 合并和 PDF 渲染等批处理任务。项目地址：https://github.com/yudenh/office-tools-cli
- `officecli`：用于 DOCX/PPTX/XLSX 读取、校验、结构化编辑、插入图片和细粒度格式调整。项目地址：https://github.com/iOfficeAI/OfficeCLI

## 文件放置

将本仓库中的配置文件同步到对应工具使用的配置目录中。

Agents 可放在 OpenCode 或 Kilo 全局配置目录：

```text
~/.config/opencode/agents
~/.config/kilo/agents
```

Skills 放在通用 AI Agent skills 目录：

```text
~/.agents/skills
```

`AGENTS.md` 可按所用 AI Agent 的约定放置；OpenCode 全局配置目录为：

```text
~/.config/opencode/AGENTS.md
```

## 行为准则

`AGENTS.md` 基于 Andrej Karpathy 提出的四条核心准则整理，定义了以下原则：

1. 先思考再编码。
2. 简单优先。
3. 外科手术式修改。
4. 目标驱动执行。

这些原则用于减少 AI Agent 执行过程中的误判、过度设计和无关改动。

## 维护建议

- 技能说明应保持简洁、明确、可执行。
- 新增技能时，应包含触发场景、执行步骤和注意事项。
- 修改行为准则时，应优先保持稳定性和一致性。
