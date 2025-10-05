# Data Model: Reliable Backend API for Aeries Data Retrieval

## Entities

### Student Data
- State ID: string, unique
- School ID: string
- First name: string
- Last name: string
- Birth date: date
- Attendance: list of records
- Grades: list of records
- Test scores: list of records

Relationships: Belongs to School Data.

Validation: State ID must be unique.

### School Data
- Demographics: dict
- Attendance summaries: dict

Relationships: Has many Student Data.

### Report
- Aggregated data: dict

Relationships: Generated from Student Data and School Data.
