from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Student:
    """Represents a student in the Aeries system.
    
    Attributes:
        id: Unique identifier for the student
        name: Full name of the student
        grade: Grade level of the student
        school_id: ID of the school the student attends
        email: Email address of the student
        phone: Phone number of the student
    """
    id: int
    name: str
    grade: str
    school_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the student to a dictionary.
        
        Returns:
            Dictionary representation of the student
        """
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade,
            "school_id": self.school_id,
            "email": self.email,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Create a Student instance from a dictionary.
        
        Args:
            data: Dictionary containing student data
            
        Returns:
            New Student instance
        """
        return cls(
            id=data['id'],
            name=data['name'],
            grade=data['grade'],
            school_id=data.get('school_id'),
            email=data.get('email'),
            phone=data.get('phone')
        )