<div align="center">

# Pokémon AI Agents

**LLM-powered AI agents that play Pokémon Showdown autonomously.**

Watch Large Language Models battle each other in real-time, or challenge them yourself.

[![Python 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-Integrated-green.svg)](https://litellm.ai/)
[![Langfuse](https://img.shields.io/badge/Langfuse-Traced-orange.svg)](https://langfuse.com/)

<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWxlZ2J5d3N2Nm9oanRldTA3aGw4NHFrcW53ZGk1bWdzaWtlaGJwZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/xeuSulJ22SiTaZWBoD/giphy.gif" width="100" alt="Pikachu" />

*🎶 I wanna be the very best ... Like no one ever was 🎶*

<br>

[![Pokémon AI Agent Demo](https://raw.githubusercontent.com/MohamedMostafa259/pokemon-ai-agent/main/pokemon-ai-agent-demo.gif)](https://youtu.be/8ZNadmh-Sy8)

[**▶️ Watch the full video demo with audio on YouTube**](https://youtu.be/8ZNadmh-Sy8)

</div>

---

## What is this?

This project connects state-of-the-art LLMs (Llama, Gemma, Qwen, Mistral, and more) to a local [Pokémon Showdown](https://pokemonshowdown.com/) server via [poke-env](https://github.com/hsahovic/poke-env). The AI receives the full battle state each turn, reasons about type matchups, HP, field conditions, and revealed opponent information, then decides whether to attack or switch using tool calls.

A [Gradio](https://gradio.app/) interface lets you:
- **Human vs. AI** - Play against any supported LLM yourself.
- **AI vs. AI** - Pick two models and watch them fight autonomously.

All LLM calls are routed through [LiteLLM](https://litellm.ai/) and traced via [Langfuse](https://langfuse.com/) for observability.

## Quickstart

### Prerequisites

- [Python 3.14+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/) (for the Showdown server and client)

### 1. Clone and configure

```bash
git clone https://github.com/MohamedMostafa259/pokemon-ai-agent.git
cd pokemon-ai-agent
```

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and paste your API keys. See [Getting API Keys](#getting-api-keys) below.

### 2. Create venv and install dependencies

```bash
uv venv
.venv/scripts/activate
uv sync
```

### 3. Run

```bash
uv run python run.py
```

This single command will:
1. Clone the Showdown server and client repos (first run only).
2. Install their Node.js dependencies and build the client.
3. Start the local Showdown server on port `8000`.
4. Launch the Gradio control panel on port `7860`.

### 4. Play

| What | URL |
|------|-----|
| **Gradio Control Panel** | [http://127.0.0.1:7860](http://127.0.0.1:7860) |
| **Showdown Client** (spectate/play) | [http://localhost:8000](http://localhost:8000) |

**"Human vs. AI" flow:**
1. Open the Showdown client and log in with any username.
2. In the Gradio panel, select an AI model, enter your Showdown username and a bot name, then click "Send Challenge."
3. Accept the challenge in the Showdown client.

**"AI vs. AI" flow:**
1. Open the Showdown client and log in with any username.
2. In the Gradio panel, select two AI models, enter their bot names, then click "Start AI vs. AI Battle."
3. The two AIs will battle each other autonomously.

## Getting API Keys

All models in this project use **free-tier API quotas** (as of April 2026, per [free-llm-api-resources](https://github.com/cheahjs/free-llm-api-resources)). Just create a free account on each provider's platform, generate an API key, and paste it into `.env`.

| Provider | Env Variable |
|----------|-------------|
| [OpenRouter](https://openrouter.ai/) | `OPENROUTER_API_KEY` |
| [Cerebras](https://cloud.cerebras.ai/) | `CEREBRAS_API_KEY` |
| [Google AI Studio](https://aistudio.google.com/) | `GEMINI_API_KEY` |
| [Groq](https://console.groq.com/) | `GROQ_API_KEY` |
| [Mistral](https://console.mistral.ai/) | `MISTRAL_API_KEY` |

You only need keys for the providers whose models you want to use. If you only want to try Cerebras models, only `CEREBRAS_API_KEY` is required.

### Using Paid Tiers for More Powerful Models

If you have a paid API key (e.g., Gemini Pro, OpenAI GPT-4, Anthropic Claude), you can add any model supported by [LiteLLM](https://docs.litellm.ai/docs/providers) to the `MODEL_MAP` dictionary in `battle_runners.py`:

```python
MODEL_MAP = {
    # ... existing free models ...

    # Examples of paid models you could add:
    "OpenAI GPT-4o": "openai/gpt-4o",
    "Anthropic Claude Sonnet 4": "anthropic/claude-sonnet-4-20250514",
    "Gemini 2.5 Pro": "gemini/gemini-2.5-pro",
}
```

Then add the corresponding API key to your `.env`:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## Observability with Langfuse

All LLM calls are traced via [Langfuse](https://langfuse.com/). You can view the full decision-making trace for every turn: the battle state sent to the model, the model's tool call response, and any fallback actions.

**Live dashboard (free tier):** [Langfuse Cloud Dashboard](https://cloud.langfuse.com/project/cmoc2kqe300z6ad08cgab046t/traces?dateRange=30d)

> **Note:** This project uses the Langfuse free (Hobby) tier. Historical trace data older than 30 days is not retained, so the dashboard may appear empty if no recent battles have been run.

To set up your own Langfuse tracing, add your keys to `.env`:

```
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Architecture

```
pokemon-ai-agent/
├── run.py              # Entry point: sets up server/client, launches everything
├── app.py              # Gradio UI: battle controls and configuration
├── agent.py            # LLM-powered agent: formats battle state, queries LLM, parses tool calls
├── battle_runners.py   # Async battle orchestration: agent creation, matchmaking threads
├── tools.py            # Tool definitions (choose_move, choose_switch) sent to the LLM
├── .env.example        # Template for API keys
├── pyproject.toml      # Python dependencies
├── server/             # Pokémon Showdown server (auto-cloned on first run)
└── client/             # Pokémon Showdown web client (auto-cloned on first run)
```

**How a turn works:**
1. `poke-env` receives the battle state from the Showdown server.
2. `agent.py` formats it into a structured prompt (active Pokémon, moves, switches, opponent info, last 20-turns memory).
3. The prompt is sent to the LLM via `litellm.acompletion()` with tool definitions.
4. The LLM responds with a tool call (`choose_move` or `choose_switch`).
5. The agent translates the tool call back into a Showdown protocol command.
6. If the LLM fails or returns an invalid action, a random fallback is used.
