from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class School:
    """Represents a school in the Aeries system.
    
    Attributes:
        id: Unique identifier for the school
        name: Name of the school
        address: Physical address of the school
        phone: Phone number of the school
    """
    id: int
    name: str
    address: str
    phone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the school to a dictionary.
        
        Returns:
            Dictionary representation of the school
        """
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'School':
        """Create a School instance from a dictionary.
        
        Args:
            data: Dictionary containing school data
            
        Returns:
            New School instance
        """
        return cls(
            id=data['id'],
            name=data['name'],
            address=data['address'],
            phone=data.get('phone')
        )