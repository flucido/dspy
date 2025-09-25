import pytest
import os
from unittest.mock import patch, Mock
from src.services.aeries_service import AeriesService
from src.services.formatting_service import FormattingService
from src.models.student import Student

def test_retrieve_student_data():
    """Test retrieving and formatting student data from Aeries."""
    # Set dummy environment variables for testing
    os.environ['AERIES_BASE_URL'] = 'https://dummy-url.com'
    os.environ['AERIES_CERT_PATH'] = '/dummy/path/cert.pem'
    os.environ['AERIES_KEY_PATH'] = '/dummy/path/key.pem'
    
    # Mock the requests.get to return sample data
    mock_students = [
        Student(id=1, name='John Doe', grade='10'),
        Student(id=2, name='Jane Smith', grade='11')
    ]
    
    with patch('src.services.aeries_service.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = [student.to_dict() for student in mock_students]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        aeries_service = AeriesService()
        formatting_service = FormattingService()
        
        # Retrieve student data
        student_data = aeries_service.get_students()
        
        assert isinstance(student_data, list)
        assert len(student_data) > 0
        assert all(isinstance(student, Student) for student in student_data)
        
        # Format the data
        formatted_data = formatting_service.format_students(student_data)
        
        assert isinstance(formatted_data, list)
        assert len(formatted_data) == len(student_data)