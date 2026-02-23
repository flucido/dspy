# Dr. Ogren Apps

A multi-project repository containing the Lauren Ogren Therapy website and related tools.

---

## Projects

### `dlo/` — Lauren Ogren Therapy Website

A modern, responsive website built with Next.js 15, Tailwind CSS, and ShadCN UI.

| Aspect | Details |
|--------|---------|
| **Type** | Next.js 15 (App Router) |
| **Tech** | TypeScript, Tailwind CSS 4, ShadCN UI |
| **Features** | Focus Reader (boustrophedon text transformation), responsive design |
| **Deploy** | Vercel |

**Quick Start:**
```bash
cd dlo
npm install
npm run dev
```

---

### `bookmaker/` — OxTurn Learning Engine

A Python-based boustrophedon text transformation engine with FastAPI backend.

| Aspect | Details |
|--------|---------|
| **Type** | Python CLI + FastAPI |
| **Tech** | Python 3.11+, ReportLab, FastAPI |
| **Features** | PDF/EPUB generation, boustrophedon text layout |
| **Deploy** | Separate API server |

**Quick Start:**
```bash
cd bookmaker
uv sync
./run_api.sh --reload  # Starts API at http://localhost:8000
```

---

### `content/` — Sample Content

Sample text files for testing the OxTurn transformation.

---

### `spatial audio/` — Future Project

Placeholder for an upcoming spatial audio project.

---

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   dlo/          │   HTTP  │   bookmaker/    │
│   (Next.js)     │ ──────► │   (FastAPI)     │
│                 │         │                 │
│  /api/oxturn    │         │   /transform    │
│  (proxy route)  │         │   /health       │
└─────────────────┘         └─────────────────┘
        │                           │
        ▼                           ▼
    Vercel                    API Server
   (Frontend)              (OXTURN_API_URL)
```

### Connection

The `dlo` frontend includes a **Focus Reader** feature that transforms text using the boustrophedon method. This is powered by the `bookmaker` backend:

1. Frontend calls `/api/oxturn` (Next.js API route)
2. API route proxies to `OXTURN_API_URL` (FastAPI backend)
3. Backend transforms text and returns result

**Environment Variables:**

| Variable | Required | Description |
|----------|----------|-------------|
| `OXTURN_API_URL` | Production | URL of the OxTurn API (e.g., `https://api.example.com`) |

In development, the API defaults to `http://localhost:8000`.

---

## Local Development

### Prerequisites

- Node.js 18+ (for `dlo`)
- Python 3.11+ and [uv](https://docs.astral.sh/uv/) (for `bookmaker`)

### Running Both Projects

**Terminal 1 — Backend:**
```bash
cd bookmaker
uv sync
./run_api.sh --reload
# API runs at http://localhost:8000
```

**Terminal 2 — Frontend:**
```bash
cd dlo
npm install
npm run dev
# Website runs at http://localhost:3000
```

The frontend will automatically connect to the local API.

---

## Deployment

| Project | Platform | Notes |
|---------|----------|-------|
| `dlo/` | Vercel | Auto-deploys from `main` branch |
| `bookmaker/` | API Server | Set `OXTURN_API_URL` in Vercel environment |

See [`dlo/DEPLOYMENT.md`](dlo/DEPLOYMENT.md) for Vercel deployment details.

---

## Development Commands

### dlo (Frontend)

```bash
cd dlo
npm run dev        # Start development server
npm run build      # Production build
npm run lint       # Run ESLint
npm run test       # Run Vitest tests
npm run typecheck  # TypeScript check
```

### bookmaker (Backend)

```bash
cd bookmaker
uv sync            # Install dependencies
./run_api.sh       # Start API server
./run_api.sh --reload  # Start with auto-reload
uv run pytest      # Run tests
uv run ruff check oxturn  # Lint
uv run mypy oxturn # Type check
```

---

## Project Status

| Project | Status |
|---------|--------|
| `dlo/` | Active development |
| `bookmaker/` | Active development |
| `spatial audio/` | Planned |

---

## License

MIT License — see individual project directories for details.
