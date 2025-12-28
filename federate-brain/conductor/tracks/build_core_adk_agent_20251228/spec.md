# Spec: Core ADK Agent with Google Workspace Integration

## Overview
This specification outlines the development of the core ADK (Agent Development Kit) agent for the Federated Brain system. The agent will integrate with Google Workspace APIs for Calendar and Task management, and provide a basic Next.js frontend chat interface. Local LLM inference will be powered by Ollama.

## Features

### 1. ADK Agent Core
-   **Agent Framework:** Implement the agent using CopilotKit (React-Integrated) for its proven track record with Next.js, built-in chat UI components, strong TypeScript support, and active community.
-   **Local LLM Integration:** Configure the agent to use Ollama running Gemma 3B for local LLM inference. This leverages Ollama's native Docker support and CLI-first design.
-   **Fallback LLM:** Configure a fallback to `google/gemini-flash` for cloud inference if local inference is insufficient.

### 2. Google Workspace Integration
-   **Function Calling Layer:** Implement Google Workspace function calling for Calendar and Tasks APIs. This will enable the agent to interact with Google services programmatically.
-   **Calendar Management:**
    -   List events from multiple calendars (user, spouse, work).
    -   Detect scheduling conflicts.
    -   Suggest alternative event times.
-   **Task Management:**
    -   List tasks from Google Tasks.
    -   Create new tasks.
    -   Mark tasks as complete.

### 3. Agent Memory & Context
-   **Knowledge Base Integration:** Mount the existing `my-code-brain/knowledge` directory as a read-only volume. The agent should be able to read:
    -   Latest daily briefings from `life-ops/` (personal, work, ltc).
    -   Context from `codebase/` (XML and Markdown digests).
    -   Chat history from `chats/`.
-   **Agent State Persistence:** Store the agent's operational state (conversation history, decisions) in a separate Docker volume (`/agent-state`).

### 4. Next.js Frontend
-   **Chat Interface:** Implement a basic chat interface using CopilotKit components, allowing natural language interaction with the agent.
-   **Read-Only Views:** Display read-only views for:
    -   Multi-calendar overlay.
    -   Task list.
    -   Daily briefing panel.

## Architecture

### System Overview
-   **Home Server (Docker Host):** Orchestrates containers for the ADK Agent, Frontend, and Ollama.
-   **ADK Agent Container:** Contains the CopilotKit Agent, Ollama/LM Studio (Gemma 3B), Agent State Manager, and Google Workspace Function Calling Layer.
-   **Frontend Container:** Hosts the Next.js Web UI with Agent Chat Interface, Calendar/Task Dashboard, and Gantt Chart View.
-   **Shared Volumes:** Read-only mount of `my-code-brain/knowledge`, read-write for `/agent-state`, and `/logs/`.
-   **External Services:** Google Workspace APIs, GitHub API, Gemini API (fallback/enhancement).

### Deployment Strategy
-   **Local Development:** Utilize Docker Compose for local setup on macOS/Linux.
-   **Authentication:** Unified strategy using Google Cloud CLI for Google APIs and GitHub Personal Access Token for GitHub API. Environment variables for other secrets.

## Future Considerations (Beyond this track)
-   Proactive features (conflict alerts, auto-suggestions).
-   Advanced visualizations (Gantt charts).
-   Home Assistant integration for physical automation.
-   Vector database for semantic search optimization.
