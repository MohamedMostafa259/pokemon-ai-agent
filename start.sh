#!/bin/bash

echo "===== Pokemon AI Agent Startup ====="

# Start the Pokemon Showdown server in the background
echo "Starting Pokemon Showdown Server..."
cd /app/server
node pokemon-showdown start --no-security &

# Wait for the Showdown server to be ready
echo "Waiting for Showdown server..."
sleep 3

# Start the Gradio app (foreground, keeps container alive)
echo "Starting Gradio App on port 7860..."
cd /app
export PYTHONUNBUFFERED=1
python app.py
