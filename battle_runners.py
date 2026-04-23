import asyncio
import traceback
import logging
import threading

from poke_env.player import Player, RandomPlayer
from poke_env import AccountConfiguration, LocalhostServerConfiguration
from agent import PokemonAgent

# Constants
DEFAULT_BATTLE_FORMAT = "gen9randombattle"

# Free Models Mapping. src: https://github.com/cheahjs/free-llm-api-resources
MODEL_MAP = {
    # OpenRouter
    "OpenRouter GLM 4.5 Air": "openrouter/z-ai/glm-4.5-air:free",
    "OpenRouter Qwen3 Next 80B": "openrouter/qwen/qwen3-next-80b-a3b-instruct:free",
    "OpenRouter Llama 3.3 70B": "openrouter/meta-llama/llama-3.3-70b-instruct:free",
    "OpenRouter MiniMax m2.5": "openrouter/minimax/minimax-m2.5:free",
    "OpenRouter Gemma 4 31B": "openrouter/google/gemma-4-31b-it:free",
    "OpenRouter Gemma 3 27B": "openrouter/google/gemma-3-27b-it:free",
    "OpenRouter Dolphin Mistral 24B": "openrouter/cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
    "OpenRouter Nemotron 3 120B": "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
    "OpenRouter GPT OSS 120B": "openrouter/openai/gpt-oss-120b:free",
    "OpenRouter Hermes 3 Llama 3.1 405B": "openrouter/nousresearch/hermes-3-llama-3.1-405b:free",
    
    # Cerebras
    "Cerebras GPT OSS 120B": "cerebras/gpt-oss-120b",
    "Cerebras Llama 3.1 8B": "cerebras/llama3.1-8b",

    # Google AI Studio
    "Google Gemma 4 31B": "gemini/gemma-4-31b-it",
    "Google Gemma 3 27B": "gemini/gemma-3-27b-it",
    "Google Gemini 3.1 Flash-Lite": "gemini/gemini-3.1-flash-lite-preview",

    # Groq
    "Groq Qwen3 32B": "groq/qwen/qwen3-32b",

    # Mistral
    "Mistral Codestral 2508": "mistral/codestral-2508"
}
AGENT_OPTIONS = ["Random Player"] + list(MODEL_MAP.keys())

async def create_agent_async(agent_type: str, username: str, password: str | None = None, 
                             battle_format: str = DEFAULT_BATTLE_FORMAT) -> Player | str:
    logging.info(f"Attempting to create {agent_type} as {username}")
    
    server_configuration = LocalhostServerConfiguration
    # Nullify password since we run on localhost/docker
    password = None
    
    account_config = AccountConfiguration(username, password)
    try:
        if agent_type == "Random Player":
            player = RandomPlayer(
                account_configuration=account_config,
                server_configuration=server_configuration,
                battle_format=battle_format,
                start_listening=True,
            )
        elif agent_type in MODEL_MAP:
            player = PokemonAgent(
                model_name=MODEL_MAP[agent_type],
                account_configuration=account_config,
                server_configuration=server_configuration,
                battle_format=battle_format,
                start_listening=True,
            )
        else:
            return f"Error: Invalid agent type '{agent_type}' requested."

        logging.info(f"Agent ({username}) created on Local server.")
        return player

    except Exception as e:
        error_message = f"Error creating agent {username}: {e}"
        logging.error(traceback.format_exc())
        return error_message

async def send_battle_invite_async(player: Player, opponent_username: str, battle_format: str) -> str:
    try:
        await player.send_challenges(opponent_username, n_challenges=1)
        return f"Invitation sent to {opponent_username}!"
    except Exception as e:
        logging.error(traceback.format_exc())
        raise e

# Background Threads

def start_invite_thread(agent_choice: str, opp_username: str, bot_username: str, bot_password: str) -> str:
    if not opp_username.strip(): return "⚠️ Please enter the Opponent's Username."
    if not bot_username.strip(): return "⚠️ Please enter the Bot's Username."

    def _bg_task():
        async def _run():
            agent_or_error = await create_agent_async(agent_choice, bot_username, bot_password)
            if isinstance(agent_or_error, str): return
            try:
                await send_battle_invite_async(agent_or_error, opp_username.strip(), DEFAULT_BATTLE_FORMAT)
            except Exception: pass
            # Keep loop alive for the battle
            while list(agent_or_error.battles.values()) or list(agent_or_error._challenges.values()):
                await asyncio.sleep(1)
        asyncio.run(_run())

    threading.Thread(target=_bg_task, daemon=True).start()
    return f"✅ '{bot_username}' is attempting to challenge '{opp_username}'. Keep your client open!"

def start_bot_vs_bot_thread(agent1_choice: str, bot1_username: str, bot1_password: str, 
                            agent2_choice: str, bot2_username: str, bot2_password: str) -> str:
    if not bot1_username.strip() or not bot2_username.strip(): return "⚠️ Both Bots need a Username."

    def _bg_task():
        async def _run():
            agent1 = await create_agent_async(agent1_choice, bot1_username, bot1_password)
            agent2 = await create_agent_async(agent2_choice, bot2_username, bot2_password)
            if isinstance(agent1, str) or isinstance(agent2, str): return
            await agent1.battle_against(agent2, n_battles=1)
            logging.info("Arena match finished.")
        asyncio.run(_run())

    threading.Thread(target=_bg_task, daemon=True).start()
    return f"🚀 Arena Match started between {bot1_username} and {bot2_username}!"

def start_ladder_thread(agent_choice: str, bot_username: str, bot_password: str) -> str:
    if not bot_username.strip():
         return "⚠️ Bot requires a Username!"

    def _bg_task():
        async def _run():
            try:
                player = await create_agent_async(agent_choice, bot_username, bot_password)
                if isinstance(player, str): return
                logging.info(f"Connecting to ladder as {bot_username}...")
                await player.ladder(1)
            except Exception as e:
                logging.error(f"Error laddering: {e}")
        asyncio.run(_run())
        
    threading.Thread(target=_bg_task, daemon=True).start()
    return f"🚀 {bot_username} is now queuing up on the API ladder!"
