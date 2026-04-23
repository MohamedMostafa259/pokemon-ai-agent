#!/bin/bash

# Write browser-compatible config for the Showdown client.
# play.pokemonshowdown.com/config/config.js is a symlink to ../../config/config.js,
# so writing here is what gets served at /client/config/config.js via nginx.
cat << 'EOF' > /app/client/config/config.js
var Config = Config || {};
Config.server = {
    id: 'localhost',
    host: window.location.hostname,
    port: window.location.port ? parseInt(window.location.port) : (window.location.protocol === 'https:' ? 443 : 80),
    httpport: window.location.port ? parseInt(window.location.port) : (window.location.protocol === 'https:' ? 443 : 80),
    altport: 80
};
EOF
echo "Config write status: $?"

# Redirect testclient.html to load our local config at an absolute path.
sed -i 's|https://play.pokemonshowdown.com/config/config.js|/client/config/config.js|g' /app/client/play.pokemonshowdown.com/testclient.html
echo "Testclient patch status: $?"

echo "Starting Pokemon Showdown Server..."
cd /app/server
node pokemon-showdown start --no-security &

echo "Starting Nginx..."
nginx -c /app/nginx.conf

echo "Starting AI Agent Gradio App..."
cd /app
export GRADIO_SERVER_PORT=7861
export PYTHONUNBUFFERED=1
python app.py
