# AI Agents Config

This repository stores general behavioral guidelines and reusable skill definitions for AI coding agents.

## Contents

- `AGENTS.md`: General behavioral guidelines for AI coding agents, focused on thinking before coding, simplicity, surgical changes, and goal-driven execution.
- `skills/config-folder-path-color/`: Generates VS Code `folder-path-color` configuration for the current workspace.
- `skills/config-android-repo-mirror/`: Configures Android/Gradle projects to use Aliyun Maven mirrors instead of `google()` and `mavenCentral()`.

## File Placement

Place the configuration files from this repository into the configuration directory used by AI coding tools that support agents and skills.

The `skills` directory can be placed under `.agents` in the user's home directory. Both Codex and OpenCode can use it:

```text
~/.agents/skills
```

For Codex, place `AGENTS.md` at:

```text
~/.codex/AGENTS.md
```

For OpenCode, place `AGENTS.md` at:

```text
~/.config/opencode/AGENTS.md
```

## Principles

`AGENTS.md` is organized around four core principles proposed by Andrej Karpathy:

1. Think before coding.
2. Simplicity first.
3. Surgical changes.
4. Goal-driven execution.

These principles help reduce incorrect assumptions, over-engineering, and unrelated changes during AI-assisted coding.

## Maintenance

- Keep skill instructions concise, explicit, and actionable.
- When adding a new skill, include its trigger scenario, execution steps, and notes.
- When updating behavioral guidelines, prioritize stability and consistency.
