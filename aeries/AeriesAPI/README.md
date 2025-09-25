# Aeries API Backend

A reliable backend API for retrieving and exporting data from the Aeries school information system.

## Overview

### Purpose and Scope
This project provides a clean, modular backend interface to the Aeries API, enabling developers to retrieve student, school, and report data with proper error handling, logging, and export capabilities. The system supports multiple output formats (CSV, Excel, PDF) and follows best practices for security, testing, and maintainability.

### Key Features
- **Data Retrieval**: Fetch students, schools, and reports from Aeries API
- **Data Export**: Export data to CSV, Excel, and PDF formats
- **Error Handling**: Comprehensive logging and error management
- **Testing**: Full test coverage with contract, integration, and unit tests
- **Security**: Environment-based configuration (no hardcoded secrets)
- **Modular Design**: Clean separation of concerns with services and models

## Installation and Setup

### Prerequisites
- Python 3.7+
- Access to Aeries API with valid credentials

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AeriesAPI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export AERIES_BASE_URL="https://your-aeries-instance.com"
   export AERIES_CERT_PATH="/path/to/certificate.pem"
   export AERIES_KEY_PATH="/path/to/private-key.pem"
   ```

## Usage

### Command Line Interface
Use the CLI to export data:

```bash
# Export student data to CSV
python -m src.cli.export_commands export students csv

# Export school data to Excel
python -m src.cli.export_commands export schools excel

# Export reports to PDF
python -m src.cli.export_commands export reports pdf
```

### Programmatic Usage
```python
from src.services.students_service import StudentsService
from src.services.schools_service import SchoolsService
from src.services.reports_service import ReportsService

# Get student data
students_service = StudentsService()
students = students_service.get_students()

# Get school data
schools_service = SchoolsService()
schools = schools_service.get_schools()

# Get report data
reports_service = ReportsService()
reports = reports_service.get_reports()

# Export data
export_service = ExportService()
csv_data = export_service.export_to_csv(students)
```

### API Endpoints
The system provides the following endpoints:
- `GET /students` - Retrieve all students
- `GET /schools` - Retrieve all schools  
- `GET /reports` - Retrieve all reports

## Project Structure
```
AeriesAPI/
├── src/
│   ├── cli/           # Command-line interface
│   ├── models/        # Data models (Student, School, Report)
│   └── services/      # Business logic services
├── tests/
│   ├── contract/      # Contract tests
│   ├── integration/   # Integration tests
│   └── unit/          # Unit tests
├── specs/             # Feature specifications
└── README.md
```

## Testing
Run the test suite:
```bash
pytest tests/
```

Run specific test types:
```bash
pytest tests/unit/        # Unit tests
pytest tests/contract/    # Contract tests
pytest tests/integration/ # Integration tests
```

## Configuration
The application uses environment variables for configuration:
- `AERIES_BASE_URL`: Base URL for the Aeries API
- `AERIES_CERT_PATH`: Path to the client certificate
- `AERIES_KEY_PATH`: Path to the private key

## Security
- No hardcoded secrets in the codebase
- All sensitive configuration via environment variables
- Certificate-based authentication for API access
- Comprehensive error handling to prevent information leakage

## Development
1. Create a new feature branch
2. Write tests first (TDD approach)
3. Implement the feature
4. Run tests and linting
5. Update documentation
6. Submit a pull request

## License
No license specified.