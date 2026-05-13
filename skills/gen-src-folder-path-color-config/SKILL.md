---
name: gen-src-folder-path-color-config
description: "Use when: generate config for folder-path-color extension from direct child directories of src."
---

# gen-src-folder-path-color-config

Generate VS Code `folder-path-color` configuration for direct child directories of `src` in the current workspace.

## Use When

The user wants to generate or refresh config for the `folder-path-color` extension based on direct child directories of `src` in the current workspace.

## Steps

1. List the direct child directories of `src` in the current workspace root.
2. Create one config entry for each directory:

```jsonc
{
  "path": "src/directory-name"
}
```

3. Write or update `.vscode/settings.json` with:

```jsonc
{
  "folder-path-color.folders": [
    {
      "path": "src/directory-name-1"
    },
    {
      "path": "src/directory-name-2"
    }
  ]
}
```

## Notes

- Include only direct child directories under `src`, not files or nested directories.
- Use paths relative to the workspace root, prefixed with `src/`.
- Preserve unrelated settings in `.vscode/settings.json`.
- Replace the existing `folder-path-color.folders` value if present.
- Create `.vscode/settings.json` if it does not exist.
- Sort entries alphabetically for stable output.
