# Recommended LLM Models by Provider

A curated list of models for each API key you're using, rated out of 10 for overall
capability (reasoning, coding, and general performance). Each provider lists:
**2 Best**, **2 Better**, and **1 Good** model.

> Ratings are general-purpose guidance as of mid-2026. Model availability changes
> frequently — check each provider's dashboard for the current catalog and exact IDs.

---

## OpenAI (`OPENAI_API_KEY`)

| Tier | Model | Model ID | Rating | Notes |
|------|-------|----------|--------|-------|
| 🥇 Best | GPT-5 | `gpt-5` | 10/10 | Flagship reasoning + general model. |
| 🥇 Best | o3 | `o3` | 9.5/10 | Deep reasoning for math, science, hard coding. |
| 🥈 Better | GPT-4.1 | `gpt-4.1` | 9/10 | Strong coding + long context, cost-effective. |
| 🥈 Better | GPT-4o | `gpt-4o` | 8.5/10 | Fast multimodal all-rounder. |
| 🥉 Good | GPT-4o mini | `gpt-4o-mini` | 7.5/10 | Cheap, fast, great for high-volume tasks. |

---

## Groq (`GROQ_API_KEY`)

Groq is an ultra-fast inference provider hosting open-weight models.

| Tier | Model | Model ID | Rating | Notes |
|------|-------|----------|--------|-------|
| 🥇 Best | Llama 3.3 70B | `llama-3.3-70b-versatile` | 9/10 | Best overall quality on Groq, very fast. |
| 🥇 Best | DeepSeek R1 Distill 70B | `deepseek-r1-distill-llama-70b` | 8.8/10 | Strong reasoning at blazing speed. |
| 🥈 Better | Qwen 2.5 32B | `qwen-2.5-32b` | 8/10 | Solid coding + multilingual balance. |
| 🥈 Better | Mixtral 8x7B | `mixtral-8x7b-32768` | 7.5/10 | MoE model, long 32k context. |
| 🥉 Good | Llama 3.1 8B | `llama-3.1-8b-instant` | 7/10 | Lightweight, extremely low latency. |

---

## OpenRouter (`OPENROUTER_API_KEY`)

OpenRouter aggregates models from many providers behind one API.

| Tier | Model | Model ID | Rating | Notes |
|------|-------|----------|--------|-------|
| 🥇 Best | Claude Opus 4.8 | `anthropic/claude-opus-4.8` | 10/10 | Top-tier reasoning, coding, and agentic work. |
| 🥇 Best | GPT-5 | `openai/gpt-5` | 10/10 | Flagship OpenAI model via OpenRouter. |
| 🥈 Better | Gemini 2.5 Pro | `google/gemini-2.5-pro` | 9/10 | Huge context window, strong multimodal. |
| 🥈 Better | Claude Sonnet 5 | `anthropic/claude-sonnet-5` | 8.8/10 | Fast, cost-efficient, excellent coder. |
| 🥉 Good | DeepSeek V3 | `deepseek/deepseek-chat` | 8/10 | Very strong open model, low cost. |

---

## Quick Picks

- **Highest quality, cost no object:** OpenAI `gpt-5` or OpenRouter `anthropic/claude-opus-4.8`
- **Best speed-to-quality ratio:** Groq `llama-3.3-70b-versatile`
- **Cheapest usable option:** OpenAI `gpt-4o-mini` or Groq `llama-3.1-8b-instant`
- **Best for long documents:** OpenRouter `google/gemini-2.5-pro`
