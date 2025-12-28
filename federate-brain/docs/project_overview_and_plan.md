# Project Overview: Federated Brain System

## 1. Executive Summary
This project aims to create a "Write-Once, Read-Forever" knowledge system named the "Federated Brain." It will automatically aggregate three distinct data streams—code repositories, personal life data (email, calendar, tasks), and AI chat histories—into a central, private GitHub repository called `my-code-brain`. This repository will function as a persistent, single source of truth, designed to be consumed by various AI tools like NotebookLM, Cursor, and Copilot, providing a continuous and aggregate understanding of all personal and professional activities. The system is built on a "Push-to-Central" architecture, where independent "miner" agents (GitHub Actions, Google Apps Script) synthesize data at the edge and push standardized Markdown or XML to the central repository.

## 2. Core Problem & Proposed Solution
The core problem is that valuable knowledge and context are siloed across numerous platforms (code hosts, email, chat apps) and are often ephemeral or difficult to query programmatically. This makes it challenging to get a holistic view of past work, connect ideas between projects, or provide comprehensive context to AI development assistants.

The proposed solution is to build an automated ETL (Extract, Transform, Load) pipeline that:
1.  **Extracts** data from sources like GitHub repositories, Google Workspace (Gmail, Calendar, Tasks), and Gemini chat exports.
2.  **Transforms** this raw data into structured, AI-friendly formats (Markdown summaries, XML code packs). An "intelligence layer" using a fast LLM (like Gemini Flash) is used to synthesize and summarize the data, turning noise into signal.
3.  **Loads** the processed files into a central GitHub repository, creating a unified, queryable, and persistent knowledge base.

## 3. Key Features & Requirements
-   **Automated Code Mining**:
    -   A GitHub Action will run on every push to `main` in designated repositories.
    -   It will use `repomix` to pack the codebase into a single, filtered XML file, excluding noise like `node_modules` and lockfiles.
    -   The packed XML will be pushed to the `my-code-brain` repo under a `knowledge/codebase/` directory.
-   **Automated Life-Ops Mining**:
    -   A Google Apps Script ("Auto-Journalist") will run on a daily schedule.
    -   It will fetch data from Gmail, Google Calendar, and Google Tasks.
    -   It will use the Gemini API to generate a "Daily Briefing" Markdown summary.
    -   The briefing will be pushed to the `my-code-brain` repo under a `knowledge/life-ops/` directory.
-   **Automated Chat Mining**:
    -   A Google Apps Script ("Export Watcher") will monitor a Google Drive folder for new "Export to Docs" files from Gemini.
    -   Upon detection, it will convert the Google Doc to Markdown.
    -   The Markdown chat log will be pushed to the `my-code-brain` repo under a `knowledge/chats/` directory.
-   **Terminal User Interface (TUI)**:
    -   A TUI built with Python and the Textual framework will serve as the primary interface for interacting with the "Brain."
    -   The TUI will feature a multi-screen layout: a "Dashboard" for the latest daily briefing, a "Knowledge Browser" to explore the raw files in the repo, and the modular capability to "inject" future projects or views as new screens.
-   **Central Knowledge Repository**:
    -   A private GitHub repository named `my-code-brain` will store all synthesized knowledge.
    -   The data will be organized into logical folders (`codebase`, `life-ops`, `chats`).
    -   This repository will be the primary source for AI tools like NotebookLM and Cursor.

## 4. Initial Project Plan & Milestones
-   **Phase 1: Core Infrastructure Setup (Week 1)**
    -   Milestone: `my-code-brain` private GitHub repository created and Personal Access Token (PAT) generated.
-   **Phase 2: Code Miner Implementation (Week 1-2)**
    -   Milestone: The `update-brain.yml` GitHub Action is successfully deployed to a pilot code repository and automatically pushes a `context.xml` file to the central brain.
-   **Phase 3: Life & Chat Miner Implementation (Week 2-3)**
    -   Milestone: The Google Apps Scripts for the "Auto-Journalist" and "Export Watcher" are deployed and successfully push their respective Markdown files to the central brain on schedule.
-   **Phase 4: TUI Development & Integration (Week 3-4)**
    -   Milestone: A functional Textual TUI is built that can read from the local clone of `my-code-brain` and display the daily briefing and file structure.
-   **Phase 5: Consumption Layer & Refinement (Ongoing)**
    -   Milestone: NotebookLM and Cursor are successfully configured to use `my-code-brain` as a primary knowledge source, and queries demonstrate cross-domain understanding.

## 5. Potential Risks & Open Questions
-   **Risk**: APIs for third-party services (like Gemini chat history) are not officially public and rely on workarounds like "Export to Docs." A UI change could break the chat mining workflow.
-   **Risk**: The cost of LLM API calls for summarization, while currently low, could increase if the volume of data grows significantly or more complex models are used.
-   **Risk**: Security of the GitHub PAT and Gemini API Key stored in Google Apps Script properties is critical. A compromise could expose the entire knowledge base.
-   **Question**: Is there a more direct way to access Gemini chat history than Google Takeout for backfilling past data? The current method is a manual, one-time process.
-   **Question**: How will schema changes or new data sources be managed in the future? The system needs a clear process for expansion.

## 6. Stakeholders & Team Roles
-   **Project Lead/User**: The primary individual whose data is being mined and who will consume the knowledge base.
-   **AI Assistant (Gemini)**: Acts as the intelligence layer for summarizing and synthesizing data.

## 7. Source Document Summary
-   **I want to create a terminal user interface either ....md**: Discussed the choice between GPUI (GUI) and Textual (TUI), strongly recommending Textual for its Python integration and CSS-based layout, and provided a proof-of-concept `brain_dashboard.py` script.
-   **Into a detailed brief keep the code going and prov....md**: Provided a formal technical brief for the entire "Federated Brain" architecture, including implementation details for the "Code Miner" (GitHub Actions) and "Life Miner" (Google Apps Script), and a deployment checklist.
-   **okay keeping the theme of mining these areas and I....md**: Detailed the "Auto-Journalist" Google Apps Script for mining Gmail, Calendar, and Tasks, using Gemini for summarization, and discussed different ways to consume the output (Dashboard, Email, Tasks).
-   **my question was can you access a GitHub knowledge ....md**: Clarified that there is no public API to programmatically access Gemini chat history, proposing the "Export Watcher" (Google Apps Script) as a workaround and suggesting Google Takeout for backfilling historical data.
-   **could you access that via API so can you programma....md**: Explained that GitHub Copilot Knowledge Bases cannot be updated via API, reinforcing the superiority of the "Federated Brain" (central repo) approach which uses standard `git` as its API.
-   **With Google code wiki service being introduced is ....md**: Addressed the limitations of closed systems like Google Code Wiki and NotebookLM, proposing a self-owned "Continuous Code Brain" powered by GitHub Actions and `repomix` to create a portable and automatable knowledge base.
-   **Is there any reason to due date analysis in notebo....md**: Differentiated between quantitative (bad fit) and qualitative (good fit) data analysis in NotebookLM, confirming its suitability for analyzing the text-based outputs of this system.
-   **Keep going.md**: Provided the "Phase 2" implementation of the Textual TUI, demonstrating a modular, multi-screen architecture and the `BrainLoader` class for reading data from the repository.