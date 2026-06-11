---
name: docx-format-standard
description: "Use when: apply common Chinese standard formatting to DOCX documents, including fonts, bold headings, first-line indent, table spacing, and centered page numbers."
---

# docx-format-standard

Format an existing Microsoft Word (.docx) document using common Chinese standard document formatting.

## Use When

The user wants to standardize a DOCX document by applying common Chinese document formatting, including fonts, heading bolding, paragraph indentation, table formatting, and centered page numbers.

## Requirements

- Python 3.8+
- `python-docx` (install with `pip install python-docx` if missing)

## Steps

1. Accept the input DOCX path and optional output DOCX path. By default, edit and save over the original document; only save a separate copy when the user explicitly asks for it.
2. Open the DOCX with `python-docx`.
3. Set the document default font:
   - Latin/default font: `等线` (`DengXian`)
   - East Asian/Chinese font: `宋体` (`SimSun`)
   - Default font size: `小四` (`12pt`)
4. Set every paragraph to 0 lines before, 0 lines after, and 1.15 line spacing.
5. Treat the document's first non-empty paragraph as the title, set it bold, center it, and set its font size to `三号` (`16pt`). Skip leading blank paragraphs when locating the title.
6. Bold Chinese numbered headings like `一、...`, `二、...`, `三、...`, set their font size to `四号` (`14pt`), and set both spacing before and after to `0.5` line.
7. Bold numeric hierarchy headings like `1.1`, `1.2`, `2.1`, `2.1.1`, `3.2.1`.
8. For non-heading paragraphs, set first-line indent to 2 Chinese characters.
9. For all table cells, set paragraph spacing before/after to `0` lines, line spacing to single, and vertical alignment to center.
10. Add centered Arabic page numbers to every section footer.
11. Save the output document and close/release all document handles.

## Formatting Rules

### Font

- Default Latin/default font: `等线` (`DengXian`).
- Default East Asian/Chinese font: `宋体` (`SimSun`).
- Default font size: `小四` (`12pt`).

### Title

- Use the document's first non-empty paragraph as the title.
- Skip leading blank paragraphs when determining the title.
- Preserve its original text and paragraph position.
- Set all runs in the title paragraph to bold.
- Set the title font size to `三号` (`16pt`).
- Center the title paragraph.

### Paragraph Spacing

- Apply to every paragraph.
- Set spacing before to `0` lines.
- Set spacing after to `0` lines.
- Set line spacing to `1.15`.

### Chinese Numbered Headings

Bold paragraphs whose stripped text starts with a Chinese numeral followed by `、`, set their font size to `四号` (`14pt`), and set both spacing before and after to `0.5` line.

Regex: `^[一二三四五六七八九十百千万]+、`

Examples:

- `一、项目背景`
- `二、建设内容`
- `三、实施计划`

### Numeric Hierarchy Headings

Bold paragraphs whose stripped text starts with a dotted numeric hierarchy.

Regex: `^\d+(\.\d+)+(\s|\u3000|$)`

Examples:

- `1.1 项目概述`
- `1.2 建设目标`
- `2.1.1 系统架构`
- `3.2.1 数据流程`

### Normal Paragraphs

- Paragraphs that are not the title and do not match heading rules are normal body paragraphs.
- Set first-line indent to 2 Chinese characters, approximately `0.74cm`.
- Do not force bold off; preserve existing emphasis unless the task explicitly asks to remove it.

### Tables

- Apply to every table cell in every table.
- Set each cell paragraph's spacing before to `0` lines.
- Set each cell paragraph's spacing after to `0` lines.
- Set each cell paragraph's line spacing to single.
- Set each table cell's vertical alignment to center.
- Set each table row's minimum height to `1cm`.
- Enable table column autofit.

### Page Number Footer

- Add Arabic page numbers using Word `PAGE` field.
- Align footer paragraph center.
- Apply to all document sections.

## Python Script

Save the following script to a temporary file (e.g., `docx_format_standard.py`) and run it:

```python
import os
import re
import sys

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


CHINESE_HEADING_RE = re.compile(r'^[一二三四五六七八九十百千万]+、')
NUMERIC_HEADING_RE = re.compile(r'^\d+(\.\d+)+(\s|\u3000|$)')


def set_run_font(run, size_pt=12):
    run.font.name = 'DengXian'
    run.font.size = Pt(size_pt)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')


def set_default_font(doc):
    style = doc.styles['Normal']
    style.font.name = 'DengXian'
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.rFonts
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), 'DengXian')
    rFonts.set(qn('w:hAnsi'), 'DengXian')
    rFonts.set(qn('w:eastAsia'), 'SimSun')


def set_paragraph_bold(paragraph, size_pt=12):
    if not paragraph.runs:
        paragraph.add_run(paragraph.text)
    for run in paragraph.runs:
        run.bold = True
        set_run_font(run, size_pt)


def set_paragraph_spacing(paragraph):
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(0)
    paragraph_format.space_after = Pt(0)
    paragraph_format.line_spacing = 1.15
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE


def set_chinese_heading_spacing(paragraph):
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(6)
    paragraph_format.space_after = Pt(6)


def get_title_index(paragraphs):
    return next((index for index, paragraph in enumerate(paragraphs) if paragraph.text.strip()), None)


def set_table_paragraph_spacing(paragraph):
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(0)
    paragraph_format.space_after = Pt(0)
    paragraph_format.line_spacing = 1
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE


def format_tables(doc):
    for table in doc.tables:
        table.autofit = True
        for row in table.rows:
            row.height = Cm(1)
            row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
            for cell in row.cells:
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                for paragraph in cell.paragraphs:
                    set_table_paragraph_spacing(paragraph)


def is_chinese_heading(text):
    return bool(CHINESE_HEADING_RE.match(text.strip()))


def is_numeric_heading(text):
    return bool(NUMERIC_HEADING_RE.match(text.strip()))


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.text = ''

    run = paragraph.add_run()
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    run._r.append(fld_begin)

    instr_run = paragraph.add_run()
    instr_text = OxmlElement('w:instrText')
    instr_text.set(qn('xml:space'), 'preserve')
    instr_text.text = ' PAGE '
    instr_run._r.append(instr_text)

    end_run = paragraph.add_run()
    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    end_run._r.append(fld_end)


def add_footer_page_numbers(doc):
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        add_page_number(paragraph)


def format_document(input_path, output_path=None):
    input_path = os.path.abspath(input_path)
    if output_path is None:
        output_path = input_path
    output_path = os.path.abspath(output_path)

    doc = Document(input_path)

    try:
        set_default_font(doc)
        paragraphs = doc.paragraphs
        title_index = get_title_index(paragraphs)

        for index, paragraph in enumerate(paragraphs):
            set_paragraph_spacing(paragraph)
            stripped = paragraph.text.strip()
            if not stripped:
                continue

            for run in paragraph.runs:
                set_run_font(run)

            if index == title_index:
                continue
            elif is_chinese_heading(stripped):
                set_paragraph_bold(paragraph, 14)
                set_chinese_heading_spacing(paragraph)
            elif is_numeric_heading(stripped):
                set_paragraph_bold(paragraph)
            else:
                paragraph.paragraph_format.first_line_indent = Cm(0.74)

        if title_index is not None:
            title_paragraph = paragraphs[title_index]
            title_paragraph.paragraph_format.first_line_indent = Cm(0)
            set_paragraph_bold(title_paragraph, 16)
            title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        format_tables(doc)
        add_footer_page_numbers(doc)
        doc.save(output_path)
        print(f'Formatted: {output_path}')
    finally:
        # python-docx does not keep Word open, but dropping references makes the release explicit.
        doc = None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python docx_format_standard.py <input.docx> [output.docx]')
        sys.exit(1)

    format_document(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

## Usage

```bash
python docx_format_standard.py document.docx
python docx_format_standard.py document.docx document_formatted.docx
```

## Notes

- By default, the script edits and saves over the original DOCX. Save to a separate output path only when the user explicitly asks for a separate copy.
- `python-docx` does not launch Microsoft Word and normally does not leave a Word application lock.
- If using `officecli`, COM automation, LibreOffice, or Word automation instead, always save and close the document after processing. This is mandatory: failing to close the document can leave the DOCX locked and prevent later edits.
- After processing, verify that no Office/automation process is holding the document lock before reporting completion.
