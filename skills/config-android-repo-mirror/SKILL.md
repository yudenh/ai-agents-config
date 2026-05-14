---
name: config-android-repo-mirror
description: "Use when: configure Android/Gradle projects to replace google()/mavenCentral() repositories with Aliyun Maven mirrors."
---

# config-android-repo-mirror

Configure an Android/Gradle project to use Aliyun Maven repository mirrors.

## Use When

The user wants to configure, fix, or refresh Android/Gradle Maven repository mirrors, especially when they mention `build.gradle`, `repositories`, `google()`, `mavenCentral()`, or Aliyun Maven mirrors.

## Steps

1. Locate the Android/Gradle project files in the current workspace.
2. Locate relevant `build.gradle` files that define `repositories` blocks.
3. Replace Gradle repository declarations as follows:

```gradle
google() -> maven { url 'https://maven.aliyun.com/repository/google' }
mavenCentral() -> maven { url 'https://maven.aliyun.com/repository/public' }
```

4. Preserve unrelated Gradle settings and repository entries.
5. Run the most relevant Gradle sync/build check available for the project when practical.

## Notes

- Prefer the smallest edit that satisfies the requested configuration.
- If repositories already use the Aliyun mirror URLs, leave them unchanged.
- For Kotlin DSL files (`*.gradle.kts`), use Kotlin DSL syntax instead:

```kotlin
maven { url = uri("https://maven.aliyun.com/repository/google") }
maven { url = uri("https://maven.aliyun.com/repository/public") }
```

- Preserve formatting style where possible.
