"""Test API error handling."""

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "oxturn-api"}


def test_transform_no_file():
    """Test transform with no file."""
    response = client.post("/transform")
    assert response.status_code == 422


def test_transform_invalid_file_type():
    """Test transform with invalid file type."""
    file_content = b"test content"
    files = {"file": ("test.jpg", io.BytesIO(file_content), "image/jpeg")}
    response = client.post("/transform", files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_transform_empty_file():
    """Test transform with empty text file."""
    files = {"file": ("test.txt", io.BytesIO(b""), "text/plain")}
    response = client.post("/transform", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_transform_invalid_mode():
    """Test transform with invalid mode."""
    file_content = b"This is a test."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    data = {"mode": "invalid_mode"}
    response = client.post("/transform", files=files, data=data)
    assert response.status_code == 400
    assert "Invalid mode" in response.json()["detail"]


def test_transform_invalid_output_format():
    """Test transform with invalid output format."""
    file_content = b"This is a test."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    data = {"output_format": "docx"}
    response = client.post("/transform", files=files, data=data)
    assert response.status_code == 400
    assert "Unsupported output format" in response.json()["detail"]


def test_transform_oversized_file():
    """Test transform with file exceeding size limit."""
    large_content = b"x" * (11 * 1024 * 1024)
    files = {"file": ("test.txt", io.BytesIO(large_content), "text/plain")}
    response = client.post("/transform", files=files)
    assert response.status_code == 400
    assert "too large" in response.json()["detail"].lower()


def test_transform_valid_txt_to_pdf():
    """Test valid transformation from txt to PDF."""
    file_content = b"This is a test of the boustrophedon transformation."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    data = {"output_format": "pdf", "mode": "dumb"}
    response = client.post("/transform", files=files, data=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_transform_valid_txt_to_html():
    """Test valid transformation from txt to HTML."""
    file_content = b"This is a test of the boustrophedon transformation."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    data = {"output_format": "html", "mode": "dumb"}
    response = client.post("/transform", files=files, data=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    html_content = response.content.decode("utf-8")
    assert "text-align: right" in html_content
    assert "boustrophedon-line" in html_content and "reversed" in html_content


def test_preview_valid():
    """Test valid preview request."""
    file_content = b"This is a test. This is another test."
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    data = {"mode": "dumb", "max_lines": 10}
    response = client.post("/preview", files=files, data=data)
    assert response.status_code == 200
    json_data = response.json()
    assert "lines" in json_data
    assert "total_lines" in json_data
    assert len(json_data["lines"]) > 0


if __name__ == "__main__":
    print("Running API error handling tests...")
    print("\n1. Testing health endpoint...")
    test_health_endpoint()
    print("   ✓ Health endpoint working")

    print("\n2. Testing invalid file type...")
    test_transform_invalid_file_type()
    print("   ✓ Invalid file type rejected")

    print("\n3. Testing empty file...")
    test_transform_empty_file()
    print("   ✓ Empty file rejected")

    print("\n4. Testing invalid mode...")
    test_transform_invalid_mode()
    print("   ✓ Invalid mode rejected")

    print("\n5. Testing invalid output format...")
    test_transform_invalid_output_format()
    print("   ✓ Invalid output format rejected")

    print("\n6. Testing oversized file...")
    test_transform_oversized_file()
    print("   ✓ Oversized file rejected")

    print("\n7. Testing valid txt to PDF...")
    test_transform_valid_txt_to_pdf()
    print("   ✓ Valid PDF transformation works")

    print("\n8. Testing valid txt to HTML...")
    test_transform_valid_txt_to_html()
    print("   ✓ Valid HTML transformation works with correct alignment")

    print("\n9. Testing valid preview...")
    test_preview_valid()
    print("   ✓ Valid preview works")

    print("\n✅ All API error handling tests passed!")
