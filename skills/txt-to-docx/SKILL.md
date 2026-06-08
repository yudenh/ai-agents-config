---
name: txt-to-docx
description: "Use when: convert TXT file content to a formatted DOCX document, removing empty lines and applying heading styles."
---

# txt-to-docx

Convert a plain text (.txt) file into a Microsoft Word (.docx) document with automatic heading detection and formatting.

## Use When

The user wants to convert a TXT file to a formatted DOCX document, especially when headings need to be auto-detected and bolded.

## Requirements

- Python 3.8+
- `python-docx` (install with `pip install python-docx` if missing)

## Steps

1. Read the input TXT file line by line.
2. Remove all empty lines (lines that contain only whitespace or are blank).
3. Apply formatting rules to each remaining line.
4. Create the output DOCX file. If the output path already exists, append a numeric suffix (`_1`, `_2`, ...) to avoid overwriting.
5. Add page numbers (Arabic numerals, centered) to the document footer.
6. Save and close the document.

## Formatting Rules (applied independently to each line)

### a. Title detection (first line only)
After removing empty lines, if the **first line** contains no Chinese or English punctuation marks, format it as a bold title with larger font (16pt, centered).

Punctuation characters to check: `，。！？、；：""''（）《》【】,\.!?;:'"()\[\]{}`

### b. Chinese numbered headings
Lines starting with these patterns are bold:
- `一、` `二、` `三、` ... (Chinese numeral + Chinese comma)
- `（一）` `（二）` ... (parenthesized Chinese numerals)
- `1、` `2、` ... (Arabic numeral + Chinese comma)
- `1．` `2．` ... (Arabic numeral + full-width dot)

### c. Numerical hierarchical headings
Lines matching patterns like `1.1`, `1.1.1`, `2.1`, `3.2.1` etc. are bold.

Regex: `^\d+(\.\d+)+(\s|$)` — one or more digits, followed by one or more dot-number groups, then whitespace or end-of-line.

### d. Everything else
Normal paragraph text (no bold).

## Python Script

Save the following script to a temporary file (e.g., `txt_to_docx.py`) and run it:

```python
import re
import sys
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PUNCTUATION = set('，。！？、；：""\'\'（）《》【】,.!?;:\'\"()[]{}')


def has_punctuation(text):
    return any(ch in PUNCTUATION for ch in text)


def is_chinese_heading(line):
    stripped = line.strip()
    if re.match(r'^[一二三四五六七八九十]+[、]', stripped):
        return True
    if re.match(r'^（[一二三四五六七八九十]+）', stripped):
        return True
    if re.match(r'^\d+[、．]', stripped):
        return True
    return False


def is_numeric_heading(line):
    stripped = line.strip()
    return bool(re.match(r'^\d+(\.\d+)+(\s|$)', stripped))


def add_page_number(doc):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar1)

    run2 = paragraph.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    run2._r.append(instrText)

    run3 = paragraph.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run3._r.append(fldChar2)


def txt_to_docx(input_path, output_path=None):
    # Read and filter lines
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n').rstrip('\r') for line in f]

    # Remove empty lines
    lines = [line for line in lines if line.strip()]

    if not lines:
        print("No content after removing empty lines.")
        return

    # Determine output path
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.docx'

    base, ext = os.path.splitext(output_path)
    counter = 1
    while os.path.exists(output_path):
        output_path = f"{base}_{counter}{ext}"
        counter += 1

    doc = Document()

    # Set default fonts: DengXian (等线) for Latin, SimSun (宋体) for CJK
    style = doc.styles['Normal']
    rPr = style.element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'DengXian')
    rFonts.set(qn('w:hAnsi'), 'DengXian')
    rFonts.set(qn('w:eastAsia'), 'SimSun')
    rPr.insert(0, rFonts)

    for i, line in enumerate(lines):
        stripped = line.strip()
        p = doc.add_paragraph()

        if i == 0 and not has_punctuation(stripped):
            # Rule a: Title
            run = p.add_run(stripped)
            run.bold = True
            run.font.size = Pt(16)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_chinese_heading(stripped):
            # Rule b: Chinese numbered heading
            run = p.add_run(stripped)
            run.bold = True
        elif is_numeric_heading(stripped):
            # Rule c: Numerical hierarchical heading
            run = p.add_run(stripped)
            run.bold = True
        else:
            # Normal text
            p.add_run(stripped)

    add_page_number(doc)
    doc.save(output_path)
    print(f"Created: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python txt_to_docx.py <input.txt> [output.docx]")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    txt_to_docx(input_path, output_path)
```

## Usage

```bash
python txt_to_docx.py input.txt                    # output: input.docx
python txt_to_docx.py input.txt output.docx         # output: output.docx
```

## Notes

- If the output file already exists, the script appends `_1`, `_2`, etc. to avoid overwriting.
- The script reads TXT files as UTF-8. For other encodings, modify the `open()` call accordingly.
- Do NOT attempt to fix or modify the script unless the task explicitly requires it.
