from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Report:
    """Represents a report in the Aeries system.
    
    Attributes:
        id: Unique identifier for the report
        name: Name of the report
        description: Description of the report
        type: Type of the report (e.g., summary, detailed)
    """
    id: int
    name: str
    description: str
    type: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the report to a dictionary.
        
        Returns:
            Dictionary representation of the report
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """Create a Report instance from a dictionary.
        
        Args:
            data: Dictionary containing report data
            
        Returns:
            New Report instance
        """
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            type=data['type']
        )