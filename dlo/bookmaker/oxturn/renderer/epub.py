"""EPUB renderer for Boustrophedon text."""

from pathlib import Path
from typing import BinaryIO
import uuid

from ebooklib import epub

from oxturn.transformer import TransformResult
from oxturn.renderer.html import HTMLRenderer


class EPUBRenderer:
    """Render Boustrophedon text to EPUB format."""

    def __init__(
        self,
        font_family: str = "Georgia, serif",
        font_size: str = "1em",
        line_height: str = "1.8",
    ) -> None:
        """Initialize EPUB renderer.

        Args:
            font_family: CSS font-family value.
            font_size: CSS font-size value.
            line_height: CSS line-height value.
        """
        self.font_family = font_family
        self.font_size = font_size
        self.line_height = line_height
        self._html_renderer = HTMLRenderer(font_family, font_size, line_height)

    def render(
        self,
        result: TransformResult,
        output: str | Path | BinaryIO,
        title: str = "Boustrophedon Text",
        author: str = "Ox-Turn Engine",
        language: str = "en",
    ) -> None:
        """Render transformed text to EPUB file.

        Args:
            result: The Boustrophedon transformation result.
            output: Output file path or file-like object.
            title: Book title.
            author: Book author.
            language: Book language code.
        """
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(str(uuid.uuid4()))
        book.set_title(title)
        book.set_language(language)
        book.add_author(author)

        # Create CSS
        css_content = self._generate_css()
        css = epub.EpubItem(
            uid="style",
            file_name="style/main.css",
            media_type="text/css",
            content=css_content.encode("utf-8"),
        )
        book.add_item(css)

        # Create main content chapter
        chapter = epub.EpubHtml(
            title=title,
            file_name="content.xhtml",
            lang=language,
        )

        # Generate content - must be bytes for ebooklib
        content_html = self._generate_content(result, title)
        chapter.content = content_html.encode("utf-8")
        chapter.add_item(css)

        book.add_item(chapter)

        # Add navigation
        book.toc = [chapter]
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define spine
        book.spine = ["nav", chapter]

        # Write to file
        if isinstance(output, (str, Path)):
            epub.write_epub(str(output), book, {})
        else:
            # For file-like objects, write to temp and read back
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp:
                tmp_path = tmp.name

            try:
                epub.write_epub(tmp_path, book, {})
                with open(tmp_path, "rb") as f:
                    output.write(f.read())
            finally:
                os.unlink(tmp_path)

    def _generate_css(self) -> str:
        """Generate CSS for EPUB."""
        return f"""
body {{
    font-family: {self.font_family};
    font-size: {self.font_size};
    line-height: {self.line_height};
    margin: 1em;
}}

h1 {{
    text-align: center;
    margin-bottom: 2em;
}}

.boustrophedon-container {{
    margin: 0;
    padding: 0;
}}

.chapter-spacer {{
    height: 3em;
}}

.boustrophedon-line {{
    margin: 0;
    padding: 0.25em 0;
}}

.boustrophedon-line.reversed {{
    text-align: justify;
}}

.boustrophedon-line.normal {{
    text-align: justify;
}}
"""

    def _generate_content(self, result: TransformResult, title: str) -> str:
        """Generate XHTML content for EPUB."""
        fragment = self._html_renderer.render_fragment(result)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>{self._escape_html(title)}</title>
    <link rel="stylesheet" type="text/css" href="style/main.css"/>
</head>
<body>
    <h1>{self._escape_html(title)}</h1>
    <div class="boustrophedon-container">
{fragment}
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
