# Technology Stack: Federated Brain System

## Overview

The Federated Brain system leverages a modern and flexible technology stack designed to support its transformation into an agent-driven home operating system. The architecture is built around containerization for ease of deployment and scaling, with a strong emphasis on integrating AI capabilities and Google Workspace services.

## Core Technologies

### Programming Languages

- **TypeScript/JavaScript:** Primarily used for the agent's core logic, the Next.js frontend, and the CopilotKit integration. This provides a robust and type-safe environment for building interactive web applications and agent functionalities.
- **Python:** Utilized for existing data miners that aggregate information into the knowledge base. This preserves existing investments and allows for flexible data processing.

### Frameworks

- **Next.js:** The chosen framework for the web-based frontend, providing server-side rendering, routing, and a component-based architecture for a rich user experience.
- **CopilotKit:** Selected as the primary framework for building the agent's core, offering robust tools for LLM integration, function calling, and managing conversational flows.

### Databases/Memory & Knowledge Management

- **Git-based File System:** The primary storage mechanism for the project's knowledge base (`my-code-brain/knowledge`). This is mounted as a read-only volume in the agent container, ensuring version control and external accessibility.
- **Docker Volumes:** Used for persistent storage of the agent's operational state, including conversation history and decision logs.
- **Vector Database (Future):** Planned for Phase 2 optimization to enable faster semantic search capabilities across the knowledge base.

### Local LLM Inference

- **Ollama:** The chosen local LLM inference engine, running **Gemma 3B**. Ollama provides native Docker support and a CLI-first design, making it ideal for automation and deployment on a home server.

### Deployment

- **Docker:** All services (agent, frontend, Ollama, Home Assistant - Phase 2) are containerized and orchestrated using Docker Compose. This simplifies local development and ensures consistent deployment across various target environments (development machine, bare-metal Linux server, NAS).

## Authentication & Secrets Management

- **Google Cloud CLI (gcloud):** Used for authenticating with Google Workspace APIs.
- **GitHub Personal Access Token:** Secured through a `secrets/github-token` file and accessed via environment variables.
- **Environment Variables (`.env` file):** For managing various API keys and configuration parameters.
