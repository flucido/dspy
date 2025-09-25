import pytest
import os
from unittest.mock import patch, Mock
from src.services.aeries_service import AeriesService
from src.services.formatting_service import FormattingService
from src.services.export_service import ExportService
from src.models.student import Student
from src.models.school import School
from src.models.report import Report

def test_aeries_service_missing_env_vars():
    """Test AeriesService with missing environment variables."""
    # Clear environment variables
    original_env = dict(os.environ)
    for key in ['AERIES_BASE_URL', 'AERIES_CERT_PATH', 'AERIES_KEY_PATH']:
        os.environ.pop(key, None)
    
    try:
        service = AeriesService()
        with pytest.raises(ValueError, match="Missing required environment variables"):
            service.get_students()
    finally:
        os.environ.update(original_env)

def test_formatting_service():
    """Test FormattingService."""
    service = FormattingService()
    students = [
        Student(id=1, name="John Doe", grade="10"),
        Student(id=2, name="Jane Smith", grade="11")
    ]
    
    formatted = service.format_students(students)
    
    assert isinstance(formatted, list)
    assert len(formatted) == 2
    assert formatted[0]["name"] == "John Doe"
    assert formatted[1]["name"] == "Jane Smith"

def test_export_service_csv():
    """Test ExportService CSV export."""
    service = ExportService()
    data = [
        {"id": 1, "name": "John Doe", "grade": "10"},
        {"id": 2, "name": "Jane Smith", "grade": "11"}
    ]
    
    csv_output = service.export_to_csv(data)
    
    assert isinstance(csv_output, str)
    assert "John Doe" in csv_output
    assert "Jane Smith" in csv_output
    assert "id,name,grade" in csv_output

def test_export_service_empty_data():
    """Test ExportService with empty data."""
    service = ExportService()
    csv_output = service.export_to_csv([])
    
    assert csv_output == ""

def test_aeries_service_with_mock():
    """Test AeriesService with mocked requests."""
    os.environ['AERIES_BASE_URL'] = 'https://dummy-url.com'
    os.environ['AERIES_CERT_PATH'] = '/dummy/path/cert.pem'
    os.environ['AERIES_KEY_PATH'] = '/dummy/path/key.pem'
    
    mock_students = [
        Student(id=1, name='John Doe', grade='10'),
        Student(id=2, name='Jane Smith', grade='11')
    ]
    
    with patch('src.services.aeries_service.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [student.to_dict() for student in mock_students]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        service = AeriesService()
        students = service.get_students()
        
        assert isinstance(students, list)
        assert len(students) == 2
        assert all(isinstance(student, Student) for student in students)
        assert students[0].name == "John Doe"