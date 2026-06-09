---
name: txt-to-docx
description: "Use when: convert TXT content to a same-name DOCX document after removing empty lines."
---

# txt-to-docx

Convert a plain text (.txt) file into a same-name Microsoft Word (.docx) document.

## Use When

The user wants to convert a TXT file into a DOCX file with the same base name.

## Requirements

- Python 3.8+
- `python-docx` (install with `pip install python-docx` if missing)

## Steps

1. Accept the input TXT file path.
2. Determine the same-name DOCX path by replacing the `.txt` extension with `.docx`.
3. If the DOCX already exists, open it as the base draft; if it does not exist, create it.
4. Clear the existing DOCX body content completely.
5. Read the TXT file line by line.
6. Remove all empty lines, including blank lines and whitespace-only lines.
7. Write each remaining TXT line as one DOCX paragraph.
8. Save the DOCX to the same-name DOCX path.
9. Close the DOCX document and release the file lock after processing.

## Python Script

Save the following script to a temporary file (e.g., `txt_to_docx.py`) and run it:

```python
import os
import sys

from docx import Document


def clear_body(doc):
    body = doc._body._element
    for child in list(body):
        if child.tag.endswith('}sectPr'):
            continue
        body.remove(child)


def txt_to_docx(input_path):
    input_path = os.path.abspath(input_path)
    output_path = os.path.splitext(input_path)[0] + '.docx'

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    doc = Document(output_path) if os.path.exists(output_path) else Document()
    clear_body(doc)

    for line in lines:
        doc.add_paragraph(line)

    try:
        doc.save(output_path)
    finally:
        doc = None
    print(f'Written: {output_path}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python txt_to_docx.py <input.txt>')
        sys.exit(1)

    txt_to_docx(sys.argv[1])
```

## Usage

```bash
python txt_to_docx.py input.txt
```

## Notes

- Input `input.txt` always writes to `input.docx`.
- If `input.docx` already exists, its existing body content is fully cleared before writing TXT content.
- The script reads TXT files as UTF-8. For other encodings, modify the `open()` call accordingly.
- After processing, always close the DOCX document and release the file lock before reporting completion.
