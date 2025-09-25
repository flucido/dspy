import pytest
from unittest.mock import patch
from src.services.students_service import StudentsService
from src.models.student import Student

def test_get_students_contract():
    """Test that GET /students returns a list of student data as per contract."""
    # Mock the AeriesService to return sample Student objects
    mock_students = [
        Student(id=1, name='John Doe', grade='10'),
        Student(id=2, name='Jane Smith', grade='11')
    ]
    
    with patch('src.services.students_service.AeriesService') as mock_aeries:
        mock_aeries_instance = mock_aeries.return_value
        mock_aeries_instance.get_students.return_value = mock_students
        
        service = StudentsService()
        data = service.get_students()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(isinstance(item, dict) for item in data)
        assert all('id' in item for item in data)