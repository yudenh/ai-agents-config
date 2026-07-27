#!/usr/bin/env python3
"""
Filter models in a kimi config.toml file.

By default:
  - openai provider: keep only gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna,
    gpt-5.5, gpt-5.4, gpt-5.4-mini
  - opencode provider: keep only big-pickle and model names containing "free"

Additional models can be removed with --remove model-name.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_sections(text: str) -> list[tuple[str, list[str]]]:
    """Split TOML text into (header_line, body_lines) sections."""
    sections: list[tuple[str, list[str]]] = []
    current_header = ""
    current_lines: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            if current_header or current_lines:
                sections.append((current_header, current_lines))
            current_header = line
            current_lines = []
        else:
            current_lines.append(line)

    if current_header or current_lines:
        sections.append((current_header, current_lines))

    return sections


def get_model_info(header: str) -> tuple[str | None, str | None]:
    """Extract (provider, model_name) from a [models."provider/model"] header."""
    match = re.match(r'\[models\."([^/]+)/([^"]+)"\]', header)
    if match:
        return match.group(1), match.group(2)
    return None, None


OPENAI_ALLOWED = {
    "gpt-5.6-sol",
    "gpt-5.6-terra",
    "gpt-5.6-luna",
    "gpt-5.5",
    "gpt-5.4",
    "gpt-5.4-mini",
}


def should_keep(provider: str, model_name: str) -> bool:
    """Apply default filtering rules based on provider."""
    if provider == "openai":
        return model_name in OPENAI_ALLOWED
    elif provider == "opencode":
        return model_name == "big-pickle" or "free" in model_name
    return True


def filter_config(
    input_path: Path,
    output_path: Path | None = None,
    remove_models: list[str] | None = None,
    dry_run: bool = False,
) -> int:
    """Filter the config file and write the result."""
    text = input_path.read_text(encoding="utf-8")
    sections = parse_sections(text)

    remove_set = set(remove_models or [])
    kept_sections: list[tuple[str, list[str]]] = []
    removed_count = 0

    for header, body in sections:
        provider, model_name = get_model_info(header)

        if provider is not None and model_name is not None:
            # This is a model section — apply filtering
            if model_name in remove_set:
                removed_count += 1
                continue
            if not should_keep(provider, model_name):
                removed_count += 1
                continue

        kept_sections.append((header, body))

    # Reconstruct the file
    output_lines: list[str] = []
    for header, body in kept_sections:
        if header:
            output_lines.append(header)
        output_lines.extend(body)

    # Ensure file ends with a newline
    result = "\n".join(output_lines)
    if not result.endswith("\n"):
        result += "\n"

    if dry_run:
        print(result, end="")
        return removed_count

    target = output_path or input_path
    target.write_text(result, encoding="utf-8")
    print(f"Removed {removed_count} model(s). Written to {target}", file=sys.stderr)
    return removed_count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Filter models in a kimi config.toml file."
    )
    default_config = Path.home() / ".kimi-code" / "config.toml"
    parser.add_argument(
        "config",
        type=Path,
        nargs="?",
        default=default_config,
        help=f"Path to config.toml (default: {default_config})",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output path (default: overwrite input file)",
    )
    parser.add_argument(
        "--remove",
        action="append",
        default=[],
        metavar="MODEL",
        help="Additional model name to remove (can be repeated)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print filtered output to stdout without writing",
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: {args.config} not found", file=sys.stderr)
        return 1

    filter_config(
        input_path=args.config,
        output_path=args.output,
        remove_models=args.remove,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
