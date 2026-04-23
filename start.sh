#!/bin/bash

# Update client config to use relative path/hostname for websocket
echo "Configuring Pokemon Showdown Client..."
cat << 'EOF' > /app/client/config/config.js
exports.server = {
    id: 'localhost',
    host: window.location.hostname,
    port: window.location.port ? window.location.port : (window.location.protocol === 'https:' ? 443 : 80),
    httpport: window.location.port ? window.location.port : (window.location.protocol === 'https:' ? 443 : 80),
    altport: 80,
    routes: {
        client: '/client/'
    }
};
EOF

echo "Starting Pokemon Showdown Server..."
cd /app/server
node pokemon-showdown start --no-security &

echo "Starting Nginx..."
nginx -c /app/nginx.conf

echo "Starting AI Agent Gradio App..."
cd /app
python app.py
