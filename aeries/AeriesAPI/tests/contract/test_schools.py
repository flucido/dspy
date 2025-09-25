import pytest
from unittest.mock import patch
from src.services.schools_service import SchoolsService
from src.models.school import School

def test_get_schools_contract():
    """Test that GET /schools returns a list of school data as per contract."""
    # Mock the AeriesService to return sample School objects
    mock_schools = [
        School(id=1, name='Test School 1', address='123 Main St'),
        School(id=2, name='Test School 2', address='456 Oak Ave')
    ]
    
    with patch('src.services.schools_service.AeriesService') as mock_aeries:
        mock_aeries_instance = mock_aeries.return_value
        mock_aeries_instance.get_schools.return_value = mock_schools
        
        service = SchoolsService()
        data = service.get_schools()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(isinstance(item, dict) for item in data)
        assert all('id' in item for item in data)