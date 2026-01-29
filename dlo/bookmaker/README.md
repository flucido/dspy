# Ox-Turn Learning Engine

**Boustrophedon text transformation engine** — alternating-direction text for focused reading.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is Boustrophedon?

*Boustrophedon* (from Greek βουστροφηδόν, "ox-turning") is a style of writing where alternate lines run in opposite directions. Ancient Greeks used this pattern, and modern research suggests it can improve reading speed by reducing eye movement.

```
This line reads left to right, as normal.
                    .thgir ot tfel ,desrever si eno sihT
And this one goes left to right again.
```

## Installation

```bash
# Using uv (recommended)
uv sync

# Or with pip
pip install -e .

# For smart mode (NLP-based line breaking)
pip install -e ".[nlp]"
python -m spacy download en_core_web_sm
```

## Quick Start

```bash
# Convert a text file to PDF
oxturn convert input.txt -o output.pdf

# Convert to EPUB for e-readers
oxturn convert input.txt -o output.epub

# Preview in terminal
oxturn preview input.txt

# Use smart mode (NLP-based line breaking)
oxturn convert input.txt -o output.pdf --mode smart
```

## CLI Options

```bash
oxturn convert [OPTIONS] INPUT_FILE

Options:
  -o, --output PATH       Output file (.pdf, .epub, .html)
  -m, --mode TEXT         'dumb' or 'smart' [default: dumb]
  -w, --line-width INT    Characters per line [default: 80]
  -s, --font-size INT     Font size in points [default: 11]
  -f, --font-family TEXT  Font family [default: Helvetica]
  -t, --title TEXT        Document title
  -V, --version           Show version
  --help                  Show help
```

## Python API

```python
from oxturn import BoustrophedonTransformer
from oxturn.renderer import PDFRenderer

# Transform text
transformer = BoustrophedonTransformer(
    line_width=80,
    mode="dumb",  # or "smart" for NLP-based
)
result = transformer.transform("Your text here...")

# Render to PDF
renderer = PDFRenderer(font_size=12)
renderer.render(result, "output.pdf")

# Access individual lines
for line in result:
    print(line.display_text)
    print(f"  Reversed: {line.reversed}")
```

## Transformation Modes

### Dumb Mode (Default)
Simple character-count based line wrapping. Fast and predictable.

### Smart Mode
Uses spaCy NLP to break lines at natural pauses (sentence boundaries, clauses). Produces more readable output but requires the `nlp` extra.

## Development

```bash
# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Type checking
uv run mypy oxturn

# Linting
uv run ruff check oxturn
```

## License

MIT License — see [LICENSE](LICENSE) for details.
