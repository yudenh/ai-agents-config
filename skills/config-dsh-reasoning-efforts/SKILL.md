---
name: config-dsh-reasoning-efforts
description: "Use when: patch dsh cordis.patch.yml models to fill missing input and reasoningEfforts, or user mentions dsh/cordis/思考强度/reasoningEfforts."
---

# config-dsh-reasoning-efforts

为 dsh 配置 `cordis.patch.yml` 中的大模型补全缺失的 `input` 和 `reasoningEfforts`，只补缺失项，不覆盖已有值。

## Use When

用户想补全 dsh 思考强度配置，或提到 `cordis.patch.yml`、`reasoningEfforts`、`思考强度`、`dsh 模型补全`。

## Target

- Windows: `%USERPROFILE%\.dsh\profiles\web\cordis.patch.yml`
- macOS/Linux: `~/.dsh/profiles/web/cordis.patch.yml`

文件中顶层为 YAML 数组，找到 `id: llm-pi-ai` 条目 → `config.providers` → 每个 provider 下的 `models[]`，逐个模型补全。

参考样例见本仓库 `ref/cordis.patch.yml`（已补全思考强度的目标形态）。

## Steps

1. 确保依赖可用（往返解析，保留注释、`!!js` 表达式和缩进风格）：

   ```bash
   python -c "import ruamel.yaml" || pip install ruamel.yaml
   ```

2. 先预览（不写文件、不备份），确认待修改模型列表符合预期：

   ```bash
   python <skill-dir>/patch_cordis.py --dry-run
   ```

   可用 `--target <path>` 指定非默认位置的 `cordis.patch.yml`。

3. 正式执行（脚本自动在同目录创建时间戳备份 `cordis.patch.yml.bak.YYYYMMDD-HHMMSS`，校验备份与原文件一致后才写入，写完回读校验 YAML 可解析）：

   ```bash
   python <skill-dir>/patch_cordis.py
   ```

   其中 `<skill-dir>` 是本 skill 所在目录（含 `patch_cordis.py` 的那一级）。

4. 核对脚本输出的修改模型列表符合预期即可（配置文件不在版本库中，无需 diff）。

## Rules

脚本对每个模型的补全规则（缺失或为空时才填，已有值保留原样）：

- `input` 缺失时填 `[text, image]`；已有（即使只有 `text` 一项）则保留。
- `reasoningEfforts` 缺失时按模型 `id`（大小写不敏感子串匹配）推断；已有（即使只有部分档位）则保留：
  - `id` 含 `deepseek` / `glm` / `kimi`：`low` / `high` / `max`
  - 其他模型：`low` / `medium` / `high`

## Notes

- 核心原则是补缺不覆盖：已有值一律保留，只填缺失或空的项。
- 不写 `off` 档：是否关闭思考强度走 dsh 默认行为。
- 备份是强制步骤（脚本内建），改坏会导致 agent 起不来；目标文件不存在或结构不对时脚本直接停止，不创建新文件。
