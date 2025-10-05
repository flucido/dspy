# Olamah Setup (macOS, Apple Silicon)

This README documents a clean, service-based install of Ollama on macOS with Apple Silicon, plus convenience settings you asked for.

## Summary
- Install method: Homebrew
- Ollama version: 0.11.10
- Service: runs at login via `brew services`
- Default host: `127.0.0.1:11434` (configurable)
- Thinking output: hidden by default via `olrun` alias
- Models installed: `qwen3:latest` (only)
- Shortcuts: alias `OL` (for `ollama`), function `olrun` (runs `ollama run` with `--hidethinking` by default)

## Install steps performed
1. Install Ollama via Homebrew:
   ```bash
   brew install ollama
   ```
2. Start as a user service so it runs at login:
   ```bash
   brew services start ollama
   ```
3. Verify daemon and API:
   ```bash
   ollama --version
   curl -s localhost:11434/api/tags
   ```
4. Pull the requested model only:
   ```bash
   ollama pull qwen3:latest
   ```
5. Sanity-test run:
   ```bash
   ollama run qwen3:latest "Say hello from Qwen3."
   ```

## Host configuration
- Default (local):
  - OLLAMA_HOST is set in your shell config to `127.0.0.1:11434`.
  - Current configured host in ~/.zshrc: 127.0.0.1:11434
  - You can change it to a remote host/port if you deploy Ollama elsewhere.
- To check the current host in your shell:
  ```bash
  echo "$OLLAMA_HOST"
  ```
- To use a different host for a single command:
  ```bash
  OLLAMA_HOST=127.0.0.1:11434 ollama list
  ```

## Hiding thinking output
- Use the `olrun` function to hide thinking output by default:
  ```bash
  olrun MODEL "Your prompt"
  ```
  Behavior:
  - If you already provided `--hidethinking`, it will not be duplicated.
  - Otherwise, `--hidethinking` is added for you.
  Under the hood it effectively runs:
  ```bash
  ollama run --hidethinking MODEL "Your prompt"
  ```
- If a model doesn’t support thinking output, the flag is harmless.

## Shortcuts added
- Alias: `OL` → `ollama`
- Function: `olrun` → runs `ollama run` and adds `--hidethinking` unless you already supplied it

These are appended to `~/.zshrc` inside a clearly marked block so they are easy to find and edit.

To load them now in your current terminal session:
```bash
source ~/.zshrc
```

## Service management
- Start: `brew services start ollama`
- Stop: `brew services stop ollama`
- Restart: `brew services restart ollama`
- Status: `brew services list | grep ollama`

## Models and storage
- Current models: `qwen3:latest`.
- Default storage location is `~/.ollama`.
- If you later want a custom models directory (e.g., external disk), you can set `OLLAMA_MODELS` before starting the service:
  ```bash
  export OLLAMA_MODELS="/Volumes/External/ollama-models"
  brew services restart ollama
  ```

## Useful commands
- List models: `OL list`
- Pull a model: `OL pull <name>:<tag>`
- Remove a model: `OL rm <name>:<tag>`
- Run a prompt with hidden thinking: `olrun <name>:<tag> "Your prompt"`

## Troubleshooting
- Ensure the service is running:
  ```bash
  brew services list | grep ollama
  ```
- Check the API:
  ```bash
  curl -s localhost:11434/api/tags
  ```
- Logs (service): try restarting, or run the daemon in the foreground for debugging:
  ```bash
  brew services stop ollama
  /opt/homebrew/opt/ollama/bin/ollama serve
  ```

## Uninstall (optional)
If you ever want to remove Ollama (keeping models):
```bash
brew services stop ollama
brew uninstall ollama
```
To also remove local models/cache:
```bash
rm -rf ~/.ollama
```

---
Created by Agent Mode on 2025-09-13.
