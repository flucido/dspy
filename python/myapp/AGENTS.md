# AGENTS.md - Development Guidelines for myapp

## Build/Lint/Test Commands

### Build
- `python -m build` - Build distribution packages
- `pip install -e .` - Install in development mode

### Test
- `python -m pytest` - Run all tests
- `python -m pytest tests/test_file.py::TestClass::test_method` - Run single test
- `python -m pytest -v` - Run tests with verbose output

### Lint & Format
- `ruff check .` - Lint code with ruff
- `ruff format .` - Format code with ruff
- `black .` - Format code with black
- `isort .` - Sort imports

## Code Style Guidelines

### Imports
- Use absolute imports: `from myapp.module import function`
- Group imports: standard library, third-party, local
- Use `isort` for consistent import ordering

### Formatting
- Use `black` or `ruff format` for consistent formatting
- Line length: 88 characters (black default)
- Use double quotes for strings

### Types
- Use type hints for function parameters and return values
- `from typing import List, Dict, Optional, Union`
- Enable mypy checking: `mypy .`

### Naming Conventions
- Functions: `snake_case` (e.g., `get_user_data`)
- Classes: `PascalCase` (e.g., `UserManager`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- Variables: `snake_case` (e.g., `user_count`)

### Error Handling
- Use specific exceptions over generic `Exception`
- Use context managers for resource management
- Log errors appropriately with logging module

### General Best Practices
- Write docstrings for public functions and classes
- Keep functions small and focused on single responsibility
- Use descriptive variable names
- Add type hints for better IDE support