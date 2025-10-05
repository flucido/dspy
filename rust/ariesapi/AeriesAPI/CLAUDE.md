# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based backend API for retrieving and exporting data from the Aeries school information system. The project provides a modular interface to fetch student, school, and report data with proper error handling, logging, and export capabilities to CSV, Excel, and PDF formats.

## Architecture

### Three-Layer Service Architecture

1. **AeriesService** (`src/services/aeries_service.py`): Core API communication layer that handles certificate-based authentication and all HTTP requests to the Aeries API. All API calls go through this service.

2. **Domain Services**: Business logic layer with specialized services:
   - `StudentsService`: Student data operations
   - `SchoolsService`: School data operations
   - `ReportsService`: Report data operations
   - `FormattingService`: Data transformation and formatting

3. **ExportService** (`src/services/export_service.py`): Handles data serialization to CSV, Excel (openpyxl), and PDF (reportlab) formats.

### Data Models

All models inherit from a base structure and provide `from_dict()` class methods for deserialization:
- `Student`: State ID, School ID, First/Last name, Birth date, attendance, grades, test scores
- `School`: Demographics and attendance summaries
- `Report`: Aggregated data from students and schools

### Authentication

Certificate-based authentication is used for all API requests. Three environment variables are required:
- `AERIES_BASE_URL`: Base URL for the Aeries API
- `AERIES_CERT_PATH`: Path to client certificate (.pem)
- `AERIES_KEY_PATH`: Path to private key file

These are loaded in `AeriesService.__init__()` and validated before each API call.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env from .env.example)
export AERIES_BASE_URL="https://your-aeries-instance.com"
export AERIES_CERT_PATH="/path/to/certificate.pem"
export AERIES_KEY_PATH="/path/to/private-key.pem"
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test suites
pytest tests/unit/            # Unit tests
pytest tests/contract/        # API contract tests
pytest tests/integration/     # Integration tests (export functionality)

# Run a single test file
pytest tests/unit/test_services.py

# Run with verbose output
pytest -v tests/
```

### Code Quality
```bash
# Format code (Black)
black src/ tests/

# Lint code (Flake8)
flake8 src/ tests/
```

### CLI Usage
```bash
# Export student data
python -m src.cli.export_commands --format csv --output students
python -m src.cli.export_commands --format excel --output students
python -m src.cli.export_commands --format pdf --output students
```

## Testing Strategy

Three distinct test layers mirror the architecture:

1. **Unit tests** (`tests/unit/`): Test individual services and models in isolation
2. **Contract tests** (`tests/contract/`): Validate API responses against expected schemas defined in `specs/001-use-both-the/contracts/*.yaml`
3. **Integration tests** (`tests/integration/`): Test the full pipeline including export to files

## Important Patterns

### Error Handling
All services validate environment variables before making API calls and raise `ValueError` for missing configuration. API errors are caught as `requests.exceptions.RequestException` and logged before re-raising.

### Logging
The codebase uses Python's built-in `logging` module. Each service sets up its own logger with `logging.getLogger(__name__)`. Log at INFO level for successful operations and ERROR level for failures.

### Data Flow
```
AeriesService → Domain Service → FormattingService → ExportService → File Output
```

## Specification-Driven Development

The `specs/001-use-both-the/` directory contains the feature specification, data models, and API contracts. When implementing new features:
1. Start with the spec document to understand requirements
2. Check the data model for entity relationships
3. Refer to contract YAML files for expected API response structures
