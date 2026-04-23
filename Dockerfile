FROM python:3.11-slim

# Install system dependencies and Node.js
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python dependencies and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app

# Clone and install Pokemon Showdown server
RUN git clone https://github.com/smogon/pokemon-showdown.git server \
    && cd server \
    && npm install \
    && cp config/config-example.js config/config.js

# Clone, install, and build Pokemon Showdown client
RUN git clone https://github.com/smogon/pokemon-showdown-client.git client \
    && cd client \
    && npm install || true \
    && cp config/config-example.js config/config.js \
    && node build

RUN chmod +x start.sh

# Showdown server on 8000, Gradio on 7860
EXPOSE 7860 8000

ENTRYPOINT ["./start.sh"]
