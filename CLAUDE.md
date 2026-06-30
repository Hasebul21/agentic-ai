# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start PostgreSQL + run main.py
make run

# Database management
make seed          # Populate with e-commerce sample data
make reset         # Drop → recreate → migrate → re-seed
make stop          # Stop PostgreSQL container
make logs          # Stream PostgreSQL logs

# Run specific modules directly
PYTHONPATH=. .venv/bin/python db/queries.py
PYTHONPATH=. .venv/bin/python db/raw_queries.py
PYTHONPATH=. .venv/bin/python db/seed.py

# Database migrations
PYTHONPATH=. .venv/bin/alembic upgrade head
PYTHONPATH=. .venv/bin/alembic revision --autogenerate -m "description"

# Jupyter notebooks
jupyter lab
```

All Python commands must be run with `PYTHONPATH=.` and use `.venv/bin/python` (not system Python).

## Architecture

This is a Python 3.12 learning environment for Agentic AI concepts, combining a PostgreSQL-backed e-commerce dataset with LLM integration via OpenAI and Anthropic SDKs.

### Layers

**Database layer** (`db/`): SQLAlchemy 2.x ORM over PostgreSQL 16 (Docker). Eight tables model an e-commerce domain: `categories`, `suppliers`, `products`, `inventory`, `customers`, `orders`, `order_items`, and `conversations` (for storing LLM chat history). `db/database.py` creates the engine and `SessionLocal` factory; `db/models.py` defines all ORM models with relationships; `db/crud.py` handles conversation persistence; `db/queries.py` contains 15 sample ORM queries across easy/medium/complex difficulty for learning.

**Migrations** (`alembic/`): Alembic reads `DATABASE_URL` from `.env` via `alembic/env.py`. A single initial migration (`alembic/versions/83367c40cb1e_initial_schema.py`) creates the full schema.

**Entry point** (`main.py`): Loads `.env`, initializes OpenAI client (`gpt-4o-mini`), queries inventory via SQLAlchemy, and prints results. This is a minimal demo combining DB + LLM.

**Learning modules** (not yet created, defined in README):
- `01_basics/` — Chat completions, streaming, structured output
- `02_tools_and_function_calling/` — Tool schemas, agent loops
- `03_rag/` — Embeddings, vector stores (ChromaDB, FAISS), RAG pipeline
- `04_agents/` — ReAct pattern (Thought → Action → Observation)
- `05_multi_agent/` — Multi-agent orchestration
- `06_langgraph/` — State graphs, conditional routing, memory

### Key dependencies

| Package | Purpose |
|---|---|
| `openai` 2.44.0 | Primary LLM client |
| `anthropic` 0.113.0 | Claude API client |
| `langchain` + `langgraph` | Agent frameworks |
| `sqlalchemy` + `alembic` | ORM + migrations |
| `chromadb`, `faiss-cpu` | Vector stores for RAG |
| `sentence-transformers` | Local embeddings |
| `tavily-python`, `duckduckgo-search` | Web search tools |
| `pydantic` 2.x | Data validation |
| `rich` | Terminal output formatting |

### Environment variables

Copy `.env.example` to `.env` and fill in:
- `OPENAI_API_KEY` — required
- `ANTHROPIC_API_KEY` — for Claude experiments
- `TAVILY_API_KEY` — for web search tools
- `LANGSMITH_API_KEY` + `LANGSMITH_TRACING=true` — for LangSmith tracing
- `DATABASE_URL` — defaults to `postgresql://agentic:agentic123@localhost:5432/agentic_ai`

### Docker

PostgreSQL 16 runs in a container named `agentic_ai_db` (port 5432). `make run` handles container startup and waits for readiness before executing Python. Data persists in the `postgres_data` volume; `make reset` does a full wipe and re-seed.
