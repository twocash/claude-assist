"""Test script for inline formatting parsing."""

import re
from converter import _parse_inline_formatting, text_to_rich_text, clean_markdown

# Test 1: Code detection
test_code = 'Here is `some code` in text'
result = _parse_inline_formatting(test_code)
print("Test 1 - Code:")
for seg in result:
    print(f"  {seg}")

# Test 2: Full inline formatting
test_full = '**Bold** and *italic* and `code` and [link](http://example.com) and ~~strike~~'
result = _parse_inline_formatting(test_full)
print("\nTest 2 - Full formatting:")
for seg in result:
    print(f"  {seg}")

# Test 3: Convert to rich_text
rich = text_to_rich_text(test_full)
print("\nTest 3 - Rich text output:")
for item in rich:
    text = item['text']['content']
    annot = item['annotations']
    link = item['text'].get('link', {}).get('url', '')
    flags = []
    if annot.get('bold'): flags.append('B')
    if annot.get('italic'): flags.append('I')
    if annot.get('code'): flags.append('C')
    if annot.get('strikethrough'): flags.append('S')
    if link: flags.append(f'L:{link}')
    print(f"  '{text}' [{','.join(flags) or 'plain'}]")

# Test 4: Table cleanup
test_table = """| **Header 1** | **Header 2** |

| --- | --- |

| Row 1 | Data 1 |

| Row 2 | Data 2 |
"""
cleaned = clean_markdown(test_table)
print("\nTest 4 - Table cleanup:")
print(cleaned)

if __name__ == '__main__':
    print("\n=== All tests complete ===")
