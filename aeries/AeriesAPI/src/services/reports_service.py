from typing import List, Dict, Any
from src.services.aeries_service import AeriesService
from src.models.report import Report

class ReportsService:
    """Service for handling reports endpoint.
    
    Provides methods to retrieve report data from the Aeries API.
    """

    def __init__(self):
        """Initialize the ReportsService with required dependencies."""
        self.aeries_service = AeriesService()

    def get_reports(self) -> List[Dict[str, Any]]:
        """Get all reports.
        
        Returns:
            List of dictionaries containing report data
        """
        reports = self.aeries_service.get_reports()
        return [report.to_dict() for report in reports]