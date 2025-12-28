# My Code Brain

This is the central "Federated Brain" repository. It serves as the persistent, single source of truth for all aggregated knowledge.

## Structure

- `knowledge/codebase/`: XML packs of code repositories (mined by `repomix`).
- `knowledge/life-ops/`: Daily briefings and life data summaries (mined by `warp-google-workspace-automation`).
- `knowledge/chats/`: Archived chat logs (mined from Gemini exports).

## Usage

This repository is primarily consumed by **The Brain TUI**, a terminal interface for browsing knowledge and managing operations.

### Running the TUI

```bash
uv run python -m tui.app
```

### Debugging

To debug the TUI with live logs:

1. **Open Terminal 1** (Console):

    ```bash
    uv run textual console
    ```

2. **Open Terminal 2** (App):

    ```bash
    ./scripts/debug.sh
    # OR
    uv run textual run --dev tui.app
    ```

You will see logs and print statements in Terminal 1.

### Features

- **Dashboard**: View daily briefings from Life Miners.
- **Knowledge Base**: Browse and search archived chat logs and codebases.
- **Operations**: Create new operational documents and plans using standardized templates.

## Automation

Data is pushed here automatically by various "miners":

- **Code Miner**: GitHub Actions in source repos.
- **Life Miner**: Local scripts/cron jobs.
