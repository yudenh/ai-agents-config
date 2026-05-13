# AI Agents Config

This repository stores general behavioral guidelines and reusable skill definitions for AI coding agents.

## Contents

- `AGENTS.md`: General behavioral guidelines for AI coding agents, focused on thinking before coding, simplicity, surgical changes, and goal-driven execution.
- `skills/gen-sln-folder-path-color-config/`: Generates VS Code `folder-path-color` extension configuration from projects in the current `.sln` solution.
- `skills/gen-src-folder-path-color-config/`: Generates VS Code `folder-path-color` extension configuration from direct child directories under `src` in the current workspace.

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

## Skill Usage

When the user wants to generate or refresh VS Code `folder-path-color` configuration, the agent can choose the appropriate skill:

- Use `gen-sln-folder-path-color-config` when the workspace contains a `.sln` solution.
- Use `gen-src-folder-path-color-config` when modules are organized as direct child directories under `src`.

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
