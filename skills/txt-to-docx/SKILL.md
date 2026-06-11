---
name: txt-to-docx
description: "Use when: convert TXT content to a same-name DOCX document after removing empty lines and turning obvious tab/space/pipe-delimited blocks into tables."
---

# txt-to-docx

Convert a plain text (.txt) file into a same-name Microsoft Word (.docx) document. Obvious table-like text blocks are converted into DOCX tables.

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
7. Detect consecutive table-like lines split by tabs, pipes (`|`), or two-or-more spaces.
8. Convert table-like blocks of at least 2 rows and 2 columns into DOCX tables.
9. Apply black borders to every table cell and vertically center cell content.
10. Write all other TXT lines as DOCX paragraphs.
11. Save the DOCX to the same-name DOCX path.
12. Close the DOCX document and release the file lock after processing.

## Python Script

Save the following script to a temporary file (e.g., `txt_to_docx.py`) and run it:

```python
import os
import re
import sys

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def clear_body(doc):
    body = doc._body._element
    for child in list(body):
        if child.tag.endswith('}sectPr'):
            continue
        body.remove(child)


def split_table_cells(line):
    text = line.strip()
    if '\t' in text:
        cells = re.split(r'\t+', text)
    elif '|' in text:
        cells = text.strip('|').split('|')
    elif re.search(r' {2,}', text):
        cells = re.split(r' {2,}', text)
    else:
        return None

    cells = [cell.strip() for cell in cells]
    if len(cells) < 2 or any(not cell for cell in cells):
        return None
    return cells


def set_cell_black_borders(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tc_pr.append(borders)

    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        tag = f'w:{edge}'
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn('w:val'), 'single')
        element.set(qn('w:sz'), '4')
        element.set(qn('w:space'), '0')
        element.set(qn('w:color'), '000000')


def add_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            cell = table.cell(row_index, col_index)
            cell.text = value
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_black_borders(cell)


def add_lines(doc, lines):
    index = 0
    while index < len(lines):
        cells = split_table_cells(lines[index])
        if cells is None:
            doc.add_paragraph(lines[index])
            index += 1
            continue

        rows = [cells]
        col_count = len(cells)
        next_index = index + 1
        while next_index < len(lines):
            next_cells = split_table_cells(lines[next_index])
            if next_cells is None or len(next_cells) != col_count:
                break
            rows.append(next_cells)
            next_index += 1

        if len(rows) >= 2:
            add_table(doc, rows)
        else:
            doc.add_paragraph(lines[index])
        index = next_index


def txt_to_docx(input_path):
    input_path = os.path.abspath(input_path)
    output_path = os.path.splitext(input_path)[0] + '.docx'

    with open(input_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    doc = Document(output_path) if os.path.exists(output_path) else Document()
    clear_body(doc)

    add_lines(doc, lines)

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
- Table detection only uses tabs, pipes (`|`), and two-or-more spaces as delimiters; commas are not table delimiters.
- Table blocks must contain at least 2 consecutive rows with the same column count.
- The script reads TXT files as UTF-8. For other encodings, modify the `open()` call accordingly.
- After processing, always close the DOCX document and release the file lock before reporting completion.
