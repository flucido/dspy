import pytest
from src.services.export_service import ExportService

def test_export_to_pdf():
    """Test exporting student data to PDF."""
    pytest.importorskip("reportlab")
    # This test will fail until the export service is implemented
    export_service = ExportService()
    
    # Sample student data
    student_data = [
        {"id": 1, "name": "John Doe", "grade": "10"},
        {"id": 2, "name": "Jane Smith", "grade": "11"}
    ]
    
    # Export to PDF
    pdf_data = export_service.export_to_pdf(student_data)
    
    assert isinstance(pdf_data, bytes)
    assert len(pdf_data) > 0