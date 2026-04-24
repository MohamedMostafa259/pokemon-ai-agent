import gradio as gr
import logging

from battle_runners import (
    AGENT_OPTIONS,
    start_invite_thread,
    start_bot_vs_bot_thread
)
from dotenv import load_dotenv

load_dotenv()

# Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_BATTLE_FORMAT = "gen9randombattle"

PIKACHU_GIF = "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWxlZ2J5d3N2Nm9oanRldTA3aGw4NHFrcW53ZGk1bWdzaWtlaGJwZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/xeuSulJ22SiTaZWBoD/giphy.gif"

def main_app():
    """Creates and returns the Gradio application interface."""
    
    custom_css = """
    /* ===== Global Styles ===== */
    body, .gradio-container {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%) !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
        color: #e0e0e0 !important;
        min-height: 100vh;
    }
    .gradio-container {
        max-width: 960px !important;
        margin: 0 auto !important;
        padding: 2rem 1.5rem !important;
    }

    /* ===== Hero Section ===== */
    .hero-section {
        text-align: center;
        padding: 2.5rem 1rem 1rem 1rem;
    }
    .hero-title {
        font-size: 4em;
        font-weight: 900;
        background: linear-gradient(135deg, #FFCB05 0%, #FFD700 40%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3em;
        line-height: 1.1;
    }
    .hero-subtitle {
        font-size: 1.35em;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .hero-gif {
        margin: 1.2rem auto 0 auto;
        display: block;
        width: 80px;
        filter: drop-shadow(0 0 12px rgba(255, 203, 5, 0.4));
    }

    /* ===== Spectate Button ===== */
    .spectate-wrapper {
        text-align: center;
        margin: 1.5rem 0 1.8rem 0;
    }
    .spectate-btn {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #3B4CCA 0%, #2563eb 100%);
        color: #fff !important;
        padding: 14px 32px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.15em;
        box-shadow: 0 4px 20px rgba(59, 76, 202, 0.4);
        transition: all 0.3s ease;
    }
    .spectate-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(59, 76, 202, 0.6);
    }
    .pulse-dot {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
        50% { box-shadow: 0 0 0 8px rgba(34,197,94,0); }
    }

    /* ===== Tabs & Cards ===== */
    .tab-nav button {
        font-size: 1.1em !important;
        font-weight: 700 !important;
    }
    .gr-group, .gr-panel, .block, .form, .panel {
        background: #1a1a2e !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
    }

    /* ===== Form Controls ===== */
    input[type="text"], textarea, .gr-input, .gr-text-input, .gr-dropdown, select {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    input[type="text"]:focus, textarea:focus {
        border-color: #FFCB05 !important;
        box-shadow: 0 0 0 3px rgba(255,203,5,0.15) !important;
    }

    /* ===== Pokemon Battle Buttons ===== */
    .gr-button.primary, button.primary {
        background: linear-gradient(180deg, #FF3333 0%, #CC0000 100%) !important;
        color: #fff !important;
        font-weight: 800 !important;
        font-size: 1.15em !important;
        border-radius: 12px !important;
        border: 2px solid #990000 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5) !important;
    }
    .gr-button.primary:hover, button.primary:hover {
        background: linear-gradient(180deg, #FF4D4D 0%, #E60000 100%) !important;
        transform: translateY(-2px) !important;
    }

    /* ===== Status Box ===== */
    .status-box textarea {
        background: rgba(0,0,0,0.3) !important;
        color: #a5f3a5 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    .tab-explanation {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95em;
        margin-bottom: 0.8rem;
        font-style: italic;
    }
    """
    
    elite_theme = gr.themes.Base(
        primary_hue="red",
        secondary_hue="amber",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
        text_size=gr.themes.sizes.text_lg
    ).set(
        body_background_fill="#0f0c29",
        body_background_fill_dark="#0f0c29",
        body_text_color="#e0e0e0",
        body_text_color_dark="#e0e0e0",
        body_text_color_subdued="#94a3b8",
        body_text_color_subdued_dark="#94a3b8",
        background_fill_primary="#1a1a2e",
        background_fill_primary_dark="#1a1a2e",
        background_fill_secondary="#16213e",
        background_fill_secondary_dark="#16213e",
        block_background_fill="#1a1a2e",
        block_background_fill_dark="#1a1a2e",
        block_border_color="rgba(255,255,255,0.08)",
        block_border_color_dark="rgba(255,255,255,0.08)",
        block_label_text_color="#cbd5e1",
        block_label_text_color_dark="#cbd5e1",
        block_title_text_color="#e0e0e0",
        block_title_text_color_dark="#e0e0e0",
        input_background_fill="#12122a",
        input_background_fill_dark="#12122a",
        input_border_color="rgba(255,255,255,0.12)",
        input_border_color_dark="rgba(255,255,255,0.12)",
        input_border_color_focus="#FFCB05",
        input_border_color_focus_dark="#FFCB05",
        input_placeholder_color="#64748b",
        input_placeholder_color_dark="#64748b",
        border_color_primary="rgba(255,255,255,0.08)",
        border_color_primary_dark="rgba(255,255,255,0.08)",
        panel_background_fill="#16213e",
        panel_background_fill_dark="#16213e",
        panel_border_color="rgba(255,255,255,0.06)",
        panel_border_color_dark="rgba(255,255,255,0.06)",
        button_primary_background_fill="#CC0000",
        button_primary_background_fill_dark="#CC0000",
        button_primary_background_fill_hover="#FF1A1A",
        button_primary_background_fill_hover_dark="#FF1A1A",
        button_primary_text_color="#ffffff",
        button_primary_text_color_dark="#ffffff",
        shadow_drop="none",
        shadow_drop_lg="none",
    )
    
    with gr.Blocks(title="Pokémon AI Agents") as demo:

        # --- Hero Section ---
        gr.HTML(
            f"""
            <div class="hero-section">
                <div class="hero-title">Pokémon AI Agents</div>
                <div class="hero-subtitle">
                    Watch Large Language Models battle each other in Pokémon Showdown or challenge them yourself.
                </div>
                <img src="{PIKACHU_GIF}" class="hero-gif" alt="Pikachu" />
            </div>
            """
        )

        # --- Spectate Button ---
        gr.HTML(
            """
            <div class="spectate-wrapper">
                <a href="http://localhost:8000" target="_blank" class="spectate-btn">
                    <span class="pulse-dot"></span>
                    Spectate Matches (Live Showdown Client)
                </a>
            </div>
            """
        )

        # --- Battle Controls ---
        with gr.Row():
            with gr.Column(scale=1, min_width=500):
                
                with gr.Tab("Human vs. AI") as tab_player:
                    gr.HTML('<div class="tab-explanation">You play against an AI agent. Log in to Showdown, then the bot challenges you.</div>')
                    with gr.Group():
                        agent_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="AI Agent (LLM)", value="Cerebras Llama 3.1 8B")
                        opp_user = gr.Textbox(label="Your Showdown Username", placeholder="The username you logged in with on the Showdown client")
                        bot_user = gr.Textbox(label="Bot Username", placeholder="Any unique name for the AI bot (e.g., pikabot99)")
                        challenge_btn = gr.Button("Send Challenge", variant="primary")
                    status_out = gr.Textbox(label="Status", interactive=False, lines=2, elem_classes=["status-box"])
                    challenge_btn.click(fn=lambda a, o, b: start_invite_thread(a, o, b), inputs=[agent_drop, opp_user, bot_user], outputs=status_out)
                    
                with gr.Tab("AI vs. AI") as tab_arena:
                    gr.HTML('<div class="tab-explanation">Two AI agents battle each other autonomously. Just pick models and watch.</div>')
                    with gr.Group():
                        with gr.Row():
                            with gr.Column():
                                a1_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="Model 1", value="Cerebras Llama 3.1 8B")
                                b1_user = gr.Textbox(label="Bot 1 Username", placeholder="e.g., bot_llama")
                            with gr.Column():
                                a2_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="Model 2", value="Mistral Codestral 2508")
                                b2_user = gr.Textbox(label="Bot 2 Username", placeholder="e.g., bot_gemma")
                        arena_btn = gr.Button("Start AI vs. AI Battle", variant="primary")
                    arena_status = gr.Textbox(label="Status", interactive=False, lines=2, elem_classes=["status-box"])
                    arena_btn.click(fn=lambda a1, b1, a2, b2: start_bot_vs_bot_thread(a1, b1, a2, b2), inputs=[a1_drop, b1_user, a2_drop, b2_user], outputs=arena_status)

    return demo, custom_css, elite_theme
