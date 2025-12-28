**Agent Context: Federated Brain System**

This document serves as the high-level context, requirements, and architectural brief for developing the "Federated Brain" system, evolving it from a passive knowledge base into an active, agent-driven operating system.-----1. Project Goal

The primary goal is to integrate an existing "Miner" system (for data harvesting and persistence) with a new **ADK/CopilotKit-based Agentic architecture** to create an active home operating system capable of automation, planning, and sophisticated data visualization.2. Core Architecture & Stack

| Component | Description / Technology | Key Decisions |
| ----- | ----- | ----- |
| **Hosting** | Containerized Home Server | Docker is the preferred containerization solution. |
| **Base OS** | Thin Linux Distribution | Running on a small OS like Arch or Alpine. |
| **Agent Core** | Orchestration Layer | Built using the **ADK SDK**. |
| **LLMs (Local)** | Local Model Inference Engine | **Ollama** or **LM Studio** to run very small, efficient, sub-10 billion parameter models (e.g., Gemma). |
| **Home Server** | Base Automation Platform | Likely **Home Assistant** (inside the container). |
| **Frontend UI** | Web Interface | A **Next.js app** hosted in its own container, running alongside the agent. |
| **Persistence** | Long-Term Memory | Existing **`my-code-brain`** GitHub repository. |

3\. Functional Requirements

The agent must be able to manage the following functions:

* **Small Automations:** Manage basic home automations (e.g., turning lights on/off).  
* **Calendar & To-Do Planning:** Plan events and to-do items.  
* **Integrated Calendar Display:** Provide a single web display of a consolidated calendar, integrating events from various calendars (e.g., for the user and spouse).  
* **Advanced Calendar Views:** Offer different views, including **Gantt charts**, and perform conflict-checking on appointments.  
* **Interface:** Accept inputs via a main agent web interface (ADK web interface), command line, and various protocols (XML, JSON file formats).

4\. Integration & ToolingGoogle Workspace Tooling (Function Calling)

The system will use **Function Calling** to interact with the Google Office Suite APIs (as an alternative to RAG for tool execution).

* **APIs to Access:**  
  * Google Calendar API  
  * Google Tasks/To-Do API  
  * Google Docs API  
  * Google Sheets API  
  * Google Slides (potential)

Existing Miner Architecture Integration

The existing "Miner" system will be integrated as follows, serving as the Agent's context and long-term memory:

| Existing Project Phase | Role in the New Architecture | Key Benefit |
| ----- | ----- | ----- |
| **Code Miner (Repomix)** | **Code Context Layer** | Agent can "read" the codebase's state from `context.xml` to answer technical questions. |
| **Life Miner (Apps Script)** | **Proactive Tooling** | Agent can **act** on daily briefings (e.g., proactively suggest moving a conflicting meeting). |
| **Federated Brain Repo** | **Long-term Memory/Knowledge Base** | Provides deep context for the ADK Agent, augmenting Gemini's own memory. |

Authentication

Authentication must be unified. **Google CLI (`gcloud`)** should be used within the Docker environment to centralize the `GITHUB_TOKEN` and `GEMINI_API_KEY` for both the existing miners and the new ADK Agent.5. Design and Development Principles

* **Design First:** Prioritize a **Senior Design Review Phase** to avoid rebuilding the system multiple times.  
* **Documentation:** All conversations and design decisions must be documented in detailed **Markdown (`.md`)** files.  
* **Diagrams:** Use **Mermaid JS** for generating architectural and flow diagrams.

6\. Next Immediate Action

The next step is to draft a **`docker-compose.yml`** file that mounts the local clone of the existing `my-code-brain` repository into the new ADK Agent container to allow the Agent to immediately access and "learn" from the mined knowledge.  
