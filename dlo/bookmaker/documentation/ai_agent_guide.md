# Ox-Turn Learning Engine: AI Agent Documentation

**Project Description:**
`oxturn` is a Boustrophedon text transformation engine. Boustrophedon writing alternates direction every line (Line 1: Left-to-Right, Line 2: Right-to-Left, etc.). This engine takes plain text input and converts it into PDF, EPUB, or HTML formats with this formatting applied to improve reading focus (based on ancient Greek styles).

---

## 1. Repository Structure

The project follows a standard Python package structure using `pyproject.toml` for configuration.

```text
bookmaker/
├── oxturn/                       # Main Package
│   ├── __init__.py
│   ├── cli.py                    # Entry point (Typer CLI App)
│   ├── transformer.py            # Core Logic (Text transformation)
│   └── renderer/                 # Output Generators
│       ├── __init__.py
│       ├── epub.py               # EPUB generation via ebooklib
│       ├── html.py               # HTML generation
│       └── pdf.py                # PDF generation via ReportLab
├── tests/                        # Test Suite
│   ├── __init__.py
│   └── test_transformer.py       # Logic verification
├── pyproject.toml                # Dependencies & Build Config
├── README.md                     # User documentation
└── plan.md                       # Development specifications
```

---

## 2. Development Flow & Logic

The application data flow is linear:
`Input File` → `CLI Parsing` → `Transformer` → `TransformResult` → `Renderer` → `Output File`

### Step 1: Transformation Core (`oxturn/transformer.py`)
This is the brain of the operation. It breaks text into lines and decides which ones to reverse.
- **Key Class:** `BoustrophedonTransformer`
- **Result Object:** `TransformResult` (iterable of `Line` objects)
- **Line Object:** `Line` contains the text, a boolean `reversed`, and a `display_text` property.
  - **Crucial Logic:** `Line.display_text` reverses the *order of words*, not the characters within the words (e.g., "Hello World" → "World Hello").

### Step 2: Rendering (`oxturn/renderer/`)
Renderers take the `TransformResult` and format it for specific files.
- **PDF (`pdf.py`):** Uses `reportlab`. Reversed lines are visually **Right-Aligned** to complete the reading effect.
- **HTML (`html.py`):** Wraps lines in `<p>` tags with CSS classes `.normal` or `.reversed`.
- **EPUB (`epub.py`):** Wraps the HTML renderer logic and packages it into an EPUB container using `ebooklib`.

---

## 3. Key Files & Implementation Details

### Legacy / Core Logic: `oxturn/transformer.py`
Responsible for converting raw strings into structured Boustrophedon lines.
- **Lines 13-22:** `reverse_word_order` function. Logic: `text.split()` → `reversed()` → `" ".join()`.
- **Lines 32-49:** `Line` dataclass.
- **Lines 67-87:** `BoustrophedonTransformer` class definition. Supports `DUMB` (char count) and `SMART` (NLP/Spacy) modes.

### CLI Entry Point: `oxturn/cli.py`
Handles argument parsing using `typer`.
- **Lines 47-97:** `convert` command arguments definition (`input_file`, `output`, `mode`, `line_width`, etc.).
- **Lines 138-150 (Inferred):** Sets up the correct renderer based on the file extension (`.pdf`, `.epub`, `.html`).

### Renderers:
1.  **`oxturn/renderer/pdf.py`**
    - **Lines 61-84:** Defines styles. `normal_style` uses `TA_JUSTIFY`, `reversed_style` uses `TA_RIGHT` (Right Align).
    - **Lines 88-110:** Iterates through lines. Uses `line.display_text` (reversed words) paired with `reversed_style` (right alignment) to achieve the boustrophedon effect.

2.  **`oxturn/renderer/epub.py`**
    - **Lines 51-93:** `render` method. Sets up book metadata, CSS, and chapter content. Uses `HTMLRenderer` internally to generate the chapter text.

3.  **`oxturn/renderer/html.py`**
    - **Lines 109-115:** CSS styling. `.boustrophedon-line.reversed` uses `text-align: right`, `.boustrophedon-line.normal` uses `text-align: justify`.
    - **Lines 140-153:** `render_fragment` method. Generates clean HTML paragraphs with boolean CSS classes for styling flexibility.

---

## 4. Dependencies

Defined in `pyproject.toml`.
- **Core:**
  - `typer`: CLI interface.
  - `rich`: Pretty terminal output.
  - `reportlab`: PDF generation.
  - `ebooklib`: EPUB generation.
- **Optional (`[npm]`):**
  - `spacy`: For "Smart" mode transformation (sentence boundary detection).

## 5. Usage Example for Agents

If you need to use this library programmatically to convert a string:

```python
from oxturn.transformer import BoustrophedonTransformer, TransformMode

# 1. Initialize Transformer
transformer = BoustrophedonTransformer(line_width=80, mode=TransformMode.DUMB)

# 2. Transform Text
raw_text = "This is line one. This will be line two."
result = transformer.transform(raw_text)

# 3. Iterate Results
for line in result.lines:
    # line.text is original
    # line.reversed is boolean
    # line.display_text is the render-ready string
    print(f"{'[R]' if line.reversed else '[L]'} {line.display_text}")
```
