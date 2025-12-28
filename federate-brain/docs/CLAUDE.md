# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Federated Brain is a centralized knowledge aggregation and operations management system consisting of:

1. **Brain TUI**: Python terminal interface (Textual framework) for browsing knowledge and managing operations
2. **Miners**: Automated scripts that extract data from external sources (codebases via repomix, daily briefings, chat logs)
3. **Operations Framework**: Document lifecycle management (specification → planning → drafting)

## Commands

```bash
# Install dependencies
uv sync

# Run the TUI
uv run python -m tui.app

# Run tests
uv run pytest
```

## Architecture

### Data Flow
```
External Sources → Miners → knowledge/ directory → Brain TUI
```

### TUI Structure
- `tui/app.py` - Main entry point with 4 tabs (Dashboard, Knowledge Base, Operations, Tools)
- `tui/screens/` - Screen implementations (dashboard.py, knowledge.py, operations.py, tools.py, tool_runner.py)
- `tui/widgets/` - Reusable components (activity.py, briefing.py, todo.py, clock.py)
- `tui/brain.tcss` - Textual CSS stylesheet
- `tui/common.py` - Shared utilities including `REPO_ROOT` constant

### Operations Module
- `operations/document.py` - Creates new documents (generates spec branch + copies template)
- `operations/plan.py` - Sets up document plans from templates
- `operations/common.py` - Git paths and branch utilities

### Document Workflow
Documents follow a git-as-database pattern:
1. User creates document → generates branch `###-description`
2. Creates `specs/###-description/` directory with `spec.md` from template
3. Plan setup copies template to `plan.md`
4. User edits on feature branch, merges to master when complete

### Miners (GitHub Actions)
- `miners/code-miner/` - Codebase mining via repomix + Gemini summarization
- `miners/life-ops/` - Life/work operations briefings
- `miners/chat-watcher/` - Chat log archival

Data populates `knowledge/` directory: `codebase/`, `life-ops/`, `chats/`

## Key Patterns

### Textual UI Pattern
```python
from textual.app import ComposeResult
from textual.widgets import Static, Button

class MyScreen(Static):
    def compose(self) -> ComposeResult:
        yield Button("Click", id="btn-action")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.notify("Clicked!")
```

### File Operations
Always use `REPO_ROOT` from `tui.common` for paths relative to project root:
```python
from tui.common import REPO_ROOT
knowledge_dir = REPO_ROOT / "knowledge" / "codebase"
```

### Git Operations
Uses subprocess with list args (safe from injection):
```python
subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
```

### External Tools
Uses `app.suspend()` for running external CLI tools (LazyGit, NeoVim, etc.)

## Environment Variables

Create `.env` in root (gitignored):
```
GEMINI_API_KEY=your_key_here
```

Used by `miners/code-miner/summarize.py` for generating code digests via Gemini 2.0 Flash.

## Branch Naming Convention

Document branches follow: `###-document-description` (e.g., `001-test`, `002-new-feature`)
