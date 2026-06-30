# Agentic AI — Practice Environment

A structured Python workspace for learning and practising Agentic AI concepts.

---

## Prerequisites

- Python 3.12 (already available at `/opt/homebrew/bin/python3.12`)
- An OpenAI API key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## 1. Activate the virtual environment

The `.venv` is already created with all packages installed. Just activate it:

```bash
# from the project root
source .venv/bin/activate
```

To deactivate later:

```bash
deactivate
```

---

## 2. Set up your API key

Copy the example env file and add your key:

```bash
cp .env.example .env
```

Open `.env` and fill in at minimum:

```
OPENAI_API_KEY=sk-your-key-here
```

The other keys are optional and only needed for specific tools:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Use Claude models |
| `TAVILY_API_KEY` | Web search tool (free tier available) |
| `LANGSMITH_API_KEY` | Tracing & debugging with LangSmith |

---

## 3. Run a Python file

```bash
python 01_basics/your_file.py
```

---

## 4. Open Jupyter Notebook

```bash
jupyter lab
```

This opens in your browser. Notebooks go in the `notebooks/` folder.

---

## Project Structure

```
Agentic_AI/
├── .env                          ← your API keys (never commit this)
├── .env.example                  ← template to copy from
├── .venv/                        ← virtual environment (Python 3.12)
│
├── 01_basics/                    ← OpenAI API, chat, streaming, structured output
├── 02_tools_and_function_calling/← tool definitions, function calling, agent loop
├── 03_rag/                       ← embeddings, vector stores, RAG pipeline
├── 04_agents/                    ← ReAct agent pattern from scratch
├── 05_multi_agent/               ← multi-agent orchestration patterns
├── 06_langgraph/                 ← stateful graphs, memory, conditional routing
└── notebooks/                    ← Jupyter notebooks for experimentation
```

---

## Installed Packages

| Package | Version | Purpose |
|---|---|---|
| `openai` | 2.44.0 | OpenAI API client |
| `anthropic` | 0.113.0 | Claude API client |
| `langchain` | 1.3.11 | LLM application framework |
| `langchain-openai` | 1.3.3 | LangChain + OpenAI integration |
| `langchain-community` | 0.4.2 | Community tools and loaders |
| `langgraph` | 1.2.7 | Stateful agent graphs |
| `chromadb` | 1.5.9 | Vector database |
| `faiss-cpu` | 1.14.3 | Fast similarity search |
| `sentence-transformers` | 5.6.0 | Local embedding models |
| `pydantic` | 2.13.4 | Data validation & structured output |
| `tavily-python` | 0.7.26 | Web search tool for agents |
| `duckduckgo-search` | 8.1.1 | Free web search tool |
| `wikipedia` | 1.4.0 | Wikipedia lookup tool |
| `rich` | 15.0.0 | Pretty terminal output |
| `jupyter` | 1.1.1 | Notebook environment |

---

## Concepts Covered (by folder)

| Folder | Concepts |
|---|---|
| `01_basics` | Chat completions, streaming, conversation history, structured output |
| `02_tools_and_function_calling` | Tool schemas, model-driven tool selection, multi-turn tool loops |
| `03_rag` | Chunking, embeddings, vector search, grounded generation |
| `04_agents` | ReAct pattern, Thought → Action → Observation loop |
| `05_multi_agent` | Orchestrator + specialist agents, agent pipelines |
| `06_langgraph` | State graphs, nodes, edges, conditional routing, checkpointing/memory |
