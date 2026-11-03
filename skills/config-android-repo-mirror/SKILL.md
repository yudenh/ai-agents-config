---
name: config-android-repo-mirror
description: "Use when: configure Android/Gradle projects to replace google()/mavenCentral()/jcenter() repositories with Aliyun Maven mirrors."
---

# config-android-repo-mirror

Configure an Android/Gradle project to use Aliyun Maven repository mirrors.

## Use When

The user wants to configure, fix, or refresh Android/Gradle Maven repository mirrors, especially when they mention `build.gradle`, `repositories`, `google()`, `mavenCentral()`, `jcenter()`, or Aliyun Maven mirrors.

## Steps

1. Locate the Android/Gradle project files in the current workspace.
2. Preview the replacement with the bundled script, review the output, then execute it.
3. Run the most relevant Gradle sync/build check available for the project when practical.

`<skill-dir>` is the directory containing this SKILL.md. Pass `--target <path>` for a project outside the current workspace. The dry run writes nothing and creates no backups; execution creates a timestamped backup per changed file, verifies it before writing, and re-reads the file afterwards.

```bash
# preview: no writes, no backups
python <skill-dir>/mirror_gradle_repos.py --dry-run

# execute after reviewing the preview
python <skill-dir>/mirror_gradle_repos.py
```

## Replacement Rules

```gradle
google() -> maven { url 'https://maven.aliyun.com/repository/google' }
mavenCentral() -> maven { url 'https://maven.aliyun.com/repository/public' }
jcenter() -> maven { url 'https://maven.aliyun.com/repository/public' }
```

The script handles both Groovy and Kotlin DSL (`*.gradle.kts` uses `uri("...")` syntax); manual edits should follow the same mapping.

## Notes

- Prefer the smallest edit that satisfies the requested configuration.
- The script is idempotent: files already fully mirrored produce zero changes on re-run.
- The script skips `build/` and `.gradle/` directories, pure comment lines, and preserves indentation, trailing comments, and original line endings.
- If repositories already use the Aliyun mirror URLs, leave them unchanged.
- Preserve formatting style where possible.
