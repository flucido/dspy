import pytest
from src.services.export_service import ExportService

def test_export_to_excel():
    """Test exporting student data to Excel."""
    pytest.importorskip("pandas")
    # This test will fail until the export service is implemented
    export_service = ExportService()
    
    # Sample student data
    student_data = [
        {"id": 1, "name": "John Doe", "grade": "10"},
        {"id": 2, "name": "Jane Smith", "grade": "11"}
    ]
    
    # Export to Excel
    excel_data = export_service.export_to_excel(student_data)
    
    assert isinstance(excel_data, bytes)
    assert len(excel_data) > 0