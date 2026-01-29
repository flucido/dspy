"""Command-line interface for Ox-Turn."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from oxturn import __version__
from oxturn.transformer import BoustrophedonTransformer, TransformMode
from oxturn.renderer.pdf import PDFRenderer
from oxturn.renderer.html import HTMLRenderer
from oxturn.renderer.epub import EPUBRenderer

app = typer.Typer(
    name="oxturn",
    help="Boustrophedon text transformation engine - alternating-direction text for focused reading.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"oxturn version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Ox-Turn: Transform text into Boustrophedon format."""
    pass


@app.command()
def convert(
    input_file: Path = typer.Argument(
        ...,
        help="Input text file to transform.",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path. Format determined by extension (.pdf, .epub, .html).",
    ),
    mode: str = typer.Option(
        "dumb",
        "--mode",
        "-m",
        help="Transformation mode: 'dumb' (character-count) or 'smart' (NLP-based).",
    ),
    line_width: int = typer.Option(
        80,
        "--line-width",
        "-w",
        help="Maximum characters per line.",
        min=20,
        max=200,
    ),
    font_size: int = typer.Option(
        11,
        "--font-size",
        "-s",
        help="Font size in points (PDF only).",
        min=8,
        max=24,
    ),
    font_family: str = typer.Option(
        "Helvetica",
        "--font-family",
        "-f",
        help="Font family (PDF: Helvetica, Times-Roman, Courier).",
    ),
    title: Optional[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="Document title (defaults to input filename).",
    ),
) -> None:
    """Transform a text file into Boustrophedon format.

    Examples:
        oxturn convert input.txt -o output.pdf
        oxturn convert input.txt -o output.epub --mode smart
        oxturn convert input.txt -o output.html --line-width 60
    """
    # Determine output path
    if output is None:
        output = input_file.with_suffix(".pdf")

    # Determine format from extension
    suffix = output.suffix.lower()
    if suffix not in {".pdf", ".epub", ".html"}:
        console.print(
            f"[red]Error:[/red] Unsupported output format '{suffix}'. "
            "Use .pdf, .epub, or .html"
        )
        raise typer.Exit(1)

    # Parse mode
    try:
        transform_mode = TransformMode(mode.lower())
    except ValueError:
        console.print(
            f"[red]Error:[/red] Invalid mode '{mode}'. Use 'dumb' or 'smart'."
        )
        raise typer.Exit(1)

    # Determine title
    if title is None:
        title = input_file.stem.replace("_", " ").replace("-", " ").title()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        # Read input
        progress.add_task("Reading input...", total=None)
        text = input_file.read_text(encoding="utf-8")

        # Transform
        progress.add_task("Transforming text...", total=None)
        transformer = BoustrophedonTransformer(
            line_width=line_width,
            mode=transform_mode,
        )
        result = transformer.transform(text)

        # Render
        progress.add_task(f"Rendering {suffix}...", total=None)

        if suffix == ".pdf":
            renderer = PDFRenderer(
                font_family=font_family,
                font_size=font_size,
            )
            renderer.render(result, output)

        elif suffix == ".epub":
            renderer = EPUBRenderer()
            renderer.render(result, output, title=title)

        elif suffix == ".html":
            renderer = HTMLRenderer()
            renderer.render(result, output, title=title)

    console.print(f"[green]✓[/green] Created {output}")
    console.print(f"  Lines: {len(result)}")
    console.print(f"  Mode: {transform_mode.value}")


@app.command()
def preview(
    input_file: Path = typer.Argument(
        ...,
        help="Input text file to preview.",
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    mode: str = typer.Option(
        "dumb",
        "--mode",
        "-m",
        help="Transformation mode: 'dumb' or 'smart'.",
    ),
    line_width: int = typer.Option(
        80,
        "--line-width",
        "-w",
        help="Maximum characters per line.",
        min=20,
        max=200,
    ),
    lines: int = typer.Option(
        20,
        "--lines",
        "-n",
        help="Number of lines to preview.",
        min=1,
        max=100,
    ),
) -> None:
    """Preview Boustrophedon transformation in the terminal.

    Examples:
        oxturn preview input.txt
        oxturn preview input.txt --mode smart --lines 30
    """
    # Parse mode
    try:
        transform_mode = TransformMode(mode.lower())
    except ValueError:
        console.print(
            f"[red]Error:[/red] Invalid mode '{mode}'. Use 'dumb' or 'smart'."
        )
        raise typer.Exit(1)

    text = input_file.read_text(encoding="utf-8")

    transformer = BoustrophedonTransformer(
        line_width=line_width,
        mode=transform_mode,
    )
    result = transformer.transform(text)

    console.print(f"\n[bold]Preview[/bold] ({transform_mode.value} mode, {line_width} chars/line)\n")
    console.print("─" * min(line_width, console.width))

    for i, line in enumerate(result.lines[:lines]):
        if line.reversed:
            # Right-align reversed lines
            console.print(f"[dim]{line.display_text:>{line_width}}[/dim]")
        else:
            console.print(line.display_text)

    if len(result) > lines:
        console.print(f"\n[dim]... and {len(result) - lines} more lines[/dim]")

    console.print("─" * min(line_width, console.width))


if __name__ == "__main__":
    app()
