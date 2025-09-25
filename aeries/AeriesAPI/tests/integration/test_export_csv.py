import pytest
from src.services.export_service import ExportService

def test_export_to_csv():
    """Test exporting student data to CSV."""
    # This test will fail until the export service is implemented
    export_service = ExportService()
    
    # Sample student data
    student_data = [
        {"id": 1, "name": "John Doe", "grade": "10"},
        {"id": 2, "name": "Jane Smith", "grade": "11"}
    ]
    
    # Export to CSV
    csv_data = export_service.export_to_csv(student_data)
    
    assert isinstance(csv_data, str)
    assert "John Doe" in csv_data
    assert "Jane Smith" in csv_data