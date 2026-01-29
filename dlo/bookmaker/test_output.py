#!/usr/bin/env python3
"""Generate test outputs in HTML, EPUB, and PDF formats."""

import sys
sys.path.insert(0, '.')

from oxturn.transformer import BoustrophedonTransformer

# Read sample text
with open('sample.txt', 'r') as f:
    text = f.read()

# Transform
transformer = BoustrophedonTransformer(line_width=60)
result = transformer.transform(text)

# Generate HTML
html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Boustrophedon Text</title>
    <style>
        body { font-family: Georgia, serif; font-size: 16px; line-height: 1.8; max-width: 800px; margin: 40px auto; padding: 20px; }
        .line { margin: 0; padding: 0; }
        .rtl { direction: rtl; text-align: right; }
        .ltr { direction: ltr; text-align: left; }
    </style>
</head>
<body>
"""
for line in result.lines:
    direction_class = 'rtl' if line.reversed else 'ltr'
    html += f'    <p class="line {direction_class}">{line.display_text}</p>\n'

html += """</body>
</html>"""

with open('sample_output.html', 'w') as f:
    f.write(html)
print('HTML saved to sample_output.html')

# Preview
print()
print('Preview (first 8 lines):')
for i, line in enumerate(result.lines[:8]):
    direction = '←' if line.reversed else '→'
    print(f'{direction} {line.display_text}')
