import gradio as gr
import logging

from battle_runners import (
    AGENT_OPTIONS,
    start_invite_thread,
    start_bot_vs_bot_thread,
    start_ladder_thread
)

# Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

# Constants
DEFAULT_BATTLE_FORMAT = "gen9randombattle"

def main_app():
    """Creates and returns the Gradio application interface."""
    
    custom_css = """
    .gradio-container {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .tab-nav {
        flex-wrap: wrap !important;
        white-space: nowrap !important;
    }
    .header-text {
        text-align: center;
        margin-bottom: 20px;
    }
    .header-title {
        font-weight: 800;
        font-size: 2.5em;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .header-subtitle {
        font-size: 1.1em;
        color: #64748b;
    }
    """
    
    elite_theme = gr.themes.Base(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"]
    )
    
    with gr.Blocks(title="Pokémon AI Agents") as demo:
        
        gr.HTML(
            """
            <div class="header-text">
                <div class="header-title">Pokémon AI Agents</div>
                <div class="header-subtitle">A web interface to run, test, and spectate Large Language Models playing Pokémon Showdown.</div>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=1, min_width=450):
                
                with gr.Tab("Player Match") as tab_player:
                    with gr.Group():
                        gr.Markdown("Challenge an AI agent to a battle on Showdown.\n\n⚠️ *Requires a registered Showdown bot account.*")
                        agent_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="AI Agent", value="Cerebras Llama 3.1 8B")
                        opp_user = gr.Textbox(label="Your Showdown Username", placeholder="e.g., player123")
                        bot_user = gr.Textbox(label="Bot Username", placeholder="Registered Bot Username")
                        bot_pass = gr.Textbox(label="Bot Password", type="password", info="Leave blank for Localhost")
                        challenge_btn = gr.Button("Send Challenge", variant="primary")
                    status_out = gr.Textbox(label="Status", interactive=False, lines=2)
                    challenge_btn.click(fn=start_invite_thread, inputs=[agent_drop, opp_user, bot_user, bot_pass], outputs=status_out)
                    
                with gr.Tab("AI vs AI") as tab_arena:
                    with gr.Group():
                        gr.Markdown("Watch two different LLMs battle each other on Showdown.\n\n⚠️ *Requires two registered accounts.*")
                        with gr.Row():
                            with gr.Column():
                                a1_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="Model 1", value="Cerebras Llama 3.1 8B")
                                b1_user = gr.Textbox(label="Bot 1 Username", placeholder="Bot 1 Username")
                                b1_pass = gr.Textbox(label="Bot 1 Password", type="password")
                            with gr.Column():
                                a2_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="Model 2", value="Google Gemma 4 31B")
                                b2_user = gr.Textbox(label="Bot 2 Username", placeholder="Bot 2 Username")
                                b2_pass = gr.Textbox(label="Bot 2 Password", type="password", info="Optional locally")
                        arena_btn = gr.Button("Start AI vs AI Battle", variant="primary")
                    arena_status = gr.Textbox(label="Status", interactive=False, lines=2)
                    arena_btn.click(fn=start_bot_vs_bot_thread, inputs=[a1_drop, b1_user, b1_pass, a2_drop, b2_user, b2_pass], outputs=arena_status)

                with gr.Tab("Auto-Ladder") as tab_ladder:
                    with gr.Group():
                        gr.Markdown("Allow an AI agent to play ranked matches on your Showdown account.\n\n⚠️ *Wait for login before switching tabs!*")
                        ladder_drop = gr.Dropdown(choices=AGENT_OPTIONS, label="AI Agent", value="Cerebras Llama 3.1 8B")
                        lad_user = gr.Textbox(label="Showdown Username", placeholder="Your Registered Username")
                        lad_pass = gr.Textbox(label="Showdown Password", type="password", info="Optional locally")
                        ladder_btn = gr.Button("Start Auto-Laddering", variant="primary")
                    ladder_status = gr.Textbox(label="Status", interactive=False, lines=2)
                    ladder_btn.click(fn=start_ladder_thread, inputs=[ladder_drop, lad_user, lad_pass], outputs=ladder_status)

            with gr.Column(scale=2, min_width=600):
                gr.Markdown("### 📺 Live Showdown Client")
                gr.HTML(
                    """
                    <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 60px 40px; text-align: center; background-color: #f8fafc; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 500px;">
                        <h2 style="margin-bottom: 10px; color: #0f172a; font-family: Inter, sans-serif; font-weight: 700; font-size: 1.8em;">Battles run on the local server.</h2>
                        <p style="margin-bottom: 30px; font-size: 1.1em; color: #475569; max-width: 500px; line-height: 1.6;">
                            Your Docker space is hosting a local Pokemon Showdown server and client.<br><br>
                            Click below to open the client in a new tab. Once your AI matches start, you can find them in your active battles or by searching for your bot's username!
                        </p>
                        <a href="/client/" target="_blank" style="background-color: #3b82f6; color: white; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1em; box-shadow: 0 2px 4px rgb(59 130 246 / 0.4);">
                            🟢 Open Local Pokémon Showdown (New Tab)
                        </a>
                    </div>
                    """
                )

    return demo

if __name__ == "__main__":
    app = main_app()
    app.launch(server_name="0.0.0.0", server_port=7861)
