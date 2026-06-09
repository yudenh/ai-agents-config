---
name: docx-insert-seal
description: "Use when: insert a company seal/stamp image into a DOCX document at supplier signature placeholders."
---

# docx-insert-seal

Insert a company seal (公章) image into a DOCX document at locations where a supplier seal/stamp is required, with floating-above-text layout.

## Use When

The user wants to stamp a company seal image onto a DOCX document at supplier seal placeholder locations. Matches any paragraph containing both `供` and `盖章`, covering patterns like `供应商盖章`, `供方盖章`, `供货方盖章处`, etc. Ignore legal-representative placeholders such as `法定代表人（盖章）` / `法定代表人盖章`; do not insert the company seal there.

## Requirements

- Python 3.8+
- `officecli` CLI tool (install: `irm https://d.officecli.ai/install.ps1 | iex`)
- `Pillow` (install with `pip install Pillow` if missing)

## Steps

1. Accept the DOCX file path and seal image path as arguments.
2. Use `officecli query` to find all paragraphs containing supplier seal keywords, excluding legal-representative placeholders.
3. If no matching paragraph is found, report and exit without modification.
4. Use `officecli get /section[1]` to retrieve page dimensions.
5. Compute image dimensions via PIL (width 4cm, height proportional).
6. Compute positions:
   - **Horizontal**: center at 75% of content width (`hPosition = (pageWidth - marginLeft - marginRight) * 0.75 - imageWidth / 2`)
   - **Vertical**: center at paragraph (`vPosition = -(imageHeight / 2)`)
7. For each matching paragraph, use `officecli add --type picture` to insert a floating seal:
   - `anchor=true wrap=none behindText=false` (浮于文字上方)
   - `hRelative=column vRelative=paragraph`
   - Image source, width, height from step 5
8. **Use `officecli close` to save and close the document.** This is mandatory — officecli runs in resident mode; without an explicit `close` the file may remain locked or lose unsaved data.
9. Print the number of seals inserted.

## Python Script

Save the following script to a temporary file (e.g., `docx_insert_seal.py`) and run it:

```python
import sys
import os
import json
import subprocess
import re
from PIL import Image

# Search paragraphs containing both '供' and '盖章', excluding legal-representative placeholders
SEAL_WORDS = ['\u76d6\u7ae0']  # 盖章
LEGAL_REP_SEAL_RE = re.compile(r'\u6cd5\u5b9a\u4ee3\u8868\u4eba[\s\S]{0,12}\u76d6\u7ae0')  # 法定代表人...盖章


def officecli(args):
    result = subprocess.run(
        ['officecli'] + args,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
    if result.returncode != 0:
        err = result.stderr.strip()
        if err:
            print(f'officecli error: {err}')
        return None
    out = result.stdout.strip()
    if not out:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out


def get_image_size(img_path):
    with Image.open(img_path) as img:
        w_px, h_px = img.size
    target_w = 4.0
    ratio = h_px / w_px
    return target_w, round(target_w * ratio, 2)


def close_file(path):
    """Save and close the document. Required — officecli resident process holds a lock otherwise."""
    officecli(['close', path])


def is_legal_rep_seal_placeholder(text):
    return bool(LEGAL_REP_SEAL_RE.search(text))


def main():
    if len(sys.argv) < 3:
        print('Usage: python docx_insert_seal.py <input.docx> <seal_image>')
        sys.exit(1)

    docx_path = os.path.abspath(sys.argv[1])
    img_path = os.path.abspath(sys.argv[2])

    if not os.path.exists(docx_path):
        print(f'Error: DOCX not found: {docx_path}')
        sys.exit(1)
    if not os.path.exists(img_path):
        print(f'Error: Image not found: {img_path}')
        sys.exit(1)

    # Check officecli availability
    ver = officecli(['--version'])
    if not ver:
        print('Error: officecli not found. Install: irm https://d.officecli.ai/install.ps1 | iex')
        sys.exit(1)

    img_w, img_h = get_image_size(img_path)
    print(f'Image: {img_w}cm x {img_h}cm')

    try:
        # Find paragraphs with both '供' and '盖章', but not legal-representative placeholders
        raw_matches = {}
        for word in SEAL_WORDS:
            result = officecli([
                'query', docx_path, f'paragraph:contains("{word}")', '--json'
            ])
            if result and result.get('data', {}).get('matches', 0) > 0:
                for p in result['data']['results']:
                    raw_matches[p['path']] = p

        all_matches = [
            p for p in raw_matches.values()
            if '\u4f9b' in f"{p.get('text', '')} {p.get('preview', '')}"
            and not is_legal_rep_seal_placeholder(f"{p.get('text', '')} {p.get('preview', '')}")
        ]

        if not all_matches:
            print('No supplier seal placeholder found. Document unchanged.')
            return

        # Get page layout
        sec = officecli(['get', docx_path, '/section[1]', '--json'])
        if not sec:
            print('Error: Could not read document layout.')
            return

        fmt = sec['data']['results'][0]['format']
        pw = float(fmt['pageWidth'].replace('cm', ''))
        ml = float(fmt['marginLeft'].replace('cm', ''))
        mr = float(fmt['marginRight'].replace('cm', ''))
        content_w = pw - ml - mr

        h_pos = round(content_w * 0.75 - img_w / 2, 2)
        v_pos = round(-(img_h / 2), 2)

        inserted = 0
        for para in all_matches:
            path = para['path']
            r = officecli([
                'add', docx_path, path,
                '--type', 'picture',
                '--prop', 'anchor=true',
                '--prop', 'wrap=none',
                '--prop', 'behindText=false',
                '--prop', f'src={img_path}',
                '--prop', f'width={img_w}cm',
                '--prop', f'height={img_h}cm',
                '--prop', f'hPosition={h_pos}cm',
                '--prop', 'hRelative=column',
                '--prop', f'vPosition={v_pos}cm',
                '--prop', 'vRelative=paragraph',
            ])
            if r:
                inserted += 1
                text = para.get('text', para.get('preview', ''))[:60]
                print(f'  [{inserted}] Seal at: "{text}"')

        print(f'Done. {inserted} seal(s) inserted.')

    finally:
        # Always close the document — officecli resident holds a lock otherwise
        close_file(docx_path)


if __name__ == '__main__':
    main()
```

## Usage

```bash
# Basic usage: position seal at every matching placeholder
python docx_insert_seal.py contract.docx seal.png
```

- The script modifies the original file in place.
- The seal image should be a PNG with transparent background for best results.

## Notes

- Uses `officecli` for all DOCX manipulation via its native picture-insertion API.
- **Document must be closed after processing.** Failure to do so leaves an officecli resident process holding the file lock, preventing reuse and risking data loss. The script uses `try/finally` to ensure `close` is always called.
- The seal is inserted as a floating anchored picture (`anchor=true`, `wrap=none`), appearing above the text.
- Each matching paragraph gets its own seal; identical paths are deduplicated.
- If no keyword match is found, the document is left unchanged.
- Page layout (margins, width) is read from `/section[1]`; for documents with mixed page layouts, the first section's dimensions are used.
