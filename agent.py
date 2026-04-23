import json_repair
import litellm

# Import necessary poke-env components for type hinting and functionality
import poke_env
from tools import toolsList

class PokemonAgent(poke_env.player.Player):
    """
    An AI agent for Pokemon Showdown that uses LiteLLM
    to support OpenAI, Anthropic, Gemini, Mistral, and more.
    """
    def __init__(self, model_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # litellm will automatically pick up API keys from the environment variables
        # (e.g., OPENROUTER_API_KEY, CEREBRAS_API_KEY, GROQ_API_KEY, MISTRAL_API_KEY, GEMINI_API_KEY)
        self.model = model_name
        self.functions = toolsList
        
        # Short-term memory
        self.history = []

    def _format_battle_state(self, battle: poke_env.battle.Battle) -> str:
        """Formats the current battle state into a string for the LLM."""
        # Own active Pokemon details
        active_pkmn = battle.active_pokemon
        active_pkmn_info = f"Your active Pokemon: {active_pkmn.species} " \
                           f"(Type: {'/'.join(map(str, active_pkmn.types))}) " \
                           f"HP: {active_pkmn.current_hp_fraction * 100:.1f}% " \
                           f"Status: {active_pkmn.status.name if active_pkmn.status else 'None'} " \
                           f"Boosts: {active_pkmn.boosts}"

        # Opponent active Pokemon details
        opponent_pkmn = battle.opponent_active_pokemon
        opponent_pkmn_info = f"Opponent's active Pokemon: {opponent_pkmn.species} " \
                             f"(Type: {'/'.join(map(str, opponent_pkmn.types))}) " \
                             f"HP: {opponent_pkmn.current_hp_fraction * 100:.1f}% " \
                             f"Status: {opponent_pkmn.status.name if opponent_pkmn.status else 'None'} " \
                             f"Boosts: {opponent_pkmn.boosts}"

        # Available moves
        available_moves_info = "Available moves:\n"
        if battle.available_moves:
            for move in battle.available_moves:
                available_moves_info += f"- {move.id} (Type: {move.type}, BP: {move.base_power}, Acc: {move.accuracy}, PP: {move.current_pp}/{move.max_pp}, Cat: {move.category.name})\n"
        else:
             available_moves_info += "- None (Must switch or Struggle)\n"

        # Available switches
        available_switches_info = "Available switches:\n"
        if battle.available_switches:
            for pkmn in battle.available_switches:
                 available_switches_info += f"- {pkmn.species} (HP: {pkmn.current_hp_fraction * 100:.1f}%, Status: {pkmn.status.name if pkmn.status else 'None'})\n"
        else:
            available_switches_info += "- None\n"

        # Combine information
        state_str = f"{active_pkmn_info}\n" \
                    f"{opponent_pkmn_info}\n\n" \
                    f"{available_moves_info}\n" \
                    f"{available_switches_info}\n" \
                    f"Weather: {battle.weather}\n" \
                    f"Terrains: {battle.fields}\n" \
                    f"Your Side Conditions: {battle.side_conditions}\n" \
                    f"Opponent Side Conditions: {battle.opponent_side_conditions}\n\n"
        
        # PERMANENT REVEALED KNOWLEDGE LEDGER
        revealed_knowledge = "Opponent's Revealed Team & Moves:\n"
        if battle.opponent_team:
            for pkmn_name, pkmn in battle.opponent_team.items():
                types = '/'.join(map(str, pkmn.types))
                moves = ', '.join([move for move in pkmn.moves.keys()]) if pkmn.moves else 'None revealed'
                item = pkmn.item if pkmn.item else 'Unknown'
                ability = pkmn.ability if pkmn.ability else 'Unknown'
                revealed_knowledge += f"- {pkmn.species} (Type: {types}): Moves: [{moves}], Item: {item}, Ability: {ability}\n"
        else:
             revealed_knowledge += "- Unknown\n"
        
        state_str += f"{revealed_knowledge}\n"

        # FLOW: 8-TURN MEMORY
        if self.history:
            history_str = "Your recent actions (Flow):\n"
            for i, action in enumerate(self.history):
                history_str += f"Turn -{len(self.history) - i}: {action}\n"
            state_str += f"{history_str}\n"

        return state_str.strip()

    async def _get_llm_decision(self, battle_state: str) -> dict | None:
        """Sends state to LiteLLM router and gets back the function call decision."""
        system_prompt = (
            "You are an elite Pokemon battle AI. Your goal is to win the battle. "
            "Based on the current battle state, decide the best action by choosing an available move or switch. "
            "Consider type matchups, HP, status conditions, field effects, entry hazards, and opponent actions."
        )
        user_prompt = f"Current Battle State:\n{battle_state}\n\nChoose the best action."

        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                tools=[{"type": "function", "function": f} for f in self.functions],
            )
            message = response.choices[0].message
            if getattr(message, 'tool_calls', None):
                function_call = message.tool_calls[0].function
                return {"name": function_call.name, "arguments": json_repair.loads(function_call.arguments)}
            else:
                print(f"Warning: No tool call returned. Response: {message.content}")
                return None
        except Exception as e:
            print(f"Error during LiteLLM API call: {e}")
            return None

    def _find_move_by_name(self, battle: poke_env.battle.Battle, move_name: str) -> poke_env.battle.Move | None:
        """Finds the Move object corresponding to the given name."""
        # Normalize name for comparison (lowercase, remove spaces/hyphens)
        normalized_name = move_name.lower().replace(" ", "").replace("-", "")
        for move in battle.available_moves:
            if move.id == normalized_name: # move.id is already normalized
                return move
        # Fallback: try matching against the display name if ID fails (less reliable)
        for move in battle.available_moves:
             if move.id == move_name.lower(): # Handle cases like "U-turn" vs "uturn"
                 return move
             if move.name.lower() == move_name.lower():
                return move
        return None

    def _find_pokemon_by_name(self, battle: poke_env.battle.Battle, pokemon_name: str) -> poke_env.battle.Pokemon | None:
        """Finds the Pokemon object corresponding to the given species name."""
        # Normalize name for comparison
        normalized_name = pokemon_name.lower()
        for pkmn in battle.available_switches:
            if pkmn.species.lower() == normalized_name:
                return pkmn
        return None

    async def choose_move(self, battle: poke_env.battle.Battle) -> str:
        """
        Main decision-making function called by poke-env each turn.
        """
        # 1. Format battle state
        battle_state_str = self._format_battle_state(battle)
        # print(f"\n--- Turn {battle.turn} ---") # Debugging
        # print(battle_state_str) # Debugging

        # 2. Get decision from LLM
        decision = await self._get_llm_decision(battle_state_str)

        # 3. Parse decision and create order
        if decision:
            function_name = decision["name"]
            args = decision["arguments"]
            # print(f"OpenAI Recommended: {function_name} with args {args}") # Debugging

            if function_name == "choose_move":
                move_name = args.get("move_name")
                if move_name:
                    chosen_move = self._find_move_by_name(battle, move_name)
                    if chosen_move:
                        # Add to short-term memory
                        self.history.append(f"Used move: {chosen_move.id}")
                        if len(self.history) > 8:
                            self.history.pop(0)
                            
                        # print(f"Action: Using move {chosen_move.id}")
                        return self.create_order(chosen_move)
                    else:
                        print(f"Warning: LLM chose unavailable/invalid move '{move_name}'. Falling back.")
                else:
                    print("Warning: LLM 'choose_move' called without 'move_name'. Falling back.")

            elif function_name == "choose_switch":
                pokemon_name = args.get("pokemon_name")
                if pokemon_name:
                    chosen_switch = self._find_pokemon_by_name(battle, pokemon_name)
                    if chosen_switch:                        
                        # Add to short-term memory
                        self.history.append(f"Switched to: {chosen_switch.species}")
                        if len(self.history) > 8:
                            self.history.pop(0)
                        
                        # print(f"Action: Switching to {chosen_switch.species}")
                        return self.create_order(chosen_switch)
                    else:
                        print(f"Warning: LLM chose unavailable/invalid switch '{pokemon_name}'. Falling back.")
                else:
                    print("Warning: LLM 'choose_switch' called without 'pokemon_name'. Falling back.")

        # 4. Fallback if API fails, returns invalid action, or no function call
        print("Fallback: Choosing random move/switch.")
        # Ensure options exist before choosing randomly
        available_options = battle.available_moves + battle.available_switches
        if available_options:
             # Use the built-in random choice method from Player for fallback
             return self.choose_random_move(battle)
        else:
             # Should only happen if forced to Struggle
             return self.choose_default_move(battle)