# Pokémon AI Agent

AI-powered Pokémon battle agents using LLMs (via LiteLLM) on a local Pokémon Showdown server.

## Quick Start (Docker)

```bash
docker build -t pokemon-agent .
docker run -p 7860:7860 -p 8000:8000 pokemon-agent
```

Then open:
- **Gradio UI**: http://localhost:7860
- **Showdown Client**: http://localhost:8000

## How It Works

1. A local Pokémon Showdown server runs inside the Docker container
2. The Gradio web UI lets you configure and start AI battles
3. LLM agents (via LiteLLM) connect to the local server and play autonomously
4. Watch battles live in the Showdown client

## Supported Models

Uses free LLM APIs via LiteLLM — supports OpenRouter, Cerebras, Google AI Studio, Groq, and Mistral models.

Set your API keys as environment variables:
```bash
docker run -p 7860:7860 -p 8000:8000 \
  -e OPENROUTER_API_KEY=your_key \
  -e CEREBRAS_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  pokemon-agent
```
