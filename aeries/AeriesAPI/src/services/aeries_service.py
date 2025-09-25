import os
import requests
import logging
from typing import List, Dict, Any
from src.models.student import Student
from src.models.school import School
from src.models.report import Report

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AeriesService:
    """Service for interacting with the Aeries API.
    
    This service handles authentication and communication with the Aeries API
    using client certificates for secure access.
    
    Attributes:
        base_url: Base URL for the Aeries API
        cert_path: Path to the client certificate file
        key_path: Path to the private key file
    """

    def __init__(self):
        """Initialize the AeriesService with environment configuration."""
        self.base_url = os.getenv('AERIES_BASE_URL')
        self.cert_path = os.getenv('AERIES_CERT_PATH')
        self.key_path = os.getenv('AERIES_KEY_PATH')

    def get_students(self) -> List[Student]:
        """Retrieve student data from Aeries.
        
        Returns:
            List of Student objects
            
        Raises:
            ValueError: If required environment variables are missing
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.base_url or not self.cert_path or not self.key_path:
            error_msg = "Missing required environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            url = f"{self.base_url}/students"
            logger.info(f"Making request to {url}")
            response = requests.get(url, cert=(self.cert_path, self.key_path))
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully retrieved {len(data)} students")
            return [Student.from_dict(item) for item in data]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving students: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving students: {e}")
            raise

    def get_schools(self) -> List[School]:
        """Retrieve school data from Aeries.
        
        Returns:
            List of School objects
            
        Raises:
            ValueError: If required environment variables are missing
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.base_url or not self.cert_path or not self.key_path:
            error_msg = "Missing required environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            url = f"{self.base_url}/schools"
            logger.info(f"Making request to {url}")
            response = requests.get(url, cert=(self.cert_path, self.key_path))
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully retrieved {len(data)} schools")
            return [School.from_dict(item) for item in data]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving schools: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving schools: {e}")
            raise

    def get_reports(self) -> List[Report]:
        """Retrieve report data from Aeries.
        
        Returns:
            List of Report objects
            
        Raises:
            ValueError: If required environment variables are missing
            requests.exceptions.RequestException: If the API request fails
        """
        if not self.base_url or not self.cert_path or not self.key_path:
            error_msg = "Missing required environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            url = f"{self.base_url}/reports"
            logger.info(f"Making request to {url}")
            response = requests.get(url, cert=(self.cert_path, self.key_path))
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully retrieved {len(data)} reports")
            return [Report.from_dict(item) for item in data]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving reports: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving reports: {e}")
            raise