#!/usr/bin/env python3
"""补全 dsh `cordis.patch.yml` 模型的 `input` / `reasoningEfforts`.

只补缺失项，不覆盖已有值：

- `input` 缺失或为空时填 `[text, image]`，已有则保留原样。
- `reasoningEfforts` 缺失或为空时按模型 `id` 推断，已有则保留原样：
  - `id` 含 `deepseek` / `glm` / `kimi`（大小写不敏感）-> low/high/max
  - 其他 -> low/medium/high

需要 `ruamel.yaml`（往返解析，保留原文件注释、`!!js` 表达式和缩进风格）::

    pip install ruamel.yaml
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import sys
from pathlib import Path

try:
    from ruamel.yaml import YAML
except ImportError:  # pragma: no cover
    print("缺少依赖 ruamel.yaml，请先执行: pip install ruamel.yaml", file=sys.stderr)
    sys.exit(1)

DEFAULT_TARGET = Path.home() / ".dsh" / "profiles" / "web" / "cordis.patch.yml"

VENDOR_KEYWORDS = ("deepseek", "glm", "kimi")


def efforts_for(model_id: str) -> dict:
    mid = (model_id or "").lower()
    if any(k in mid for k in VENDOR_KEYWORDS):
        return {"low": "low", "high": "high", "max": "max"}
    return {"low": "low", "medium": "medium", "high": "high"}


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=Path, default=DEFAULT_TARGET,
                   help="目标 cordis.patch.yml 路径（默认用户主目录下的 dsh 配置）")
    p.add_argument("--dry-run", action="store_true", help="只预览将要修改的模型，不写文件、不备份")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    target: Path = args.target

    if not target.is_file():
        print(f"目标文件不存在: {target}", file=sys.stderr)
        return 1

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    with target.open("r", encoding="utf-8") as f:
        data = yaml.load(f)

    if not isinstance(data, list):
        print("顶层结构不是 YAML 数组，停止", file=sys.stderr)
        return 1
    entry = next((e for e in data
                  if isinstance(e, dict) and e.get("id") == "llm-pi-ai"), None)
    if entry is None:
        print("找不到 id: llm-pi-ai 条目，停止", file=sys.stderr)
        return 1
    providers = (entry.get("config") or {}).get("providers")
    if not isinstance(providers, dict):
        print("找不到 config.providers，停止", file=sys.stderr)
        return 1

    changes: list[str] = []
    for provider_name, provider in providers.items():
        if not isinstance(provider, dict):
            continue
        models = provider.get("models")
        if not isinstance(models, list):
            continue
        for m in models:
            if not isinstance(m, dict):
                continue
            mid = str(m.get("id", ""))
            touched: list[str] = []
            if not m.get("input"):
                m["input"] = ["text", "image"]
                touched.append("input=[text,image]")
            if not m.get("reasoningEfforts"):
                m["reasoningEfforts"] = efforts_for(mid)
                touched.append(f"reasoningEfforts={list(m['reasoningEfforts'])}")
            if touched:
                changes.append(f"[{provider_name}] {mid}: {', '.join(touched)}")

    if not changes:
        print("无需修改：所有模型的 input / reasoningEfforts 均已存在")
        return 0

    print("将修改以下模型：")
    for c in changes:
        print(f"  - {c}")

    if args.dry_run:
        print("(dry-run，未写入文件)")
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = target.with_name(f"{target.name}.bak.{stamp}")
    backup.write_bytes(target.read_bytes())
    if sha256_of(backup) != sha256_of(target):
        print("备份校验失败（与原文件不一致），停止", file=sys.stderr)
        return 1
    print(f"已备份: {backup}")

    with target.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)

    # 回读校验：确保写出的文件仍可正常解析
    with target.open("r", encoding="utf-8") as f:
        yaml.load(f)
    print(f"已写入: {target}（共 {len(changes)} 个模型）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
