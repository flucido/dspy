"""FastAPI wrapper for Ox-Turn Boustrophedon transformation service."""

import io
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Add parent directory to path for oxturn imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from oxturn.transformer import BoustrophedonTransformer, TransformMode
from oxturn.renderer.pdf import PDFRenderer
from oxturn.renderer.html import HTMLRenderer
from oxturn.renderer.epub import EPUBRenderer

app = FastAPI(
    title="Ox-Turn API",
    description="Boustrophedon text transformation service",
    version="0.1.0",
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF bytes using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="PDF support not available. Install pypdf: pip install pypdf",
        )

    try:
        reader = PdfReader(io.BytesIO(content))
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        if not text_parts:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. The file may be image-based or corrupted.",
            )

        return "\n\n".join(text_parts)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read PDF: {str(e)}",
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "oxturn-api"}


@app.post("/transform")
async def transform_document(
    file: UploadFile = File(..., description="Text or PDF file to transform"),
    output_format: str = Form("pdf", description="Output format: pdf, epub, or html"),
    mode: str = Form("dumb", description="Transformation mode: dumb or smart"),
    line_width: int = Form(80, ge=20, le=200, description="Characters per line"),
    font_size: int = Form(11, ge=8, le=24, description="Font size in points (PDF only)"),
    font_family: str = Form("Helvetica", description="Font family (PDF only)"),
    title: Optional[str] = Form(None, description="Document title"),
):
    """
    Transform a text or PDF file into Boustrophedon format.

    Accepts .txt or .pdf files and returns transformed document in the
    specified output format (pdf, epub, or html).
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename = file.filename.lower()
    if not (filename.endswith(".txt") or filename.endswith(".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a .txt or .pdf file.",
        )

    # Validate output format
    output_format = output_format.lower()
    if output_format not in {"pdf", "epub", "html"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported output format. Use pdf, epub, or html.",
        )

    # Validate mode
    try:
        transform_mode = TransformMode(mode.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Use 'dumb' or 'smart'.",
        )

    # Read file content
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB.",
        )

    # Extract text
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = content.decode("latin-1")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Could not decode text file. Please ensure it's UTF-8 or Latin-1 encoded.",
                )

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="File appears to be empty or contains no extractable text.",
        )

    # Determine title
    if not title:
        title = Path(file.filename).stem.replace("_", " ").replace("-", " ").title()

    try:
        transformer = BoustrophedonTransformer(
            line_width=line_width,
            mode=transform_mode,
        )
        result = transformer.transform(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transformation failed: {str(e)}",
        )

    output_buffer = io.BytesIO()
    media_type = ""
    extension = ""

    try:
        if output_format == "pdf":
            renderer = PDFRenderer(
                font_family=font_family,
                font_size=font_size,
            )
            renderer.render(result, output_buffer)
            media_type = "application/pdf"
            extension = "pdf"

        elif output_format == "epub":
            renderer = EPUBRenderer()
            renderer.render(result, output_buffer, title=title)
            media_type = "application/epub+zip"
            extension = "epub"

        elif output_format == "html":
            renderer = HTMLRenderer()
            html_content = renderer._generate_html(result, title=title)
            output_buffer.write(html_content.encode("utf-8"))
            media_type = "text/html"
            extension = "html"
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Rendering failed: {str(e)}",
        )

    output_buffer.seek(0)

    # Generate output filename
    output_filename = f"{Path(file.filename).stem}_boustrophedon.{extension}"

    return StreamingResponse(
        output_buffer,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{output_filename}"',
            "X-Lines-Transformed": str(len(result)),
            "X-Transform-Mode": transform_mode.value,
        },
    )


@app.post("/preview")
async def preview_transformation(
    file: UploadFile = File(..., description="Text or PDF file to preview"),
    mode: str = Form("dumb", description="Transformation mode: dumb or smart"),
    line_width: int = Form(80, ge=20, le=200, description="Characters per line"),
    max_lines: int = Form(20, ge=1, le=100, description="Maximum lines to preview"),
):
    """
    Preview the Boustrophedon transformation without generating a full document.

    Returns JSON with the first N transformed lines.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename = file.filename.lower()
    if not (filename.endswith(".txt") or filename.endswith(".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a .txt or .pdf file.",
        )

    # Validate mode
    try:
        transform_mode = TransformMode(mode.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode. Use 'dumb' or 'smart'.",
        )

    # Read file content
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB.",
        )

    # Extract text
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="replace")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="File appears to be empty or contains no extractable text.",
        )

    try:
        transformer = BoustrophedonTransformer(
            line_width=line_width,
            mode=transform_mode,
        )
        result = transformer.transform(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transformation failed: {str(e)}",
        )

    preview_lines = []
    for i, line in enumerate(result.lines[:max_lines]):
        preview_lines.append(
            {
                "text": line.display_text,
                "reversed": line.reversed,
                "original": line.text,
            }
        )

    return {
        "total_lines": len(result),
        "preview_lines": len(preview_lines),
        "mode": transform_mode.value,
        "line_width": line_width,
        "lines": preview_lines,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
