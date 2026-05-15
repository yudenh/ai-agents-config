---
name: gen-folder-path-color-config
description: "Use when: generate config for folder-path-color extension."
---

# gen-folder-path-color

Generate VS Code `folder-path-color` configuration for the current workspace.

## Use When

The user wants to generate or refresh config for the `folder-path-color` extension.

## Steps

1. List the direct child directories of the current workspace root.
2. Create one config entry for each directory:

```jsonc
{
  "path": "directory-name"
}
```

3. Write or update `.vscode/settings.json` with:

```jsonc
{
  "folder-path-color.folders": [
    {
      "path": "directory-name-1"
    },
    {
      "path": "directory-name-2"
    }
  ]
}
```

## Notes

- Include only direct child directories, not files or nested directories.
- Preserve unrelated settings in `.vscode/settings.json`.
- Replace the existing `folder-path-color.folders` value if present.
- Create `.vscode/settings.json` if it does not exist.
- Sort entries alphabetically for stable output.
