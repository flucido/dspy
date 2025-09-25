from typing import List, Dict, Any
from src.services.aeries_service import AeriesService
from src.models.school import School

class SchoolsService:
    """Service for handling schools endpoint.
    
    Provides methods to retrieve school data from the Aeries API.
    """

    def __init__(self):
        """Initialize the SchoolsService with required dependencies."""
        self.aeries_service = AeriesService()

    def get_schools(self) -> List[Dict[str, Any]]:
        """Get all schools.
        
        Returns:
            List of dictionaries containing school data
        """
        schools = self.aeries_service.get_schools()
        return [school.to_dict() for school in schools]