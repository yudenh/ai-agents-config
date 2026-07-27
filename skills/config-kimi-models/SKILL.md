---
name: config-kimi-models
description: Filter models in a kimi config.toml file by provider rules.
allowed-tools: Bash(config-kimi-models:*) Bash(python3:*) Bash(python:*)
---

# Config Kimi Models

Filter the model list in a kimi `config.toml` file based on provider-specific rules.

## Target config

Use the path supplied by the user. If the user does not provide one, default to `~/.kimi-code/config.toml`, resolved from the current user's home directory at runtime. Do not hard-code an absolute user directory.

## Default filtering rules

| Provider   | Keep condition                                              |
| ---------- | ----------------------------------------------------------- |
| `openai`   | Model name is one of: `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini` |
| `opencode` | Model name is `big-pickle` or contains `free`               |

All other model entries are removed. Non-model sections (`[providers.*]`, `[thinking]`, etc.) are always preserved.

## Quick start

Replace `<skill-directory>` with this skill's directory. The `CONFIG` argument is optional.

```powershell
# Filter ~/.kimi-code/config.toml in-place
python "<skill-directory>\filter_models.py"

# Filter a user-specified config file in-place
python "<skill-directory>\filter_models.py" "<config-path>"

# Preview the default config without writing
python "<skill-directory>\filter_models.py" --dry-run

# Filter a specified config and write to a different file
python "<skill-directory>\filter_models.py" "<config-path>" -o "<output-path>"
```

## Remove additional models

Use `--remove` (repeatable) to remove specific model names beyond the default rules:

```powershell
# Remove gpt-5.6 and gpt-5.5-pro in addition to default filtering
python "<skill-directory>\filter_models.py" "<config-path>" --remove gpt-5.6 --remove gpt-5.5-pro
```

## Full options

```
python "<skill-directory>\filter_models.py" [CONFIG] [-o OUTPUT] [--remove MODEL] [--dry-run]
```

| Option       | Description                                      |
| ------------ | ------------------------------------------------ |
| `CONFIG`     | Config path (default: `~/.kimi-code/config.toml`) |
| `-o OUTPUT`  | Write result to OUTPUT instead of overwriting    |
| `--remove`   | Additional model name to remove (repeatable)     |
| `--dry-run`  | Print filtered output to stdout, don't write     |
