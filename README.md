<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png" alt="Pokemon Logo" width="200"/>
  
  # 🤖 Pokémon AI Agents 🌟
  
  *“I want to be the very best, like no one ever was... but with Large Language Models!”* 🎶
  
  [![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-yellow.svg)](https://huggingface.co/spaces/mohamedmostafa259/pokemon-ai-agent)
  [![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
  [![LiteLLM](https://img.shields.io/badge/LiteLLM-Integrated-green.svg)](https://litellm.ai/)
</div>

---

Welcome to the **Pokémon AI Agent**! This repository transforms state-of-the-art LLMs (like Llama 3, Gemma, and Qwen) into elite Pokémon Trainers. By seamlessly integrating **Gradio**, **Poke-env**, and **LiteLLM**, this project runs a completely self-hosted, local **Pokémon Showdown Server & Client** inside Docker, allowing AI models to battle autonomously.

## 📸 Sneak Peek

### The Arena (Gradio Interface & Showdown Client)
*(Insert a GIF or Screenshot of your UI and Battles here!)*
> **Live Demo:** [Play on Hugging Face Spaces](https://huggingface.co/spaces/mohamedmostafa259/pokemon-ai-agent)

---

## ⚡ Features

- **🧠 Elite AI Trainers**: Connects to the best open-source and proprietary models (via OpenRouter, Groq, Cerebras, Mistral, and Google AI Studio).
- **🏟️ Autonomous Local Server**: Zero dependency on the public Pokémon Showdown servers. Your Docker container hosts its own private Showdown server and web client.
- **⚔️ Multiple Battle Modes**:
  - **Player vs AI**: Test your skills against the machine.
  - **AI vs AI (Arena Mode)**: Spectate epic clashes between different LLMs.
  - **Auto-Ladder**: Let the AI endlessly grind and rank up.
- **🔌 Seamless API Integration**: Automatically loads `.env` files and parses configurations dynamically.

---

## 🚀 How to Run

### Option A: Local Machine (Elite Developer Mode)

Running locally gives you the ultimate, unrestricted experience. No proxies, lightning-fast rebuilds!

1. **Clone & Configure**
   ```bash
   git clone https://github.com/MohamedMostafa259/pokemon-ai-agent.git
   cd pokemon-ai-agent
   
   # Copy the example environment file and add your API keys
   cp .env.example .env
   ```
   *Edit `.env` and paste your API keys (e.g., `OPENROUTER_API_KEY`, `GEMINI_API_KEY`).*

2. **Deploy with Docker**
   ```bash
   docker build -t pokemon-agent .
   docker run -p 7860:7860 -p 8000:8000 pokemon-agent
   ```

3. **Enter the Arena**
   - **Control Panel (Gradio):** Open `http://localhost:7860` to configure and dispatch your agents.
   - **Live Spectator Client:** Open `http://localhost:8000` to watch the battles unfold in real-time.

---

### Option B: Hugging Face Spaces (Cloud Mode)

Want to share your AI Gym Leader with the world?

1. **Create a Space**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new **Docker** Space.
2. **Add Secrets**
   - In your Space settings, go to **Variables and secrets**.
   - Add your keys as New Secrets (e.g., `OPENROUTER_API_KEY`, `CEREBRAS_API_KEY`).
3. **Push to HF**
   ```bash
   git remote add hf https://huggingface.co/spaces/mohamedmostafa259/pokemon-ai-agent
   git push hf main
   ```
4. **Play!**
   - Hugging Face automatically exposes port `7860`. You can control the AI and view the internal Showdown server through the Hugging Face URL provided.

---

## 🛠️ Architecture Deep Dive

- `agent.py`: The brain. Formats the complex Showdown battle state (HP, weather, revealed moves, short-term memory) into a clean prompt, queries the LLM via LiteLLM, and translates function calls back into Pokémon Showdown actions.
- `battle_runners.py`: Async battle orchestration using `poke-env`. Manages threads for matchmaking and automated laddering.
- `app.py`: A beautiful, responsive Gradio dashboard to control the AI.
- `Dockerfile` & `start.sh`: Builds a unified container hosting the Showdown Server (`node`), Showdown Client (`node build`), and the AI Agent (`python`).

---

*“There’s no sense in going out of your way to get somebody to like you.”* – Ash Ketchum... but we hope you star ⭐ this repo anyway!
