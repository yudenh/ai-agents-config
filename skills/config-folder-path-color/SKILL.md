---
name: config-folder-path-color
description: "Use when: generate VS Code folder-path-color config for the current workspace."
---

# config-folder-path-color

Generate VS Code `folder-path-color` configuration for the current workspace.

## Use When

The user wants to generate or refresh `folder-path-color` settings for the current workspace.

## Directory Selection

Choose the directory list in this priority order:

1. If the workspace root contains a `.sln` file, extract project names from the solution file and use them as the directory list.
2. If the workspace root contains a `src` folder, use the direct child directories under `src`.
3. Otherwise, use the direct child directories of the workspace root.

When using the workspace root, exclude `dist`, `bin`, `obj`, `node_modules`, and any hidden directory whose name starts with `.`.

## Steps

1. Build the directory list using the priority rules above.
2. Sort entries alphabetically for stable output.
3. Write or update `.vscode/settings.json` with `folder-path-color.folders`.
4. Preserve unrelated settings and replace only the `folder-path-color.folders` value.

## Notes

- Create `.vscode/settings.json` if it does not exist.
- Use paths relative to the workspace root.
- Keep one entry per selected directory.
