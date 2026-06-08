---
name: docx-add-watermark
description: "Use when: add an image watermark to a DOCX document with configurable position and size."
---

# docx-add-watermark

Add an image watermark to a DOCX document. The watermark is placed in the page header (behind text) on every section.

## Use When

The user wants to stamp an image watermark onto a DOCX document (e.g., company logo, "DRAFT", "CONFIDENTIAL").

## Requirements

- Python 3.8+
- `office-tools` CLI tool installed from the `office-tools-cli` project (depends on `pywin32`, requires Microsoft Word or WPS with COM support)
- `Pillow` (install with `pip install Pillow` if missing)

## Steps

1. Accept the DOCX file path and watermark image path as arguments.
2. Accept optional position/size parameters with defaults:
   - `--left`: distance from left edge (default 100pt)
   - `--top`: distance from top edge (default 200pt)
   - `--width`: watermark width (default 115pt)
   - `--height`: watermark height (auto-proportional from aspect ratio if omitted)
3. Validate that both files exist.
4. If `--height` is not specified, use PIL to read the image dimensions and compute the proportional height based on `--width`.
5. Call `office-tools watermark-docx` with the computed parameters.
6. The tool saves, closes the document, and exits Word automatically.
7. Report success or failure.

## Python Script

Save the following script to a temporary file (e.g., `docx_add_watermark.py`) and run it:

```python
import sys
import os
import json
import subprocess
from PIL import Image


def office_tools(args):
    result = subprocess.run(
        ['office-tools'] + args,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    out = result.stdout.strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out


def get_image_size(img_path):
    with Image.open(img_path) as img:
        return img.size


def main():
    import argparse

    parser = argparse.ArgumentParser(description='为 DOCX 文档添加图片水印')
    parser.add_argument('docx_path', help='输入的 DOCX 文件路径')
    parser.add_argument('image_path', help='水印图片路径')
    parser.add_argument('--left', type=float, default=100,
                        help='水印水平位置 (pt)，默认 100')
    parser.add_argument('--top', type=float, default=200,
                        help='水印垂直位置 (pt)，默认 200')
    parser.add_argument('--width', type=float, default=115,
                        help='水印宽度 (pt)，默认 115')
    parser.add_argument('--height', type=float, default=None,
                        help='水印高度 (pt)，不指定则等比自适应')
    args = parser.parse_args()

    docx_path = os.path.abspath(args.docx_path)
    img_path = os.path.abspath(args.image_path)

    if not os.path.exists(docx_path):
        print(f'Error: DOCX not found: {docx_path}')
        sys.exit(1)
    if not os.path.exists(img_path):
        print(f'Error: Image not found: {img_path}')
        sys.exit(1)

    width = args.width
    height = args.height
    if height is None:
        w_px, h_px = get_image_size(img_path)
        height = round(width * h_px / w_px, 2)
        print(f'Image: {w_px}x{h_px}px, auto height: {height}pt')

    print(f'Watermark: left={args.left}pt top={args.top}pt '
          f'width={width}pt height={height}pt')

    result = office_tools([
        'watermark-docx', docx_path,
        '--image', img_path,
        '--watermark-left', str(args.left),
        '--watermark-top', str(args.top),
        '--watermark-width', str(width),
        '--watermark-height', str(height),
        '--json',
    ])

    if result and result.get('ok'):
        print(f'Done. Watermark added to: {docx_path}')
    else:
        error = (result.get('items', [{}])[0].get('error', 'Unknown error')
                 if result else 'Unknown error')
        print(f'Failed: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()
```

## Usage

```bash
# Default: left=100pt, top=200pt, width=115pt, height=auto
python docx_add_watermark.py report.docx logo.png

# Custom position and size
python docx_add_watermark.py report.docx logo.png --left 150 --top 250 --width 200 --height 150
```

## Notes

- The watermark image is embedded (not linked) and placed behind text in each section's header.
- Document is saved, closed, and Word is terminated automatically — no manual cleanup needed.
- Requires Microsoft Word or a COM-compatible WPS installation on Windows.
- The script modifies the original file in place.
