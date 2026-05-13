---
name: gen-sln-folder-path-color-config
description: "Use when: generate config for folder-path-color extension from the current solution."
---

# gen-sln-folder-path-color-config

Generate VS Code `folder-path-color` configuration for the current solution.

## Use When

The user wants to generate or refresh config for the `folder-path-color` extension based on projects in the current solution.

## Steps

1. Extract the project name list from the `.sln` file in the current solution root.
2. Create one config entry for each project name:

```jsonc
{
  "path": "project-name"
}
```

3. Write or update `.vscode/settings.json` with:

```jsonc
{
  "folder-path-color.folders": [
    {
      "path": "project-name-1"
    },
    {
      "path": "project-name-2"
    }
  ]
}
```

## Notes

- Include only projects listed in the solution file.
- Preserve unrelated settings in `.vscode/settings.json`.
- Replace the existing `folder-path-color.folders` value if present.
- Create `.vscode/settings.json` if it does not exist.
- Sort entries alphabetically for stable output.
