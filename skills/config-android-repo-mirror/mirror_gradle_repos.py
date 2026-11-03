#!/usr/bin/env python3
"""把 Gradle 构建脚本中的 google()/mavenCentral()/jcenter() 替换为阿里云 Maven 镜像。

替换规则（与 SKILL.md 一致）:

- google()      -> maven { url 'https://maven.aliyun.com/repository/google' }
- mavenCentral() -> maven { url 'https://maven.aliyun.com/repository/public' }
- jcenter()      -> maven { url 'https://maven.aliyun.com/repository/public' }

特性:

- 扫描目标目录（默认当前目录）下所有 *.gradle / *.gradle.kts，
  自动跳过 build/、.gradle/ 等构建产物目录。
- Groovy 与 Kotlin DSL 自动识别（.gradle.kts 使用 uri("...") 语法）。
- 逐行替换，保留缩进、行尾注释和原有行尾（CRLF/LF）。
- 纯注释行（//、/*、* 开头）不处理。
- 幂等：已替换过的文件再次运行为零改动。
- 默认先 --dry-run 预览；正式执行时对每个改动的文件创建时间戳备份，
  校验备份一致后才写回，写完回读确认无残留待替换调用。

用法::

    python mirror_gradle_repos.py --dry-run
    python mirror_gradle_repos.py
    python mirror_gradle_repos.py --target /path/to/project
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

MIRRORS = {
    "google": "https://maven.aliyun.com/repository/google",
    "mavenCentral": "https://maven.aliyun.com/repository/public",
    "jcenter": "https://maven.aliyun.com/repository/public",
}

SKIP_DIRS = {"build", ".gradle"}

# 行内匹配独立的仓库调用，前后不允许单词字符或点（排除 foo.google() 之类）
CALL_RE = re.compile(r"(?<![\w.])(google|mavenCentral|jcenter)[ \t]*\([ \t]*\)")

COMMENT_PREFIXES = ("//", "/*", "*")


def mirror_line(name: str, kts: bool) -> str:
    url = MIRRORS[name]
    if kts:
        return f'maven {{ url = uri("{url}") }}'
    return f"maven {{ url '{url}' }}"


def iter_gradle_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in parts[:-1]):
            continue
        if parts[-1].endswith(".gradle") or parts[-1].endswith(".gradle.kts"):
            yield path


def transform_line(line: str, kts: bool) -> tuple[str, int]:
    if line.lstrip().startswith(COMMENT_PREFIXES):
        return line, 0
    return CALL_RE.subn(lambda m: mirror_line(m.group(1), kts), line)


def process(path: Path, dry_run: bool) -> int:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        print(f"跳过（非 UTF-8 编码）: {path}")
        return 0

    kts = path.name.endswith(".gradle.kts")
    changes = []
    out_lines = []
    for lineno, line in enumerate(text.splitlines(keepends=True), 1):
        new_line, n = transform_line(line, kts)
        if n:
            changes.append((lineno, line.rstrip("\r\n"), new_line.rstrip("\r\n")))
        out_lines.append(new_line)

    if not changes:
        return 0

    print(f"{path}: {len(changes)} 处替换")
    for lineno, old, new in changes:
        print(f"  L{lineno}: {old.strip()}")
        print(f"      -> {new.strip()}")

    if dry_run:
        return len(changes)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.bak.{stamp}")
    backup.write_bytes(data)
    if hashlib.sha256(backup.read_bytes()).hexdigest() != hashlib.sha256(data).hexdigest():
        print(f"备份校验失败（与原文件不一致），停止: {path}", file=sys.stderr)
        return -1
    print(f"  已备份: {backup}")

    new_text = "".join(out_lines)
    path.write_bytes(new_text.encode("utf-8"))

    # 回读校验：确认无残留的非注释行待替换调用
    with path.open("r", encoding="utf-8", newline="") as f:
        for lineno, line in enumerate(f, 1):
            _, n = transform_line(line, kts)
            if n:
                print(f"回读校验失败，L{lineno} 仍有残留调用: {path}", file=sys.stderr)
                return -1
    print(f"  已写入: {path}")
    return len(changes)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--target", type=Path, default=Path.cwd(),
                   help="目标项目目录（默认当前目录）")
    p.add_argument("--dry-run", action="store_true", help="只预览，不写文件、不备份")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root: Path = args.target
    if not root.is_dir():
        print(f"目标目录不存在: {root}", file=sys.stderr)
        return 1

    files = list(iter_gradle_files(root))
    if not files:
        print(f"未找到 *.gradle / *.gradle.kts 文件: {root}")
        return 0

    total = 0
    changed_files = 0
    failed = False
    for path in files:
        n = process(path, args.dry_run)
        if n < 0:
            failed = True
            break
        if n > 0:
            changed_files += 1
            total += n

    if failed:
        return 1

    if args.dry_run:
        print(f"\n(dry-run) 扫描 {len(files)} 个文件，{changed_files} 个文件待修改，共 {total} 处替换")
    elif total == 0:
        print(f"无需修改：{len(files)} 个文件中没有待替换的仓库调用")
    else:
        print(f"\n完成：{len(files)} 个文件中 {changed_files} 个已修改，共 {total} 处替换")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
