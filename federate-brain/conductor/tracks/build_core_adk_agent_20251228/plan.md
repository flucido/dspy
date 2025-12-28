# Plan: Build the core ADK agent with Google Workspace Calendar and Task management integration, and a basic Next.js frontend chat interface, leveraging Ollama for local LLM inference.

This plan outlines the steps to build the core ADK agent, integrate it with Google Workspace for Calendar and Task management, and develop a basic Next.js frontend with a chat interface, utilizing Ollama for local LLM inference.

## Phase 1: Agent Core and Local LLM Setup [checkpoint: 047b496]

- [x] Task: Set up Docker development environment and project structure (6f6911c)
    - [ ] Subtask: Create `legacy/` directory and draft `legacy/README.md`
    - [ ] Subtask: Create Docker skeleton for `agent/`, `frontend/`, `secrets/`, `docker-compose.yml`, and `.env.example`
- [x] Task: Research ADK/CopilotKit and Ollama integration (f673f32)
    - [ ] Subtask: Clarify "ADK SDK" terminology and review CopilotKit documentation
    - [ ] Subtask: Test CopilotKit + Ollama compatibility
    - [ ] Subtask: Prototype simple agent with function calling
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Agent Core and Local LLM Setup' (Protocol in workflow.md)

## Phase 2: Google Workspace Integration (Calendar & Tasks) [checkpoint: 3b7e694]

- [x] Task: Implement Google Workspace Function Calling Layer (37b7131)
    - [ ] Subtask: Write Failing Tests for Calendar API functions (list, create, detect conflicts)
    - [ ] Subtask: Implement Calendar API function handlers
    - [ ] Subtask: Write Failing Tests for Tasks API functions (list, create, complete)
    - [ ] Subtask: Implement Tasks API function handlers
- [x] Task: Integrate Google Workspace tools into Agent Configuration (6ff9843)
    - [ ] Subtask: Write Failing Tests for agent tool integration with Google Calendar
    - [ ] Subtask: Implement agent configuration with Google Calendar tools
    - [ ] Subtask: Write Failing Tests for agent tool integration with Google Tasks
    - [ ] Subtask: Implement agent configuration with Google Tasks tools
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Google Workspace Integration (Calendar & Tasks)' (Protocol in workflow.md)

## Phase 3: Agent Memory and Knowledge Base

- [~] Task: Mount `my-code-brain/knowledge` as a read-only volume
    - [x] Subtask: Write Failing Tests for reading codebase XML and Markdown digests (a602c12)
    - [ ] Subtask: Implement memory manager to read codebase context
    - [ ] Subtask: Write Failing Tests for reading life-ops daily briefings
    - [ ] Subtask: Implement memory manager to read life-ops context
    - [ ] Subtask: Write Failing Tests for reading chat history
    - [ ] Subtask: Implement memory manager to read chat context
- [ ] Task: Implement Agent State Persistence
    - [ ] Subtask: Write Failing Tests for agent state storage and retrieval
    - [ ] Subtask: Implement state manager to use Docker volume for persistence
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Agent Memory and Knowledge Base' (Protocol in workflow.md)

## Phase 4: Next.js Frontend Development

- [ ] Task: Build basic Next.js application structure
    - [ ] Subtask: Write Failing Tests for Next.js app initialization
    - [ ] Subtask: Implement Next.js project setup with CopilotKit integration
- [ ] Task: Implement Agent Chat Interface
    - [ ] Subtask: Write Failing Tests for CopilotKit chat component
    - [ ] Subtask: Implement AgentChat.tsx component
- [ ] Task: Implement Read-Only Calendar View
    - [ ] Subtask: Write Failing Tests for CalendarView.tsx component
    - [ ] Subtask: Implement CalendarView.tsx to display multi-calendar overlay
- [ ] Task: Implement Read-Only Task List
    - [ ] Subtask: Write Failing Tests for TaskList.tsx component
    - [ ] Subtask: Implement TaskList.tsx to display Google Tasks
- [ ] Task: Implement Daily Briefing Panel
    - [ ] Subtask: Write Failing Tests for DailyBriefing.tsx component
    - [ ] Subtask: Implement DailyBriefing.tsx to display latest life-ops summaries
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Next.js Frontend Development' (Protocol in workflow.md)

## Phase 5: End-to-End Testing and Verification

- [ ] Task: Test end-to-end functionality
    - [ ] Subtask: Write end-to-end tests for calendar conflict detection
    - [ ] Subtask: Run end-to-end tests for calendar conflict detection
    - [ ] Subtask: Write end-to-end tests for task creation and completion
    - [ ] Subtask: Run end-to-end tests for task creation and completion
    - [ ] Subtask: Write end-to-end tests for knowledge base querying
    - [ ] Subtask: Run end-to-end tests for knowledge base querying
- [ ] Task: Verify deployment workflow
    - [ ] Subtask: Test `docker-compose up` functionality for all services
    - [ ] Subtask: Verify frontend and agent API health checks
- [ ] Task: Conductor - User Manual Verification 'Phase 5: End-to-End Testing and Verification' (Protocol in workflow.md)
