FROM python:3.11-slim

# Install system dependencies, Nginx, and Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nginx \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python dependencies and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and configuration
COPY . /app

# Set up Nginx configuration
RUN cp nginx.conf /etc/nginx/nginx.conf

# Install dependencies for Showdown Server
WORKDIR /app
RUN if [ ! -d "server/config" ]; then git clone https://github.com/smogon/pokemon-showdown.git server; fi
WORKDIR /app/server
RUN npm install
RUN cp config/config-example.js config/config.js

# Install and BUILD Showdown Client (must compile to generate js/battle.js etc.)
WORKDIR /app
RUN if [ ! -d "client/config" ]; then git clone https://github.com/smogon/pokemon-showdown-client.git client; fi
WORKDIR /app/client
RUN npm install || true
RUN cp config/config-example.js config/config.js
RUN node build

# Set permissions
WORKDIR /app
RUN chmod -R 755 /app
RUN chmod +x start.sh

# Expose the single port Hugging Face Spaces uses
EXPOSE 7860

# Start all services
ENTRYPOINT ["./start.sh"]
