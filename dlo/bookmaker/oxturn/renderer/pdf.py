"""PDF renderer using ReportLab."""

from pathlib import Path
from typing import BinaryIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from oxturn.transformer import TransformResult, Line


class PDFRenderer:
    """Render Boustrophedon text to PDF using ReportLab."""

    def __init__(
        self,
        font_family: str = "Helvetica",
        font_size: int = 11,
        line_spacing: float = 1.5,
        margin: float = 1.0,
    ) -> None:
        """Initialize PDF renderer.

        Args:
            font_family: Font family name (Helvetica, Times-Roman, Courier).
            font_size: Font size in points.
            line_spacing: Line spacing multiplier.
            margin: Page margin in inches.
        """
        self.font_family = font_family
        self.font_size = font_size
        self.line_spacing = line_spacing
        self.margin = margin

    def render(self, result: TransformResult, output: str | Path | BinaryIO) -> None:
        """Render transformed text to PDF.

        Args:
            result: The Boustrophedon transformation result.
            output: Output file path or file-like object.
        """
        if isinstance(output, (str, Path)):
            output = str(output)

        doc = SimpleDocTemplate(
            output,
            pagesize=letter,
            leftMargin=self.margin * inch,
            rightMargin=self.margin * inch,
            topMargin=self.margin * inch,
            bottomMargin=self.margin * inch,
        )

        styles = getSampleStyleSheet()

        # Style for normal (left-to-right) lines
        normal_style = ParagraphStyle(
            "BoustrophedonNormal",
            parent=styles["Normal"],
            fontName=self.font_family,
            fontSize=self.font_size,
            leading=self.font_size * self.line_spacing,
            alignment=TA_JUSTIFY,  # Justified
            firstLineIndent=0,
            leftIndent=0,
            rightIndent=0,
        )

        # Style for reversed (right-to-left) lines
        reversed_style = ParagraphStyle(
            "BoustrophedonReversed",
            parent=styles["Normal"],
            fontName=self.font_family,
            fontSize=self.font_size,
            leading=self.font_size * self.line_spacing,
            alignment=TA_RIGHT,
            firstLineIndent=0,
            leftIndent=0,
            rightIndent=0,
        )

        story: list = []

        for line in result.lines:
            # Handle headers/chapters extra spacing
            if line.is_new_paragraph:
                # If it's a chapter header (starts with CHAPTER or similar)
                # We add a 2-line break.
                # Assuming dumb mode keeps "CHAPTER I." as the text.
                if line.text.strip().upper().startswith("CHAPTER"):
                    story.append(Spacer(1, 2 * self.font_size * self.line_spacing))
                # Note: User request "No indents, just at chapters. Let's do a two-space break."
                # We implemented "No indents" via style.
                # We implement "at chapters... two-space break" here.
                # We do NOT add spacers for normal paragraphs, so they form a block.

            display_text = line.display_text

            # Escape special characters for ReportLab
            display_text = (
                display_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )

            if line.reversed:
                para = Paragraph(display_text, reversed_style)
            else:
                para = Paragraph(display_text, normal_style)

            story.append(para)

        doc.build(story)

    def render_low_level(self, result: TransformResult, output: str | Path) -> None:
        """Render using low-level canvas API for precise character control.

        Use this method when you need pixel-perfect positioning of reversed text.

        Args:
            result: The Boustrophedon transformation result.
            output: Output file path.
        """
        output = str(output)
        c = canvas.Canvas(output, pagesize=letter)
        width, height = letter

        x_margin = self.margin * inch
        y_start = height - self.margin * inch
        line_height = self.font_size * self.line_spacing

        c.setFont(self.font_family, self.font_size)

        y = y_start
        page_bottom = self.margin * inch

        for line in result.lines:
            if y < page_bottom:
                c.showPage()
                c.setFont(self.font_family, self.font_size)
                y = y_start

            display_text = line.display_text

            if line.reversed:
                # Right-align reversed text
                text_width = c.stringWidth(display_text, self.font_family, self.font_size)
                x = width - x_margin - text_width
            else:
                x = x_margin

            c.drawString(x, y, display_text)
            y -= line_height

        c.save()
