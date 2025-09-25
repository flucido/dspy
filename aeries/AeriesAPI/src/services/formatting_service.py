from typing import List, Dict, Any
from src.models.student import Student

class FormattingService:
    """Service for formatting data for export.
    
    This service handles the conversion of model objects to dictionaries
    suitable for export to various formats.
    """

    def format_students(self, students: List[Student]) -> List[Dict[str, Any]]:
        """Format student data for export.
        
        Args:
            students: List of Student objects to format
            
        Returns:
            List of dictionaries representing the formatted student data
        """
        return [student.to_dict() for student in students]