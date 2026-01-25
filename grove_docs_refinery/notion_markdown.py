"""
Notion Markdown Converter

Converts standard GitHub-Flavored Markdown to Notion-flavored Markdown.
Main focus: pipe-delimited tables → Notion <table> XML format.

Based on Notion's enhanced markdown spec.
"""

import re
from typing import List, Tuple


def convert_pipe_table_to_notion(table_lines: List[str]) -> str:
    """
    Convert a pipe-delimited markdown table to Notion <table> XML format.

    Input:
        | Header 1 | Header 2 |
        |----------|----------|
        | Cell 1   | Cell 2   |

    Output:
        <table header-row="true">
            <tr>
                <td>Header 1</td>
                <td>Header 2</td>
            </tr>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
        </table>
    """
    if not table_lines:
        return ""

    rows = []
    has_header = False

    for i, line in enumerate(table_lines):
        line = line.strip()
        if not line:
            continue

        # Skip separator line (|---|---|) - contains only dashes, colons, pipes, spaces
        if re.match(r'^[\|\s\-:]+$', line) and '-' in line:
            has_header = True  # If there's a separator, first row is header
            continue

        # Parse cells
        cells = []
        # Remove leading/trailing pipes and split
        inner = line.strip('|')
        for cell in inner.split('|'):
            cell_content = cell.strip()
            # Escape any < > in cell content for XML safety
            cell_content = cell_content.replace('&', '&amp;')
            cell_content = cell_content.replace('<', '&lt;')
            cell_content = cell_content.replace('>', '&gt;')
            cells.append(cell_content)

        if cells:
            rows.append(cells)

    if not rows:
        return ""

    # Build Notion table XML
    header_attr = ' header-row="true"' if has_header else ''
    lines = [f'<table{header_attr}>']

    for row in rows:
        lines.append('\t<tr>')
        for cell in row:
            lines.append(f'\t\t<td>{cell}</td>')
        lines.append('\t</tr>')

    lines.append('</table>')

    return '\n'.join(lines)


def find_tables_in_markdown(content: str) -> List[Tuple[int, int, List[str]]]:
    """
    Find all pipe-delimited tables in markdown content.
    Returns list of (start_index, end_index, table_lines).
    Skips tables inside code blocks (``` fences).
    """
    lines = content.split('\n')
    tables = []
    in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Track code block state
        if line.startswith('```'):
            in_code_block = not in_code_block
            i += 1
            continue

        # Skip tables inside code blocks
        if in_code_block:
            i += 1
            continue

        # Check if line looks like start of a table (starts and ends with |)
        if line.startswith('|') and line.endswith('|') and line.count('|') >= 2:
            table_start = i
            table_lines = [lines[i]]
            i += 1

            # Collect consecutive table lines
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('|') and (next_line.endswith('|') or re.match(r'^\|[\s\-:]+\|?$', next_line)):
                    table_lines.append(lines[i])
                    i += 1
                else:
                    break

            # Only count as table if we have at least 2 rows (header + separator or data)
            if len(table_lines) >= 2:
                tables.append((table_start, i, table_lines))
        else:
            i += 1

    return tables


def convert_markdown_to_notion(content: str) -> str:
    """
    Convert standard markdown to Notion-flavored markdown.
    Currently handles:
    - Pipe-delimited tables → Notion <table> XML

    Future: toggles, callouts, etc.
    """
    # Find all tables
    tables = find_tables_in_markdown(content)

    if not tables:
        return content

    # Replace tables from end to start (to preserve indices)
    lines = content.split('\n')

    for start, end, table_lines in reversed(tables):
        notion_table = convert_pipe_table_to_notion(table_lines)
        # Replace the table lines with the Notion format
        lines[start:end] = [notion_table]

    return '\n'.join(lines)


def preview_conversion(content: str) -> dict:
    """
    Preview what would be converted without modifying content.
    Returns stats about detected elements.
    """
    tables = find_tables_in_markdown(content)

    return {
        'tables_found': len(tables),
        'table_details': [
            {
                'line_start': t[0] + 1,  # 1-indexed for humans
                'line_end': t[1],
                'rows': len([l for l in t[2] if not re.match(r'^\|[\s\-:]+\|$', l.strip().replace(' ', ''))])
            }
            for t in tables
        ]
    }


# CLI usage
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python notion_markdown.py <file.md> [--preview]")
        sys.exit(1)

    filepath = sys.argv[1]
    preview_only = '--preview' in sys.argv

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if preview_only:
        import json
        stats = preview_conversion(content)
        print(json.dumps(stats, indent=2))
    else:
        converted = convert_markdown_to_notion(content)
        print(converted)
