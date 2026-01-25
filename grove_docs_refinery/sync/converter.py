"""
Markdown <-> Notion blocks converter with table support.

Handles bidirectional conversion between:
- Local markdown files (with YAML frontmatter)
- Notion block structure

Key features:
- Table support (both directions)
- Nested block handling (toggles, columns)
- Rich text formatting preservation
"""

import re
import yaml
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


# Language normalization for Notion API
# Notion only accepts specific language values
LANGUAGE_ALIASES = {
    'tsx': 'typescript',
    'jsx': 'javascript',
    'ts': 'typescript',
    'js': 'javascript',
    'py': 'python',
    'rb': 'ruby',
    'sh': 'shell',
    'bash': 'shell',
    'zsh': 'shell',
    'yml': 'yaml',
    'md': 'markdown',
    'dockerfile': 'docker',
    'rs': 'rust',
    'cs': 'c#',
    'cpp': 'c++',
    'h': 'c',
    'hpp': 'c++',
    'kt': 'kotlin',
    'tf': 'hcl',
    'hcl': 'hcl',
    'vim': 'vimscript',
    'vue': 'vue',
    'svelte': 'svelte',
    '': 'plain text',
}


def normalize_language(lang: str) -> str:
    """Normalize code block language to Notion-accepted value."""
    lang_lower = lang.lower().strip()
    return LANGUAGE_ALIASES.get(lang_lower, lang_lower or 'plain text')


# ============================================================================
# Notion -> Markdown
# ============================================================================

def extract_text(rich_text: List[Dict]) -> str:
    """Extract plain text from Notion rich_text array."""
    if not rich_text:
        return ''
    return ''.join(item.get('plain_text', '') for item in rich_text)


def rich_text_to_markdown(rich_text: List[Dict]) -> str:
    """Convert Notion rich_text to markdown with formatting."""
    if not rich_text:
        return ''

    parts = []
    for item in rich_text:
        text = item.get('plain_text', '')
        if not text:
            continue

        annotations = item.get('annotations', {})
        href = item.get('href')

        # Apply formatting in order
        if annotations.get('code'):
            text = f'`{text}`'
        if annotations.get('bold'):
            text = f'**{text}**'
        if annotations.get('italic'):
            text = f'*{text}*'
        if annotations.get('strikethrough'):
            text = f'~~{text}~~'
        if annotations.get('underline'):
            text = f'<u>{text}</u>'
        if href:
            text = f'[{text}]({href})'

        parts.append(text)

    return ''.join(parts)


def block_to_markdown(block: Dict, indent: int = 0) -> str:
    """Convert a single Notion block to markdown."""
    block_type = block.get('type')
    content = block.get(block_type, {})
    prefix = '    ' * indent

    # Handle different block types
    if block_type == 'paragraph':
        text = rich_text_to_markdown(content.get('rich_text', []))
        result = f'{prefix}{text}\n' if text else f'{prefix}\n'

    elif block_type in ('heading_1', 'heading_2', 'heading_3'):
        level = int(block_type[-1])
        text = rich_text_to_markdown(content.get('rich_text', []))
        result = f'{prefix}{"#" * level} {text}\n'

    elif block_type == 'bulleted_list_item':
        text = rich_text_to_markdown(content.get('rich_text', []))
        result = f'{prefix}- {text}\n'

    elif block_type == 'numbered_list_item':
        text = rich_text_to_markdown(content.get('rich_text', []))
        result = f'{prefix}1. {text}\n'

    elif block_type == 'to_do':
        text = rich_text_to_markdown(content.get('rich_text', []))
        checked = '- [x]' if content.get('checked') else '- [ ]'
        result = f'{prefix}{checked} {text}\n'

    elif block_type == 'toggle':
        text = rich_text_to_markdown(content.get('rich_text', []))
        result = f'{prefix}<details>\n{prefix}<summary>{text}</summary>\n'
        # Children will be added below
        if '_children' in block:
            for child in block['_children']:
                result += block_to_markdown(child, indent + 1)
        result += f'{prefix}</details>\n'
        return result  # Early return - children already handled

    elif block_type == 'code':
        text = extract_text(content.get('rich_text', []))
        language = content.get('language', '')
        result = f'{prefix}```{language}\n{text}\n{prefix}```\n'

    elif block_type == 'quote':
        text = rich_text_to_markdown(content.get('rich_text', []))
        lines = text.split('\n')
        result = '\n'.join(f'{prefix}> {line}' for line in lines) + '\n'

    elif block_type == 'callout':
        text = rich_text_to_markdown(content.get('rich_text', []))
        icon = content.get('icon', {})
        emoji = icon.get('emoji', '💡') if icon.get('type') == 'emoji' else '💡'
        result = f'{prefix}> {emoji} {text}\n'

    elif block_type == 'divider':
        result = f'{prefix}---\n'

    elif block_type == 'table':
        result = table_to_markdown(block, indent)

    elif block_type == 'image':
        image = content.get('file', {}) or content.get('external', {})
        url = image.get('url', '')
        caption = extract_text(content.get('caption', []))
        result = f'{prefix}![{caption}]({url})\n'

    elif block_type == 'bookmark':
        url = content.get('url', '')
        caption = extract_text(content.get('caption', [])) or url
        result = f'{prefix}[{caption}]({url})\n'

    elif block_type == 'equation':
        expression = content.get('expression', '')
        result = f'{prefix}$$\n{expression}\n$$\n'

    elif block_type == 'child_page':
        title = content.get('title', 'Untitled')
        result = f'{prefix}<!-- Child page: {title} -->\n'

    elif block_type == 'child_database':
        title = content.get('title', 'Untitled')
        result = f'{prefix}<!-- Child database: {title} -->\n'

    elif block_type == 'column_list':
        # Handle columns - convert to sequential content
        result = ''
        if '_children' in block:
            for column in block['_children']:
                if column.get('type') == 'column' and '_children' in column:
                    for child in column['_children']:
                        result += block_to_markdown(child, indent)
        return result

    elif block_type == 'synced_block':
        # Synced blocks contain their content in children
        result = ''
        if '_children' in block:
            for child in block['_children']:
                result += block_to_markdown(child, indent)
        return result

    else:
        # Unknown block type - add comment
        result = f'{prefix}<!-- Unsupported block type: {block_type} -->\n'

    # Handle children (for blocks that support nesting, except those handled above)
    if '_children' in block and block_type not in ('toggle', 'table', 'column_list', 'synced_block'):
        for child in block['_children']:
            result += block_to_markdown(child, indent + 1)

    return result


def table_to_markdown(table_block: Dict, indent: int = 0) -> str:
    """Convert a Notion table block to markdown table."""
    prefix = '    ' * indent
    children = table_block.get('_children', [])

    if not children:
        return f'{prefix}<!-- Empty table -->\n'

    rows = []
    max_cols = 0

    for row_block in children:
        if row_block.get('type') == 'table_row':
            cells = row_block.get('table_row', {}).get('cells', [])
            row_text = [rich_text_to_markdown(cell) for cell in cells]
            rows.append(row_text)
            max_cols = max(max_cols, len(row_text))

    if not rows:
        return f'{prefix}<!-- Empty table -->\n'

    # Normalize row lengths
    for row in rows:
        while len(row) < max_cols:
            row.append('')

    # Build markdown table
    lines = []
    lines.append(prefix + '| ' + ' | '.join(rows[0]) + ' |')
    lines.append(prefix + '|' + '---|' * max_cols)

    for row in rows[1:]:
        lines.append(prefix + '| ' + ' | '.join(row) + ' |')

    return '\n'.join(lines) + '\n'


def blocks_to_markdown(blocks: List[Dict]) -> str:
    """Convert a list of Notion blocks to markdown."""
    lines = []
    for block in blocks:
        lines.append(block_to_markdown(block))
    return ''.join(lines)


def notion_page_to_markdown(page: Dict, blocks: List[Dict]) -> str:
    """
    Convert a Notion page to markdown with YAML frontmatter.

    Args:
        page: Notion page metadata
        blocks: Page blocks (from get_block_children)

    Returns:
        Complete markdown string with frontmatter
    """
    props = page.get('properties', {})

    # Extract title
    title_prop = props.get('title') or props.get('Name') or {}
    if title_prop.get('type') == 'title':
        title = extract_text(title_prop.get('title', []))
    else:
        title = 'Untitled'

    # Build frontmatter
    frontmatter = {
        'title': title,
        'notion_id': page.get('id', '').replace('-', ''),
        'notion_url': page.get('url', ''),
        'last_synced': datetime.now().isoformat(),
        'created_time': page.get('created_time', ''),
        'last_edited_time': page.get('last_edited_time', '')
    }

    # Convert blocks to markdown
    content = blocks_to_markdown(blocks)

    # Assemble document
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
    return f'---\n{yaml_str}---\n\n{content}'


# ============================================================================
# Markdown -> Notion
# ============================================================================

def clean_markdown(text: str) -> str:
    """
    Clean up common markdown formatting issues before conversion.

    Handles:
    - Blank lines within tables (collapses them)
    - Consecutive empty lines (reduces to one)
    - Trailing whitespace
    """
    lines = text.split('\n')
    result = []
    in_table = False
    prev_empty = False

    for line in lines:
        stripped = line.strip()

        # Detect table boundaries
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            result.append(line)
            prev_empty = False
        elif in_table and not stripped:
            # Skip blank lines inside tables
            continue
        elif in_table and not stripped.startswith('|'):
            # End of table
            in_table = False
            # Don't add blank line if previous was already blank
            if stripped:
                result.append(line)
                prev_empty = False
            elif not prev_empty:
                result.append('')
                prev_empty = True
        elif not stripped:
            # Empty line - only add if previous wasn't empty
            if not prev_empty:
                result.append('')
                prev_empty = True
        else:
            result.append(line)
            prev_empty = False

    return '\n'.join(result)


def text_to_rich_text(text: str) -> List[Dict]:
    """Convert plain text with markdown formatting to Notion rich_text format."""
    if not text:
        return []

    # Tokenize the text into segments with formatting
    segments = _parse_inline_formatting(text)

    result = []
    for segment in segments:
        item = {
            'type': 'text',
            'text': {'content': segment['text']},
            'annotations': {
                'bold': segment.get('bold', False),
                'italic': segment.get('italic', False),
                'strikethrough': segment.get('strikethrough', False),
                'underline': False,
                'code': segment.get('code', False)
            }
        }
        if segment.get('href'):
            item['text']['link'] = {'url': segment['href']}
        result.append(item)

    return result


def _parse_inline_formatting(text: str) -> List[Dict]:
    """
    Parse markdown inline formatting into segments.

    Handles: **bold**, *italic*, `code`, [links](url), ~~strikethrough~~
    """
    segments = []

    # Combined pattern to match all inline formatting
    # Order matters: bold before italic, code is greedy
    pattern = re.compile(
        r'(`[^`]+`)'                           # code
        r'|(\*\*[^*]+\*\*)'                    # bold with **
        r'|(__[^_]+__)'                        # bold with __
        r'|(~~[^~]+~~)'                        # strikethrough
        r'|(\*[^*]+\*)'                        # italic with *
        r'|(_[^_]+_)'                          # italic with _
        r'|(\[[^\]]+\]\([^)]+\))'              # links
    )

    last_end = 0
    for match in pattern.finditer(text):
        # Add plain text before this match
        if match.start() > last_end:
            plain = text[last_end:match.start()]
            if plain:
                segments.append({'text': plain})

        matched = match.group()

        # Determine which pattern matched
        if matched.startswith('`') and matched.endswith('`'):
            # Code
            segments.append({
                'text': matched[1:-1],
                'code': True
            })
        elif matched.startswith('**') and matched.endswith('**'):
            # Bold with **
            inner = matched[2:-2]
            # Check for nested italic
            if inner.startswith('*') and inner.endswith('*') and len(inner) > 2:
                segments.append({
                    'text': inner[1:-1],
                    'bold': True,
                    'italic': True
                })
            else:
                segments.append({
                    'text': inner,
                    'bold': True
                })
        elif matched.startswith('__') and matched.endswith('__'):
            # Bold with __
            segments.append({
                'text': matched[2:-2],
                'bold': True
            })
        elif matched.startswith('~~') and matched.endswith('~~'):
            # Strikethrough
            segments.append({
                'text': matched[2:-2],
                'strikethrough': True
            })
        elif matched.startswith('*') and matched.endswith('*'):
            # Italic with *
            segments.append({
                'text': matched[1:-1],
                'italic': True
            })
        elif matched.startswith('_') and matched.endswith('_'):
            # Italic with _
            segments.append({
                'text': matched[1:-1],
                'italic': True
            })
        elif matched.startswith('['):
            # Link
            link_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', matched)
            if link_match:
                segments.append({
                    'text': link_match.group(1),
                    'href': link_match.group(2)
                })

        last_end = match.end()

    # Add remaining plain text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            segments.append({'text': remaining})

    # If no segments found, return the whole text as plain
    if not segments:
        segments = [{'text': text}]

    return segments


def markdown_line_to_block(line: str, next_lines: List[str] = None) -> Tuple[Optional[Dict], int]:
    """
    Convert a markdown line to a Notion block.

    Returns:
        Tuple of (block_dict or None, lines_consumed)
    """
    stripped = line.strip()
    lines_consumed = 1

    if not stripped:
        return {'type': 'paragraph', 'paragraph': {'rich_text': []}}, 1

    # Headings
    if stripped.startswith('# '):
        return {
            'type': 'heading_1',
            'heading_1': {'rich_text': text_to_rich_text(stripped[2:])}
        }, 1

    if stripped.startswith('## '):
        return {
            'type': 'heading_2',
            'heading_2': {'rich_text': text_to_rich_text(stripped[3:])}
        }, 1

    if stripped.startswith('### '):
        return {
            'type': 'heading_3',
            'heading_3': {'rich_text': text_to_rich_text(stripped[4:])}
        }, 1

    # Divider
    if stripped in ('---', '***', '___'):
        return {'type': 'divider', 'divider': {}}, 1

    # Bullet list
    if stripped.startswith('- ') or stripped.startswith('* '):
        text = stripped[2:]
        # Check for checkbox
        if text.startswith('[ ] '):
            return {
                'type': 'to_do',
                'to_do': {'rich_text': text_to_rich_text(text[4:]), 'checked': False}
            }, 1
        if text.startswith('[x] ') or text.startswith('[X] '):
            return {
                'type': 'to_do',
                'to_do': {'rich_text': text_to_rich_text(text[4:]), 'checked': True}
            }, 1
        return {
            'type': 'bulleted_list_item',
            'bulleted_list_item': {'rich_text': text_to_rich_text(text)}
        }, 1

    # Numbered list
    if re.match(r'^\d+\.\s', stripped):
        text = re.sub(r'^\d+\.\s', '', stripped)
        return {
            'type': 'numbered_list_item',
            'numbered_list_item': {'rich_text': text_to_rich_text(text)}
        }, 1

    # Quote
    if stripped.startswith('> '):
        return {
            'type': 'quote',
            'quote': {'rich_text': text_to_rich_text(stripped[2:])}
        }, 1

    # Code block (need to look ahead)
    if stripped.startswith('```'):
        raw_language = stripped[3:].strip()
        language = normalize_language(raw_language)
        code_lines = []
        lines_consumed = 1

        if next_lines:
            for next_line in next_lines:
                lines_consumed += 1
                if next_line.strip().startswith('```'):
                    break
                code_lines.append(next_line.rstrip())

        code_content = '\n'.join(code_lines)

        # Notion API has a 2000 character limit per rich_text content
        # Split long code blocks into multiple blocks
        MAX_CHARS = 1900  # Leave some margin for safety
        if len(code_content) <= MAX_CHARS:
            return {
                'type': 'code',
                'code': {
                    'rich_text': text_to_rich_text(code_content),
                    'language': language
                }
            }, lines_consumed
        else:
            # Return a list of code blocks by splitting at line boundaries
            blocks = []
            current_chunk = []
            current_len = 0

            for line in code_lines:
                line_len = len(line) + 1  # +1 for newline
                if current_len + line_len > MAX_CHARS and current_chunk:
                    # Flush current chunk
                    blocks.append({
                        'type': 'code',
                        'code': {
                            'rich_text': text_to_rich_text('\n'.join(current_chunk)),
                            'language': language
                        }
                    })
                    current_chunk = []
                    current_len = 0
                current_chunk.append(line)
                current_len += line_len

            # Add remaining chunk
            if current_chunk:
                blocks.append({
                    'type': 'code',
                    'code': {
                        'rich_text': text_to_rich_text('\n'.join(current_chunk)),
                        'language': language
                    }
                })

            # Return special marker for multiple blocks
            return {'_multi_blocks': blocks}, lines_consumed

    # Table (need to look ahead)
    if stripped.startswith('|') and stripped.endswith('|'):
        return parse_markdown_table(line, next_lines)

    # Default: paragraph
    return {
        'type': 'paragraph',
        'paragraph': {'rich_text': text_to_rich_text(stripped)}
    }, 1


def parse_markdown_table(first_line: str, next_lines: List[str]) -> Tuple[Dict, int]:
    """Parse a markdown table into Notion table block."""
    lines = [first_line]
    lines_consumed = 1

    if next_lines:
        for next_line in next_lines:
            if next_line.strip().startswith('|'):
                lines.append(next_line)
                lines_consumed += 1
            else:
                break

    # Parse table rows
    rows = []
    for i, line in enumerate(lines):
        # Skip separator line (|---|---|)
        if re.match(r'^\|[-:\s|]+\|$', line.strip()):
            continue

        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)

    if not rows:
        return {'type': 'paragraph', 'paragraph': {'rich_text': []}}, lines_consumed

    # Build table block
    table_width = max(len(row) for row in rows)
    table_rows = []

    for row in rows:
        # Pad row to table width
        while len(row) < table_width:
            row.append('')

        table_rows.append({
            'type': 'table_row',
            'table_row': {
                'cells': [text_to_rich_text(cell) for cell in row]
            }
        })

    return {
        'type': 'table',
        'table': {
            'table_width': table_width,
            'has_column_header': True,
            'has_row_header': False
        },
        '_children': table_rows  # Will need special handling during upload
    }, lines_consumed


def markdown_to_blocks(markdown: str) -> List[Dict]:
    """Convert markdown content (without frontmatter) to Notion blocks."""
    lines = markdown.split('\n')
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]
        next_lines = lines[i + 1:] if i + 1 < len(lines) else []

        block, consumed = markdown_line_to_block(line, next_lines)
        if block:
            # Handle multi-block returns (e.g., long code blocks split into multiple)
            if '_multi_blocks' in block:
                blocks.extend(block['_multi_blocks'])
            else:
                blocks.append(block)
        i += consumed

    return blocks


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, remaining_content)
    """
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        remaining = parts[2].strip()
        return frontmatter or {}, remaining
    except yaml.YAMLError:
        return {}, content


def markdown_file_to_notion(content: str) -> Tuple[Dict, List[Dict]]:
    """
    Convert a markdown file (with frontmatter) to Notion format.

    Args:
        content: Full markdown file content

    Returns:
        Tuple of (frontmatter_dict, blocks_list)
    """
    frontmatter, body = parse_frontmatter(content)

    # Clean up markdown formatting issues before conversion
    cleaned_body = clean_markdown(body)

    blocks = markdown_to_blocks(cleaned_body)

    return frontmatter, blocks


# ============================================================================
# Utilities
# ============================================================================

def flatten_blocks(blocks: List[Dict]) -> List[Dict]:
    """
    Flatten nested blocks for Notion API upload.

    Tables with _children need special handling - the children become
    separate append calls after the table is created.
    """
    result = []

    for block in blocks:
        block_copy = {k: v for k, v in block.items() if k != '_children'}

        if block.get('type') == 'table':
            # Tables need their rows as separate children
            result.append(block_copy)
            # Note: table rows must be appended separately after table creation
        else:
            result.append(block_copy)

    return result


def get_table_rows(block: Dict) -> List[Dict]:
    """Extract table rows from a table block."""
    if block.get('type') != 'table':
        return []
    return block.get('_children', [])
