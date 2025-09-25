import pytest
from unittest.mock import patch
from src.services.reports_service import ReportsService
from src.models.report import Report

def test_get_reports_contract():
    """Test that GET /reports returns a list of reports as per contract."""
    # Mock the AeriesService to return sample Report objects
    mock_reports = [
        Report(id=1, name='Test Report 1', description='Summary report', type='summary'),
        Report(id=2, name='Test Report 2', description='Detailed report', type='detailed')
    ]
    
    with patch('src.services.reports_service.AeriesService') as mock_aeries:
        mock_aeries_instance = mock_aeries.return_value
        mock_aeries_instance.get_reports.return_value = mock_reports
        
        service = ReportsService()
        data = service.get_reports()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(isinstance(item, dict) for item in data)
        assert all('id' in item for item in data)