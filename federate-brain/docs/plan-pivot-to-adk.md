# Plan: Pivot to ADK Agent-Driven Architecture

**Version:** 1.0  
**Date:** December 28, 2025  
**Status:** Planning Phase

---

## Executive Summary

This document outlines the comprehensive plan to pivot the Federated Brain system from a passive Terminal User Interface (TUI) knowledge browser to an active, agent-driven home operating system. The pivot leverages the existing 60% complete implementation (miners, TUI, operations) as the foundation for an ADK/CopilotKit-based agentic system that provides automation, planning, and intelligent assistance.

**Key Transformation:**
- **From:** TUI-centric knowledge aggregation and browsing
- **To:** Agent-first automation platform with web UI, where the agent proactively acts on calendar conflicts, task management, and home automation using Google Workspace APIs

---

## Table of Contents

1. [Architecture Design](#1-architecture-design)
2. [Deployment Strategy](#2-deployment-strategy)
3. [Critical Design Decisions](#3-critical-design-decisions)
4. [Implementation Phases](#4-implementation-phases)
5. [Open Questions & Research Needed](#5-open-questions--research-needed)
6. [Risk Analysis](#6-risk-analysis)
7. [Success Metrics](#7-success-metrics)

---

## 1. Architecture Design

### 1.1 System Overview

```mermaid
graph TB
    subgraph "Home Server (Docker Host)"
        subgraph "ADK Agent Container"
            ADK[ADK Core/CopilotKit Agent]
            LocalLLM[Ollama/LM Studio<br/>Gemma 3B]
            Memory[Agent State Manager]
            FnCalling[Google Workspace<br/>Function Calling Layer]
        end
        
        subgraph "Frontend Container"
            NextJS[Next.js Web UI]
            AgentInterface[Agent Chat Interface]
            Dashboard[Calendar/Task Dashboard]
            Gantt[Gantt Chart View]
        end
        
        subgraph "Home Automation Container (Optional Phase 2)"
            HA[Home Assistant]
        end
        
        subgraph "Shared Volumes"
            Knowledge[/my-code-brain/knowledge/<br/>Read-Only Mount]
            State[/agent-state/<br/>Read-Write]
            Logs[/logs/]
        end
    end
    
    subgraph "External Services"
        Google[Google Workspace APIs<br/>Calendar, Tasks, Docs, Sheets]
        GitHub[GitHub API<br/>my-code-brain repo]
        Gemini[Gemini API<br/>(Fallback/Enhancement)]
    end
    
    subgraph "Data Miners (Existing)"
        CodeMiner[Code Miner<br/>GitHub Actions]
        LifeMiner[Life-Ops Miner<br/>Apps Script]
        ChatWatcher[Chat Watcher<br/>Apps Script]
    end
    
    CodeMiner -->|XML| Knowledge
    LifeMiner -->|Markdown| Knowledge
    ChatWatcher -->|Markdown| Knowledge
    
    Knowledge -.->|Context| ADK
    ADK <-->|API Calls| Google
    ADK -->|Commit| GitHub
    ADK <-->|LLM Requests| LocalLLM
    ADK <-->|State| State
    ADK <-->|Optional| Gemini
    
    NextJS <-->|WebSocket/HTTP| ADK
    AgentInterface -.->|Part of| NextJS
    Dashboard -.->|Part of| NextJS
    Gantt -.->|Part of| NextJS
    
    ADK -.->|Phase 2| HA
    
    style ADK fill:#4a90e2,stroke:#333,stroke-width:3px
    style Knowledge fill:#90ee90,stroke:#333,stroke-width:2px
    style NextJS fill:#ff6b6b,stroke:#333,stroke-width:2px
```

### 1.2 ADK Agent Core Architecture

#### 1.2.1 Agent Configuration Structure

The ADK agent will be configured with the following components:

**Option A: CopilotKit (React-Integrated)**
```typescript
// copilotkit-agent-config.ts
import { CopilotRuntime, OpenAIAdapter } from "@copilotkit/runtime";
import { GoogleWorkspaceTools } from "./tools/google-workspace";
import { BrainMemory } from "./memory/brain-memory";

export const agentConfig = {
  // LLM Configuration
  model: {
    primary: "ollama/gemma:3b",      // Local inference
    fallback: "google/gemini-flash", // Cloud fallback
    temperature: 0.7,
  },
  
  // Tool Configuration
  tools: [
    GoogleWorkspaceTools.calendar,   // Calendar management
    GoogleWorkspaceTools.tasks,      // Task CRUD
    GoogleWorkspaceTools.docs,       // Document creation
    GoogleWorkspaceTools.sheets,     // Data tracking
  ],
  
  // Memory/Context Configuration
  memory: {
    type: "federated-brain",
    path: "/mnt/knowledge",          // Mount point
    readers: [
      "codebase-xml",                // XML parser for code
      "markdown-parser",             // MD for life-ops/chats
    ],
    maxContextTokens: 8000,          // For small models
  },
  
  // Agent Personality & Instructions
  systemPrompt: `You are a proactive home operating system assistant...`,
  
  // Capabilities
  capabilities: {
    proactiveAlerts: true,           // Conflict detection
    autoSuggestions: true,           // Meeting rescheduling
    multiCalendar: true,             // User + spouse calendars
    ganttView: true,                 // Advanced visualization
  },
};
```

**Option B: Pure ADK SDK (Framework-Agnostic)**
```python
# adk_agent_config.py (Hypothetical - needs research)
from adk import Agent, Tool, Memory
from adk.llm import OllamaProvider
from tools.google_workspace import CalendarTool, TasksTool

agent = Agent(
    name="federated-brain-agent",
    llm=OllamaProvider(model="gemma:3b", host="ollama:11434"),
    tools=[
        CalendarTool(auth="gcloud"),
        TasksTool(auth="gcloud"),
    ],
    memory=Memory(
        backend="filesystem",
        path="/mnt/knowledge",
        parsers=["xml", "markdown"],
    ),
    system_prompt="You are a proactive home OS...",
)
```

#### 1.2.2 Google Workspace Function Calling Layer

The agent will use **function calling** (not RAG) to interact with Google APIs:

```typescript
// tools/google-workspace/calendar.ts
export const calendarTools = [
  {
    name: "list_calendar_events",
    description: "Retrieve calendar events within a date range",
    parameters: {
      type: "object",
      properties: {
        calendarId: { type: "string", description: "Calendar ID or 'primary'" },
        timeMin: { type: "string", format: "date-time" },
        timeMax: { type: "string", format: "date-time" },
      },
      required: ["timeMin", "timeMax"],
    },
    handler: async (params) => {
      const calendar = google.calendar({ version: "v3", auth });
      const response = await calendar.events.list({
        calendarId: params.calendarId || "primary",
        timeMin: params.timeMin,
        timeMax: params.timeMax,
        singleEvents: true,
        orderBy: "startTime",
      });
      return response.data.items;
    },
  },
  
  {
    name: "create_calendar_event",
    description: "Create a new calendar event",
    parameters: {
      type: "object",
      properties: {
        calendarId: { type: "string" },
        summary: { type: "string" },
        start: { type: "object" },
        end: { type: "object" },
        attendees: { type: "array", items: { type: "string" } },
      },
      required: ["summary", "start", "end"],
    },
    handler: async (params) => {
      const calendar = google.calendar({ version: "v3", auth });
      return await calendar.events.insert({
        calendarId: params.calendarId || "primary",
        requestBody: {
          summary: params.summary,
          start: params.start,
          end: params.end,
          attendees: params.attendees?.map(email => ({ email })),
        },
      });
    },
  },
  
  {
    name: "detect_calendar_conflicts",
    description: "Check for scheduling conflicts across multiple calendars",
    parameters: {
      type: "object",
      properties: {
        calendarIds: { type: "array", items: { type: "string" } },
        proposedEvent: { type: "object" },
      },
      required: ["calendarIds", "proposedEvent"],
    },
    handler: async (params) => {
      // Custom logic to check for overlaps
      const conflicts = [];
      for (const calendarId of params.calendarIds) {
        const events = await listEvents(calendarId, 
          params.proposedEvent.start, 
          params.proposedEvent.end
        );
        if (events.length > 0) {
          conflicts.push({ calendarId, conflicts: events });
        }
      }
      return conflicts;
    },
  },
];

// Similar tools for Tasks, Docs, Sheets...
```

#### 1.2.3 Memory & Context Integration

**Knowledge Repository Structure:**
```
/mnt/knowledge/               # Read-only mount of my-code-brain
├── codebase/
│   ├── *.xml                 # Repomix code packs
│   └── digest_*.md           # Daily summaries
├── life-ops/
│   ├── personal/
│   │   └── daily-briefing-*.md
│   ├── work/
│   │   └── daily-briefing-*.md
│   └── ltc/
│       └── daily-briefing-*.md
└── chats/
    └── gemini-export-*.md
```

**Agent Memory Manager:**
```typescript
// memory/brain-memory.ts
export class BrainMemory {
  constructor(private knowledgePath: string) {}
  
  async getRelevantContext(query: string, maxTokens: number): Promise<string> {
    // 1. Semantic search across knowledge base
    const codeContext = await this.searchCodebase(query);
    const lifeContext = await this.searchLifeOps(query);
    const chatContext = await this.searchChats(query);
    
    // 2. Rank by relevance
    const ranked = this.rankResults([...codeContext, ...lifeContext, ...chatContext]);
    
    // 3. Truncate to token limit
    return this.truncateToTokens(ranked, maxTokens);
  }
  
  async getLatestBriefing(account: string = "personal"): Promise<DailyBriefing> {
    const files = await fs.readdir(`${this.knowledgePath}/life-ops/${account}`);
    const latest = files.sort().reverse()[0];
    return parseBriefing(await fs.readFile(latest, "utf-8"));
  }
  
  async getCodeContext(repoName: string): Promise<string> {
    const xmlPath = `${this.knowledgePath}/codebase/${repoName}.xml`;
    if (await fs.exists(xmlPath)) {
      return fs.readFile(xmlPath, "utf-8");
    }
    return "";
  }
}
```

**Proactive Agent Workflow:**
```typescript
// workflows/proactive-assistant.ts
export async function dailyRoutine(agent: Agent) {
  // 1. Read latest briefing from all accounts
  const briefings = await Promise.all([
    agent.memory.getLatestBriefing("personal"),
    agent.memory.getLatestBriefing("work"),
    agent.memory.getLatestBriefing("ltc"),
  ]);
  
  // 2. Detect conflicts
  const conflicts = await agent.tools.detect_calendar_conflicts({
    calendarIds: ["primary", "work@example.com", "spouse@example.com"],
    dateRange: { start: "today", end: "+7days" },
  });
  
  // 3. Generate suggestions
  if (conflicts.length > 0) {
    const suggestions = await agent.chat({
      message: `I detected ${conflicts.length} calendar conflicts. Here are the details: ${JSON.stringify(conflicts)}. What should we do?`,
      autoExecute: false, // Require user confirmation
    });
    
    return { type: "conflict_alert", conflicts, suggestions };
  }
  
  // 4. Check for overdue tasks
  const tasks = await agent.tools.list_tasks({ showCompleted: false });
  const overdue = tasks.filter(t => new Date(t.due) < new Date());
  
  if (overdue.length > 0) {
    return { type: "task_reminder", overdue };
  }
  
  return { type: "all_clear" };
}
```

### 1.3 Frontend Architecture (Next.js)

**Component Structure:**
```
nextjs-app/
├── app/
│   ├── page.tsx                    # Landing/Dashboard
│   ├── chat/page.tsx               # Agent chat interface
│   ├── calendar/page.tsx           # Calendar views
│   └── tasks/page.tsx              # Task management
├── components/
│   ├── AgentChat.tsx               # CopilotKit chat component
│   ├── CalendarView.tsx            # Multi-calendar display
│   ├── GanttChart.tsx              # Project timeline view
│   ├── ConflictAlert.tsx           # Proactive alert UI
│   └── TaskList.tsx                # Task widget
├── lib/
│   ├── copilot-provider.tsx        # CopilotKit setup
│   └── api-client.ts               # Backend communication
└── public/
```

**Key UI Features:**
1. **Agent Chat Interface:** Natural language input for all commands
2. **Unified Calendar Display:** Overlay multiple Google calendars (user, spouse, work)
3. **Gantt Chart View:** Project and task timelines with dependencies
4. **Conflict Alerts:** Real-time notifications for scheduling conflicts
5. **Daily Briefing Panel:** Display latest life-ops summaries

---

## 2. Deployment Strategy

### 2.1 Docker Compose Architecture

**File: `docker-compose.yml`**
```yaml
version: '3.8'

services:
  # ADK Agent Core
  agent:
    build: ./agent
    container_name: federated-brain-agent
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcloud-auth.json
      - GITHUB_TOKEN_FILE=/secrets/github-token
      - OLLAMA_HOST=ollama:11434
      - KNOWLEDGE_PATH=/mnt/knowledge
    volumes:
      - ./my-code-brain/knowledge:/mnt/knowledge:ro  # Read-only
      - agent-state:/app/state
      - ./secrets:/secrets:ro
      - logs:/app/logs
    networks:
      - brain-network
    depends_on:
      - ollama
    restart: unless-stopped

  # Local LLM Inference
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    volumes:
      - ollama-models:/root/.ollama
    networks:
      - brain-network
    restart: unless-stopped
    # Pull model on first run:
    # docker exec ollama ollama pull gemma:3b

  # Frontend (Next.js)
  frontend:
    build: ./frontend
    container_name: brain-frontend
    ports:
      - "3000:3000"
    environment:
      - AGENT_API_URL=http://agent:8000
      - NEXT_PUBLIC_WS_URL=ws://agent:8000/ws
    networks:
      - brain-network
    depends_on:
      - agent
    restart: unless-stopped

  # Home Assistant (Phase 2 - Optional)
  homeassistant:
    image: homeassistant/home-assistant:stable
    container_name: homeassistant
    volumes:
      - ha-config:/config
    network_mode: host  # Required for discovery
    restart: unless-stopped
    profiles:
      - phase2  # Only start with: docker-compose --profile phase2 up

volumes:
  agent-state:
  ollama-models:
  ha-config:
  logs:

networks:
  brain-network:
    driver: bridge
```

### 2.2 Authentication & Secrets Management

**Unified Authentication Strategy:**

1. **Google Cloud CLI (gcloud) for Google APIs:**
   ```bash
   # On host machine (one-time setup)
   gcloud auth application-default login
   
   # Mount credentials into containers
   volumes:
     - ~/.config/gcloud:/root/.config/gcloud:ro
   ```

2. **GitHub Personal Access Token:**
   ```bash
   # Store in secrets/github-token (gitignored)
   echo "ghp_xxxxxxxxxxxxx" > secrets/github-token
   chmod 600 secrets/github-token
   ```

3. **Environment Variables (`.env` file):**
   ```bash
   # .env (gitignored)
   GEMINI_API_KEY=xxxxx
   GITHUB_TOKEN=$(cat secrets/github-token)
   GOOGLE_WORKSPACE_DOMAIN=example.com
   PRIMARY_CALENDAR_ID=primary
   SPOUSE_CALENDAR_ID=spouse@example.com
   ```

### 2.3 Deployment Targets

**Phase 1: Development (Local)**
- Run on development machine (macOS/Linux)
- Use `docker-compose up` for all services
- Port 3000 exposed for frontend access

**Phase 2: Production (Home Server)**

**Option A: Bare Metal Linux Server**
- Thin Linux (Arch/Alpine) with Docker installed
- Static IP or DDNS for remote access
- Nginx reverse proxy for HTTPS
- Let's Encrypt for SSL certificates

**Option B: NAS (Synology/QNAP)**
- Docker via NAS UI (Container Manager)
- Built-in DDNS and SSL
- Easier for non-technical maintenance

**Server Requirements:**
- CPU: 4+ cores (for Ollama inference)
- RAM: 8GB minimum (16GB recommended)
- Storage: 50GB for Docker images + models
- Network: Stable internet for Google API calls

### 2.4 Deployment Workflow

```bash
# 1. Clone repositories
git clone https://github.com/flucido/my-code-brain.git
git clone https://github.com/flucido/federate-brain.git
cd federate-brain

# 2. Setup secrets
mkdir secrets
echo "ghp_xxxxx" > secrets/github-token
gcloud auth application-default login

# 3. Configure environment
cp .env.example .env
# Edit .env with your values

# 4. Pull Ollama model
docker-compose up -d ollama
docker exec ollama ollama pull gemma:3b

# 5. Start all services
docker-compose up -d

# 6. Verify
docker-compose ps
curl http://localhost:3000  # Frontend
curl http://localhost:8000/health  # Agent API
```

### 2.5 CI/CD Integration

**Existing Miner Workflows (Unchanged):**
- Code Miner: GitHub Actions on push → `knowledge/codebase/`
- Life-Ops Miner: Apps Script daily trigger → `knowledge/life-ops/`
- Chat Watcher: Apps Script on new docs → `knowledge/chats/`

**New Agent Deployment:**
```yaml
# .github/workflows/deploy-agent.yml
name: Deploy Agent to Home Server

on:
  push:
    branches: [main]
    paths:
      - 'agent/**'
      - 'frontend/**'
      - 'docker-compose.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker images
        run: |
          docker build -t ghcr.io/flucido/brain-agent:latest ./agent
          docker build -t ghcr.io/flucido/brain-frontend:latest ./frontend
          docker push ghcr.io/flucido/brain-agent:latest
          docker push ghcr.io/flucido/brain-frontend:latest
      
      - name: Deploy to home server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOME_SERVER_HOST }}
          username: ${{ secrets.HOME_SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd ~/federate-brain
            docker-compose pull
            docker-compose up -d
```

---

## 3. Critical Design Decisions

### 3.1 ADK vs CopilotKit: Technology Choice

**Decision Point:** Which framework should we use for the agent core?

| Aspect | CopilotKit | Pure ADK SDK | Hybrid Approach |
|--------|-----------|--------------|-----------------|
| **Maturity** | Production-ready | Unknown (need research) | Best of both |
| **React Integration** | Native | Manual | CopilotKit frontend, ADK backend |
| **Documentation** | Excellent | TBD | Mixed |
| **Learning Curve** | Moderate | Unknown | Highest |
| **Flexibility** | React-focused | Potentially more flexible | Most flexible |
| **Community** | Active | TBD | Both |

**RECOMMENDATION:** Start with **CopilotKit** for MVP due to:
1. Proven track record with Next.js
2. Built-in chat UI components
3. Strong TypeScript support
4. Active community

**Research Required:**
- [ ] What is "ADK SDK" specifically? (Mentioned in requirements but no docs found)
- [ ] Is it an acronym for "Agent Development Kit"?
- [ ] Is there an official ADK SDK, or is CopilotKit the intended solution?
- [ ] Can CopilotKit be considered part of the "ADK" ecosystem?

### 3.2 Local LLM: Ollama vs LM Studio

**Decision Point:** Which local inference engine?

| Feature | Ollama | LM Studio |
|---------|--------|-----------|
| **CLI-friendly** | ✅ Excellent | ❌ GUI-focused |
| **Docker support** | ✅ Official image | ⚠️ Requires workarounds |
| **Model management** | ✅ Simple (ollama pull) | ✅ GUI-based |
| **API compatibility** | ✅ OpenAI-compatible | ✅ OpenAI-compatible |
| **Resource usage** | ✅ Efficient | ✅ Efficient |
| **Headless deployment** | ✅ Perfect for servers | ❌ Designed for desktop |

**RECOMMENDATION:** **Ollama** for production deployment due to:
- Native Docker support
- CLI-first design (better for automation)
- Easy model updates (`ollama pull gemma:3b`)

**Keep LM Studio as:**
- Development alternative (for local testing with GUI)
- Fallback if Ollama has compatibility issues

### 3.3 Agent Memory: Git-Based vs Database

**Decision Point:** Where does the agent store its operational state?

**Current Design (Git-Based):**
- Knowledge: Read from `/mnt/knowledge` (git clone of my-code-brain)
- Agent State: Separate volume `/agent-state`

**Alternative (Unified Database):**
- Knowledge: Indexed in vector DB (e.g., Chroma, Qdrant)
- Agent State: Same database (conversations, decisions, schedules)

| Aspect | Git-Based (Current) | Vector Database |
|--------|---------------------|-----------------|
| **Simplicity** | ✅ Simple file reads | ❌ Requires DB setup |
| **Portability** | ✅ Git-native backup | ⚠️ DB exports needed |
| **Search Speed** | ❌ Slower for large repos | ✅ Optimized for search |
| **Multi-agent** | ✅ Shared read access | ✅ Concurrent queries |
| **Version control** | ✅ Native git history | ❌ Separate versioning |

**RECOMMENDATION:** **Hybrid approach**:
1. **Phase 1 (MVP):** Git-based file reading (simpler, leverages existing setup)
2. **Phase 2 (Optimization):** Add vector DB for semantic search, keep git as source of truth

**Implementation:**
```typescript
// Hybrid memory manager
class HybridMemory {
  private git: GitMemory;
  private vector: VectorDB | null;
  
  constructor(knowledgePath: string) {
    this.git = new GitMemory(knowledgePath);
    this.vector = process.env.ENABLE_VECTOR_DB === 'true' 
      ? new VectorDB() 
      : null;
  }
  
  async search(query: string) {
    if (this.vector) {
      return this.vector.semanticSearch(query);
    }
    return this.git.grepSearch(query);
  }
}
```

### 3.4 Miner Integration: Push to Git vs Direct Agent Memory

**Decision Point:** Should miners continue pushing to GitHub, or write directly to agent memory?

**Option A: Continue Git Push (Current Architecture)**
```
Miner → GitHub → Git Pull → Agent reads files
```
Pros:
- ✅ Preserves version history
- ✅ Knowledge accessible outside agent (NotebookLM, Cursor)
- ✅ No changes to existing miners
- ✅ Disaster recovery (GitHub as backup)

Cons:
- ❌ Latency (commit + pull cycle)
- ❌ Git overhead for high-frequency updates

**Option B: Direct Write to Shared Volume**
```
Miner → Shared Docker Volume → Agent reads files
```
Pros:
- ✅ Low latency (no git operations)
- ✅ Simpler for high-frequency updates

Cons:
- ❌ Loses git version control
- ❌ No external consumption (NotebookLM can't access)
- ❌ Requires refactoring miners

**RECOMMENDATION:** **Keep Git Push (Option A)** because:
1. Knowledge base is explicitly designed for multi-tool consumption
2. Version control is valuable for debugging/analysis
3. Existing miners already work this way
4. Agent can still pull updates frequently (cron every 5 minutes)

**Optimization for Phase 2:**
- Add webhook from GitHub to agent: "New commit → trigger pull"
- Agent subscribes to GitHub push events for near-real-time updates

### 3.5 Home Assistant: MVP vs Phase 2

**Decision Point:** Is Home Assistant essential for MVP?

**Arguments for MVP inclusion:**
- Physical home automation (lights, sensors) is a stated requirement
- Demonstrates full "home OS" vision
- Integration complexity may delay other features

**Arguments for Phase 2:**
- Calendar/task management alone is valuable
- Google Workspace integration is more complex
- Can validate agent architecture without IoT complexity

**RECOMMENDATION:** **Defer to Phase 2** because:
1. MVP should focus on proving agent + Google Workspace integration
2. Home Assistant adds significant testing complexity (requires physical devices)
3. "Home OS" can initially mean "digital life OS" before "smart home OS"

**Phase 1 Scope:**
- ✅ Calendar conflict detection
- ✅ Task management
- ✅ Meeting scheduling
- ✅ Document creation

**Phase 2 Addition:**
- ⬜ Light control ("Turn off lights when calendar shows away")
- ⬜ Presence detection ("Family arriving home, prepare briefing")
- ⬜ Environmental automation ("Too hot during meeting, adjust AC")

---

## 4. Implementation Phases

### Phase 0: Archive & Foundation (Week 1)

**Objectives:**
- Preserve existing 60% complete work
- Setup Docker development environment
- Establish project structure

**Tasks:**
1. Create `legacy/` directory structure:
   ```
   legacy/
   ├── README.md             # "Why we archived, how to restore"
   ├── tui/                  # Existing Textual TUI
   ├── operations/           # Document operations
   ├── specs/                # Specification system
   └── reviews/              # Code reviews
   ```

2. Draft `legacy/README.md` explaining:
   - These components are functional and tested
   - They will be reintegrated in Phase 3+ as monitoring/admin tools
   - How to run the TUI standalone for debugging

3. Create Docker skeleton:
   ```bash
   mkdir -p agent/{src,tests,Dockerfile}
   mkdir -p frontend/{app,components,lib,Dockerfile}
   mkdir secrets
   touch docker-compose.yml .env.example
   ```

4. Research ADK/CopilotKit:
   - [ ] Clarify "ADK SDK" terminology
   - [ ] Review CopilotKit documentation
   - [ ] Prototype simple agent with function calling

**Deliverables:**
- [x] `legacy/` directory with preserved code
- [ ] `docker-compose.yml` with all services defined
- [ ] `.env.example` with required variables
- [ ] Research document: "ADK-vs-CopilotKit-findings.md"

### Phase 1: Agent Core MVP (Weeks 2-4)

**Objectives:**
- Functional ADK agent with Google Workspace integration
- Basic Next.js frontend with chat interface
- Agent can read from `knowledge/` directory

**Agent Capabilities (MVP):**
1. **Calendar Management:**
   - List events from multiple calendars
   - Detect conflicts
   - Suggest alternative times

2. **Task Management:**
   - List tasks from Google Tasks
   - Create new tasks
   - Mark tasks complete

3. **Knowledge Context:**
   - Read latest daily briefing
   - Answer questions about recent code changes
   - Summarize chat history

**Frontend Features (MVP):**
1. Chat interface (CopilotKit component)
2. Calendar view (read-only, multi-calendar overlay)
3. Task list (read-only)
4. Daily briefing panel

**Tasks:**
1. Implement Google Workspace function calling layer
2. Create agent configuration with Ollama backend
3. Build Next.js app with CopilotKit integration
4. Mount `my-code-brain/knowledge` as read-only volume
5. Test end-to-end: "Show me conflicts in next week"

**Success Criteria:**
- [ ] Agent can list calendar events from 2+ calendars
- [ ] Agent detects scheduling conflicts
- [ ] Agent reads and references daily briefing
- [ ] Frontend chat interface responds within 3 seconds
- [ ] All services start with `docker-compose up`

### Phase 2: Proactive Features & Gantt (Weeks 5-7)

**Objectives:**
- Agent proactively alerts on conflicts (push, not pull)
- Advanced calendar visualizations (Gantt charts)
- Multi-account support in UI

**New Capabilities:**
1. **Proactive Monitoring:**
   - Daily cron job: check for new conflicts
   - Push notifications to frontend
   - Email digest option

2. **Advanced Visualization:**
   - Gantt chart for project timelines
   - Task dependency tracking
   - Color-coded calendar overlay (personal/work/family)

3. **Multi-Account Management:**
   - Toggle between personal/work/ltc contexts
   - Unified search across all briefings
   - Account-specific task lists

**Tasks:**
1. Implement agent background jobs (cron-like)
2. Add WebSocket push to frontend
3. Build Gantt chart component (React)
4. Enhance memory manager for multi-account queries

**Success Criteria:**
- [ ] Agent sends alert within 5 minutes of conflict appearing
- [ ] Gantt chart displays 30-day project view
- [ ] Can switch between accounts in UI without refresh

### Phase 3: Home Assistant & Physical Automation (Weeks 8-10)

**Objectives:**
- Integrate Home Assistant container
- Context-aware home automation
- Reintegrate legacy TUI as admin tool

**New Capabilities:**
1. **Home Automation:**
   - "Turn off lights when away" (calendar-based)
   - "Adjust thermostat for meetings" (focus mode)
   - Presence detection integration

2. **Admin Tooling:**
   - Restore TUI as monitoring dashboard (read agent logs)
   - Use existing "Operations" for agent debugging
   - Spec system for agent capability documentation

**Tasks:**
1. Add Home Assistant to docker-compose.yml
2. Create agent tools for HA integration
3. Build automation rules in HA linked to calendar
4. Port TUI to run as monitoring service (read-only agent state)

**Success Criteria:**
- [ ] Lights turn off when calendar shows "Away"
- [ ] Agent can report current home temperature
- [ ] TUI displays agent decision log in real-time

### Phase 4: Optimization & Polish (Weeks 11-12)

**Objectives:**
- Performance tuning
- Security hardening
- Documentation completion

**Tasks:**
1. Add vector database for faster semantic search
2. Implement agent conversation history pruning
3. Security audit (secret rotation, API rate limits)
4. Write comprehensive deployment guide
5. Create demo video

**Success Criteria:**
- [ ] Agent response time < 2 seconds (95th percentile)
- [ ] All secrets in environment variables (no hardcoding)
- [ ] README enables new user to deploy in < 30 minutes
- [ ] Demo showcases all key features in 5-minute video

---

## 5. Open Questions & Research Needed

### 5.1 ADK/CopilotKit Clarification

**Critical Unknowns:**

1. **What is "ADK SDK"?**
   - Is this an official Adobe/Microsoft/Google product?
   - Or is it a conceptual "Agent Development Kit"?
   - Does CopilotKit qualify as an "ADK"?
   - Should we use a different framework entirely?

2. **CopilotKit Native Function Calling:**
   - Does CopilotKit support native Google API function calling?
   - Or do we need to wrap Google APIs in custom CopilotKit tools?
   - Example code needed for Google Calendar integration

3. **Ollama Integration with CopilotKit:**
   - CopilotKit examples use OpenAI—does it support Ollama?
   - Do we need an OpenAI-compatible proxy (e.g., LiteLLM)?
   - What's the configuration for local models?

**Research Tasks:**
- [ ] Search for "ADK SDK agent framework" official documentation
- [ ] Review CopilotKit docs: custom LLM providers
- [ ] Test CopilotKit + Ollama compatibility
- [ ] Prototype Google Calendar tool in CopilotKit

### 5.2 Architecture & Data Flow

**Unknowns:**

1. **Agent State Persistence:**
   - Where does the agent store conversation history?
   - Should it commit decisions to git, or use a separate DB?
   - How to handle multi-session state (user + spouse)?

2. **Knowledge Update Frequency:**
   - How often should agent pull from `my-code-brain`?
   - Real-time (git hooks) or polling (every 5 min)?
   - Does agent cache knowledge, or read on-demand?

3. **Multi-Calendar Permissions:**
   - How to authenticate for spouse's calendar?
   - Shared family calendar, or separate OAuth flows?
   - What Google Workspace plan supports this?

**Research Tasks:**
- [ ] Define agent state schema (conversations, decisions, user prefs)
- [ ] Test GitHub webhook → Docker container trigger
- [ ] Research Google Workspace shared calendar permissions

### 5.3 Deployment & Operations

**Unknowns:**

1. **Home Server Specs:**
   - What CPU/RAM for Gemma 3B inference?
   - Does Ollama support GPU acceleration in Docker?
   - Estimated inference time per query?

2. **Network & Security:**
   - How to expose frontend securely (VPN vs public HTTPS)?
   - Recommended firewall rules for Docker services?
   - How to rotate Google API credentials?

3. **Backup & Disaster Recovery:**
   - How to backup agent state (Docker volumes)?
   - What happens if `my-code-brain` repo is corrupted?
   - Rollback strategy for bad agent updates?

**Research Tasks:**
- [ ] Benchmark Ollama gemma:3b on target hardware
- [ ] Design backup script for Docker volumes → git
- [ ] Write disaster recovery runbook

### 5.4 Integration & Testing

**Unknowns:**

1. **Miner Compatibility:**
   - Do existing Google Apps Script miners need changes?
   - Should we migrate to Cloud Functions for better integration?
   - How to test miners in development (mock Google APIs)?

2. **Agent Testing Strategy:**
   - Unit tests for individual tools?
   - Integration tests for full workflows?
   - How to mock Google Calendar in tests?

3. **UI/UX Design:**
   - Chat-first or dashboard-first interface?
   - Mobile responsiveness requirements?
   - Accessibility standards (WCAG)?

**Research Tasks:**
- [ ] Review existing miner code for refactor needs
- [ ] Setup test environment with mock Google APIs
- [ ] Create UI mockups for key screens

---

## 6. Risk Analysis

### 6.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **ADK/CopilotKit incompatibility** | Medium | High | Start with CopilotKit MVP, keep architecture modular for framework swap |
| **Ollama performance insufficient** | Low | High | Benchmark early, have Gemini API fallback |
| **Google API rate limits** | Medium | Medium | Cache responses, implement exponential backoff |
| **Docker networking issues** | Low | Medium | Use well-documented bridge network, test early |
| **Calendar conflict logic bugs** | High | Low | Comprehensive test suite, manual QA |
| **Data loss (agent state)** | Low | High | Automated backups to git, Docker volume snapshots |

### 6.2 Product Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Agent suggestions are poor** | Medium | High | Tune prompts iteratively, add user feedback loop |
| **UI too complex** | Medium | Medium | User testing at each phase, keep chat as fallback |
| **Slow inference (>5s)** | Low | High | Use smaller model (Gemma 2B), optimize context size |
| **Google Workspace permissions issues** | Medium | Medium | Document required scopes, test with limited access |

### 6.3 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Home server downtime** | Medium | Medium | Cloud backup, mobile access to Google Calendar directly |
| **API key compromise** | Low | Critical | Rotate keys regularly, use least-privilege scopes |
| **Miner failures (miners stop working)** | Medium | Medium | Add health checks, email alerts on failure |
| **Docker volume corruption** | Low | High | Daily backups, test restore procedure |

---

## 7. Success Metrics

### 7.1 MVP Success Criteria (Phase 1)

**Functional:**
- [ ] Agent responds to 10 sample queries correctly
- [ ] Detects conflicts in multi-calendar scenario
- [ ] Frontend loads in < 3 seconds
- [ ] No crashes during 24-hour stress test

**Performance:**
- [ ] Agent response time: < 5s (p95)
- [ ] Memory usage: < 4GB total (all containers)
- [ ] Disk usage: < 20GB

**User Experience:**
- [ ] Can complete calendar conflict check in < 5 clicks
- [ ] Chat interface feels responsive (< 1s to show "thinking")
- [ ] Daily briefing loads without scrolling

### 7.2 Production Success Metrics (Phase 4)

**Reliability:**
- [ ] 99% uptime over 30 days
- [ ] < 5 minutes to recover from crash
- [ ] Zero data loss incidents

**Accuracy:**
- [ ] 95% of conflict detections are true positives
- [ ] Agent suggestions accepted by user 70%+ of time
- [ ] Task auto-creation error rate < 5%

**Performance:**
- [ ] Agent response time: < 2s (p95)
- [ ] Supports 100+ calendar events without slowdown
- [ ] Gantt chart renders 30 days in < 1s

**Adoption:**
- [ ] User checks dashboard daily
- [ ] 50%+ of tasks created via agent (not manual)
- [ ] Spouse uses unified calendar view

---

## Next Steps

1. **Immediate (This Week):**
   - [ ] Clarify ADK SDK vs CopilotKit decision
   - [ ] Archive existing code to `legacy/`
   - [ ] Create `docker-compose.yml` skeleton
   - [ ] Research Google Workspace API authentication

2. **Short-term (Next 2 Weeks):**
   - [ ] Build CopilotKit + Ollama proof-of-concept
   - [ ] Implement first Google Calendar tool
   - [ ] Test knowledge mount (read latest briefing)
   - [ ] Create basic Next.js frontend

3. **Medium-term (Month 1):**
   - [ ] Complete Phase 1 MVP
   - [ ] Deploy to development environment
   - [ ] User testing with real calendars
   - [ ] Iterate based on feedback

---

## Appendices

### A. Glossary

- **ADK:** Agent Development Kit (clarification needed)
- **CopilotKit:** React framework for building AI copilots
- **Function Calling:** LLM capability to invoke external APIs
- **Gemma:** Google's small LLM family (2B, 3B parameters)
- **Ollama:** Local LLM inference engine
- **Repomix:** Tool to pack codebase into XML

### B. References

- [Agent Context Document](./Agent%20Context_%20Federated%20Brain%20System.md)
- [Original Project Plan](./project_overview_and_plan.md)
- CopilotKit Documentation: https://docs.copilotkit.ai/
- Google Calendar API: https://developers.google.com/calendar/api
- Ollama Documentation: https://ollama.ai/docs

### C. Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-12-28 | Use CopilotKit for MVP | Better documentation than undefined "ADK SDK" |
| 2025-12-28 | Ollama over LM Studio | Docker-first design, CLI-friendly |
| 2025-12-28 | Keep Git-based knowledge | Preserves multi-tool consumption (NotebookLM) |
| 2025-12-28 | Defer Home Assistant to Phase 2 | Focus MVP on Google Workspace integration |

---

**Document Status:** Draft v1.0  
**Next Review:** After ADK/CopilotKit research complete  
**Owner:** Project Lead  
**Last Updated:** December 28, 2025
