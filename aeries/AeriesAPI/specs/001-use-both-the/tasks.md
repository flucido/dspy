# Tasks: Reliable Backend API for Aeries Data Retrieval

**Input**: Design documents from `/specs/001-use-both-the/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan: src/models/, src/services/, src/cli/, src/lib/, tests/contract/, tests/integration/, tests/unit/
- [ ] T002 Initialize Python project with dependencies: requests, pandas, pymssql, pytest, openpyxl, reportlab
- [ ] T003 [P] Configure linting and formatting tools (flake8, black)
- [ ] T004 [P] Set up environment variables for Aeries API certificate and base URL

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T005 [P] Contract test GET /reports in tests/contract/test_reports.py
- [ ] T006 [P] Contract test GET /schools in tests/contract/test_schools.py
- [ ] T007 [P] Contract test GET /students in tests/contract/test_students.py
- [ ] T008 [P] Integration test for retrieving student data in tests/integration/test_students.py
- [ ] T009 [P] Integration test for exporting to CSV in tests/integration/test_export_csv.py
- [ ] T010 [P] Integration test for exporting to Excel in tests/integration/test_export_excel.py
- [ ] T011 [P] Integration test for exporting to PDF in tests/integration/test_export_pdf.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T012 [P] Student model in src/models/student.py
- [ ] T013 [P] School model in src/models/school.py
- [ ] T014 [P] Report model in src/models/report.py
- [ ] T015 [P] Aeries API service in src/services/aeries_service.py
- [ ] T016 [P] Data formatting service in src/services/formatting_service.py
- [ ] T017 [P] Export service in src/services/export_service.py
- [ ] T018 [P] CLI commands for export in src/cli/export_commands.py
- [ ] T019 Implement GET /reports endpoint in src/services/reports_service.py
- [ ] T020 Implement GET /schools endpoint in src/services/schools_service.py
- [ ] T021 Implement GET /students endpoint in src/services/students_service.py

## Phase 3.4: Integration
- [ ] T022 Connect services to Aeries API using certificate and base URL
- [ ] T023 Error handling and logging for API calls
- [ ] T024 Security: ensure no hardcoded secrets, use env vars

## Phase 3.5: Polish
- [ ] T025 [P] Unit tests for models in tests/unit/test_models.py
- [ ] T026 [P] Unit tests for services in tests/unit/test_services.py
- [ ] T027 [P] Update README.md and docs with API usage
- [ ] T028 Performance tests for API calls
- [ ] T029 Add docstrings to all functions

## Dependencies
- Tests (T005-T011) before implementation (T012-T021)
- T012-T014 block T015-T021
- T015 blocks T019-T021
- T016-T017 block T018
- Implementation before polish (T025-T029)

## Parallel Example
```
# Launch T005-T007 together:
Task: "Contract test GET /reports in tests/contract/test_reports.py"
Task: "Contract test GET /schools in tests/contract/test_schools.py"
Task: "Contract test GET /students in tests/contract/test_students.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task