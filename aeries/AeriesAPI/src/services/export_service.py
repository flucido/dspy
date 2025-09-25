import csv
import io
from typing import List, Dict, Any

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class ExportService:
    """Service for exporting data to various formats.
    
    Supports CSV, Excel, and PDF export formats. Some formats require
    additional dependencies (pandas for Excel, reportlab for PDF).
    """

    def export_to_csv(self, data: List[Dict[str, Any]]) -> str:
        """Export data to CSV format.
        
        Args:
            data: List of dictionaries to export
            
        Returns:
            CSV formatted string
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def export_to_excel(self, data: List[Dict[str, Any]]) -> bytes:
        """Export data to Excel format.
        
        Args:
            data: List of dictionaries to export
            
        Returns:
            Excel file as bytes
            
        Raises:
            ImportError: If pandas is not available
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is not available")
        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    def export_to_pdf(self, data: List[Dict[str, Any]]) -> bytes:
        """Export data to PDF format.
        
        Args:
            data: List of dictionaries to export
            
        Returns:
            PDF file as bytes
            
        Raises:
            ImportError: If reportlab is not available
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is not available")
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        y = 800
        for row in data:
            for key, value in row.items():
                p.drawString(100, y, f"{key}: {value}")
                y -= 20
            y -= 20
        p.showPage()
        p.save()
        return buffer.getvalue()