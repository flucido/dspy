from typing import List, Dict, Any
from src.services.aeries_service import AeriesService
from src.services.formatting_service import FormattingService
from src.models.student import Student

class StudentsService:
    """Service for handling students endpoint.
    
    Provides methods to retrieve and export student data from the Aeries API.
    """

    def __init__(self):
        """Initialize the StudentsService with required dependencies."""
        self.aeries_service = AeriesService()
        self.formatting_service = FormattingService()

    def get_students(self) -> List[Dict[str, Any]]:
        """Get all students.
        
        Returns:
            List of dictionaries containing student data
        """
        students = self.aeries_service.get_students()
        return [student.to_dict() for student in students]

    def export_students(self, format: str) -> str:
        """Export students to specified format.
        
        Args:
            format: Export format ('csv', 'excel', or 'pdf')
            
        Returns:
            Exported data as string (CSV) or bytes (Excel/PDF)
            
        Raises:
            ValueError: If the format is not supported
        """
        students = self.aeries_service.get_students()
        formatted_data = self.formatting_service.format_students(students)
        
        from src.services.export_service import ExportService
        export_service = ExportService()
        
        if format == 'csv':
            return export_service.export_to_csv(formatted_data)
        elif format == 'excel':
            return export_service.export_to_excel(formatted_data)
        elif format == 'pdf':
            return export_service.export_to_pdf(formatted_data)
        else:
            raise ValueError("Unsupported format")