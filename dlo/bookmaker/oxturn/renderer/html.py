"""HTML renderer for Boustrophedon text."""

from pathlib import Path
from typing import TextIO

from oxturn.transformer import TransformResult


class HTMLRenderer:
    """Render Boustrophedon text to HTML."""

    def __init__(
        self,
        font_family: str = "Georgia, serif",
        font_size: str = "16px",
        line_height: str = "1.8",
    ) -> None:
        """Initialize HTML renderer.

        Args:
            font_family: CSS font-family value.
            font_size: CSS font-size value.
            line_height: CSS line-height value.
        """
        self.font_family = font_family
        self.font_size = font_size
        self.line_height = line_height

    def render(
        self,
        result: TransformResult,
        output: str | Path | TextIO,
        title: str = "Boustrophedon Text",
    ) -> None:
        """Render transformed text to HTML file.

        Args:
            result: The Boustrophedon transformation result.
            output: Output file path or file-like object.
            title: HTML document title.
        """
        html = self._generate_html(result, title)

        if isinstance(output, (str, Path)):
            with open(output, "w", encoding="utf-8") as f:
                f.write(html)
        else:
            output.write(html)

    def render_fragment(self, result: TransformResult) -> str:
        """Render just the content as an HTML fragment (no full document).

        Args:
            result: The Boustrophedon transformation result.

        Returns:
            HTML fragment string.
        """
        lines_html: list[str] = []

        for line in result.lines:
            # Handle chapters spacing
            if line.is_new_paragraph:
                # Assuming simple check similar to PDF renderer
                if line.text.strip().upper().startswith("CHAPTER"):
                    lines_html.append('<div class="chapter-spacer"></div>')

            display_text = self._escape_html(line.display_text)

            if line.reversed:
                lines_html.append(f'<p class="boustrophedon-line reversed">{display_text}</p>')
            else:
                lines_html.append(f'<p class="boustrophedon-line normal">{display_text}</p>')

        return "\n".join(lines_html)

    def _generate_html(self, result: TransformResult, title: str) -> str:
        """Generate complete HTML document."""
        content = self.render_fragment(result)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._escape_html(title)}</title>
    <style>
        body {{
            font-family: {self.font_family};
            font-size: {self.font_size};
            line-height: {self.line_height};
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
            background: #fefefe;
            color: #333;
        }}
        .boustrophedon-container {{
            border-left: 3px solid #e0e0e0;
            padding-left: 1rem;
        }}
        .chapter-spacer {{
            height: 3em;
        }}
        .boustrophedon-line {{
            margin: 0;
            padding: 0.25em 0;
        }}
        .boustrophedon-line.reversed {{
            text-align: right;
            color: #444;
        }}
        .boustrophedon-line.normal {{
            text-align: justify;
        }}
        @media (prefers-color-scheme: dark) {{
            body {{
                background: #1a1a1a;
                color: #e0e0e0;
            }}
            .boustrophedon-container {{
                border-left-color: #444;
            }}
            .boustrophedon-line.reversed {{
                color: #ccc;
            }}
        }}
    </style>
</head>
<body>
    <h1>{self._escape_html(title)}</h1>
    <div class="boustrophedon-container">
{content}
    </div>
</body>
</html>
"""

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )
