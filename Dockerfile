# Multi-stage Docker build for AI Product Advisor with Ollama
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    OLLAMA_HOST=0.0.0.0:11434

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the notebook and any other files
COPY product-advisor.ipynb /app/notebook.ipynb

# Create directory for Ollama models
RUN mkdir -p /root/.ollama

# Expose ports
# 8888: Jupyter Notebook
# 11434: Ollama API
EXPOSE 8888 11434

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Ollama server in background\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "Waiting for Ollama to start..."\n\
sleep 5\n\
\n\
# Pull the model (gpt-oss:20b) in background\n\
echo "Pulling gpt-oss:20b model (this may take a while on first run)..."\n\
ollama pull gpt-oss:20b &\n\
\n\
# Start Jupyter Notebook\n\
echo "Starting Jupyter Notebook..."\n\
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/bin/bash", "/app/start.sh"]

