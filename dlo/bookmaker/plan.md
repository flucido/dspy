Build Specification: Ox-Turn Learning Engine (EPA)
Overview
This is a greenfield project—the workspace is empty except for Codacy CI tooling. This specification transforms the conceptual architecture into a formal, phased build specification that will drive spec-driven development for a modular educational platform combining Boustrophedon reading with AI-generated study materials.

Phase 0: Project Bootstrap
Objective
Establish the foundational project structure, tooling, and development environment.

Deliverables
 Python project configuration (pyproject.toml)
 DuckDB integration setup
 FastAPI skeleton application
 Nix development environment (flake.nix)
 Directory structure for monorepo
Directory Structure
/
├── backend/           # FastAPI application
│   ├── api/           # API routes
│   ├── core/          # Config, database, dependencies
│   ├── models/        # Pydantic models & DB schemas
│   └── services/      # Business logic
├── worker/            # AI Worker (LLM cluster interface)
│   ├── tasks/         # Async task definitions
│   └── prompts/       # LLM prompt templates
├── frontend/          # React/Svelte web UI
├── tui/               # Textual TUI client (optional)
├── docs/              # Specifications & documentation
├── tests/             # Test suites
├── flake.nix          # Nix development environment
└── pyproject.toml     # Python project config
Acceptance Criteria
 nix develop drops into a shell with Python 3.11+, DuckDB, and dev tools
 uvicorn backend.main:app --reload starts the API server
 Health check endpoint /health returns {"status": "ok"}
 DuckDB connection initializes without error
Phase 1: Ingestion Pipeline
Objective
Accept raw documents (PDF, text, markdown) and store them for processing.