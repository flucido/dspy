# Dr. Ogren Apps - Development Commands
# Usage: make <command>

.PHONY: help dev web api test lint clean install

# Default target
help:
	@echo "Dr. Ogren Apps - Available Commands:"
	@echo ""
	@echo "  Development:"
	@echo "    dev       Start both frontend and backend (requires tmux or separate terminals)"
	@echo "    web       Start the Next.js frontend only"
	@echo "    api       Start the FastAPI backend only"
	@echo ""
	@echo "  Installation:"
	@echo "    install   Install dependencies for all projects"
	@echo ""
	@echo "  Testing & Linting:"
	@echo "    test      Run all tests"
	@echo "    lint      Run all linters"
	@echo ""
	@echo "  Cleanup:"
	@echo "    clean     Remove build artifacts and caches"

# ── Development ──────────────────────────────────────────────────────────────

web:
	@echo "Starting Next.js frontend..."
	cd dlo && npm run dev

api:
	@echo "Starting FastAPI backend..."
	cd bookmaker && ./run_api.sh --reload

dev:
	@echo "Starting both services..."
	@echo "  - Backend:  http://localhost:8000"
	@echo "  - Frontend: http://localhost:3000"
	@echo ""
	@echo "Opening in separate terminals (macOS)..."
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/bookmaker && ./run_api.sh --reload"'
	@osascript -e 'tell app "Terminal" to do script "cd $(PWD)/dlo && npm run dev"'

# ── Installation ─────────────────────────────────────────────────────────────

install:
	@echo "Installing frontend dependencies..."
	cd dlo && npm install
	@echo "Installing backend dependencies..."
	cd bookmaker && uv sync
	@echo "Done!"

# ── Testing & Linting ────────────────────────────────────────────────────────

test:
	@echo "Running frontend tests..."
	cd dlo && npm run test
	@echo "Running backend tests..."
	cd bookmaker && uv run pytest

lint:
	@echo "Linting frontend..."
	cd dlo && npm run lint
	@echo "Linting backend..."
	cd bookmaker && uv run ruff check oxturn api

# ── Cleanup ──────────────────────────────────────────────────────────────────

clean:
	@echo "Cleaning frontend..."
	rm -rf dlo/.next dlo/node_modules dlo/.cache
	@echo "Cleaning backend..."
	rm -rf bookmaker/.venv bookmaker/__pycache__ bookmaker/.pytest_cache bookmaker/.mypy_cache bookmaker/.ruff_cache bookmaker/.coverage
	@echo "Done!"
