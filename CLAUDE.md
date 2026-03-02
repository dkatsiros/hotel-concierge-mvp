# Hotel Concierge MVP

Voice-capable AI concierge for hotel guest requests.

## Stack
- Backend: FastAPI + SQLAlchemy async + PostgreSQL + Alembic
- Frontend: React 18 + TypeScript + Vite + Tailwind v4
- Voice: ElevenLabs Conversational AI (STT → Claude → TTS)
- Text chat: WebSocket + Claude API (Anthropic SDK)
- Hotel data: JSON + plain .txt files in `backend/data/`

## Commands
```bash
# Dev
docker compose up          # start all services
docker compose up --build  # rebuild + start

# Backend
cd backend && pip install -r requirements.txt
alembic upgrade head       # run migrations
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install
npm run dev

# Migrations
cd backend && alembic revision --autogenerate -m "description"
cd backend && alembic upgrade head
```

## Structure
- `backend/app/` — FastAPI application
- `backend/data/` — hotel knowledge base (JSON + txt)
- `frontend/src/` — React application
- UUID primary keys on all models
- Pydantic v2 schemas
- Async SQLAlchemy throughout

## Conventions
- No auth in Phase 1 (anonymous sessions)
- JSON data files can reference .txt files for long-form content
- WebSocket at `/ws/chat` for text chat
- Health checks at `/health` and `/health/db`
- ElevenLabs webhook tools: `POST /api/tools/{tool_name}`
- Tool modules in `backend/app/tools/` — auto-discovered via registry
- Adding a new tool: create module with `TOOL_CONFIG` + `handler` in `backend/app/tools/`, restart
- `WEBHOOK_BASE_URL` env var required for tool sync (use Tailscale Funnel or ngrok)

## Config / Env Vars
- `CHAT_PROVIDER` — `anthropic` (default) or `openai`
- `CHAT_MODEL` — optional model override; defaults to `claude-sonnet-4-20250514` / `gpt-4o`
- `ANTHROPIC_API_KEY` — required when provider is anthropic
- `OPENAI_API_KEY` — required when provider is openai

# Rules
- When making any architectural change, it should always be reflected on the claude.md file.
- Always commit after making changes.