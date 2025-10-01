# 🚀 Complete Deployment Guide

## 📋 Two Deployment Options

I've created **TWO** complete Docker deployments for your AI Product Advisor:

### 🎯 Option 1: Jupyter Notebook (Original)
**Best for:** Development, exploration, data analysis
- Full Jupyter notebook interface
- Cell-by-cell execution
- Great for testing and experimentation

### 🌐 Option 2: Streamlit Web App (Recommended for Production)
**Best for:** End users, demos, production deployment
- Beautiful modern UI
- No coding knowledge required
- Easy to share with others

---

## 🚀 Quick Start - Choose Your Option

### Option 1: Jupyter Notebook

```bash
# Navigate to project directory
cd "C:\Users\U\Desktop\my projects\OLLAMA PROJECT"

# Build and start (one command)
build.bat

# Or manually:
docker-compose up -d

# Access at: http://localhost:8888
```

### Option 2: Streamlit Web App (Recommended ⭐)

```bash
# Navigate to project directory
cd "C:\Users\U\Desktop\my projects\OLLAMA PROJECT"

# Build and start (one command)
start-webapp.bat

# Or manually:
docker-compose -f docker-compose.webapp.yml up -d

# Access at: http://localhost:8501
```

---

## 📦 What Gets Installed

### Common Components (Both Options)
- ✅ Python 3.11
- ✅ Ollama server
- ✅ gpt-oss:20b model (~13GB)
- ✅ All required Python packages

### Additional Components
- **Jupyter**: Notebook interface, development tools
- **Streamlit**: Modern web UI, production-ready interface

---

## 🎯 Step-by-Step: Streamlit Web App (Recommended)

### Prerequisites
1. **Install Docker Desktop**
   - Download from: https://www.docker.com/products/docker-desktop
   - Ensure it's running (check system tray)

2. **System Requirements**
   - RAM: 16GB minimum
   - Disk: 20GB free space
   - CPU: 4+ cores recommended

### Installation Steps

#### 1️⃣ **Navigate to Project**
```bash
cd "C:\Users\U\Desktop\my projects\OLLAMA PROJECT"
```

#### 2️⃣ **Run the Startup Script**
```bash
start-webapp.bat
```

This script will:
- ✅ Start Ollama server
- ✅ Download the AI model (first time only)
- ✅ Build the web app
- ✅ Launch everything
- ✅ Open your browser automatically

#### 3️⃣ **Wait for Model Download**
First run takes 10-30 minutes to download the model.

**Check progress:**
```bash
docker-compose -f docker-compose.webapp.yml logs -f
```

#### 4️⃣ **Access the Web App**
Once ready, open: **http://localhost:8501**

---

## 💻 Using the Web App

### First-Time Setup
1. Open sidebar (click arrow if closed)
2. Select model: `gpt-oss:20b`
3. Click "🔄 Initialize Advisor"
4. Wait for confirmation

### Research Products
1. Go to "🔍 Product Research" tab
2. Enter product category (e.g., "wireless headphones")
3. Optional: Add budget and requirements
4. Click "🚀 Generate Product Guide"
5. Wait 30-60 seconds for results

### Compare Products
1. Go to "⚔️ Product Comparison" tab
2. Enter two products to compare
3. Click "⚔️ Compare Products"
4. Get detailed head-to-head analysis

---

## 🔧 Management Commands

### View Logs
```bash
# All services
docker-compose -f docker-compose.webapp.yml logs -f

# Just web app
docker logs -f product-advisor-webapp

# Just Ollama
docker logs -f ollama-server
```

### Check Status
```bash
docker-compose -f docker-compose.webapp.yml ps
```

### Restart Services
```bash
# Restart everything
docker-compose -f docker-compose.webapp.yml restart

# Restart just web app
docker restart product-advisor-webapp

# Restart just Ollama
docker restart ollama-server
```

### Stop Services
```bash
# Stop but keep data
docker-compose -f docker-compose.webapp.yml down

# Stop and remove all data (including models)
docker-compose -f docker-compose.webapp.yml down -v
```

### Update to Latest
```bash
# Pull latest images
docker-compose -f docker-compose.webapp.yml pull

# Rebuild
docker-compose -f docker-compose.webapp.yml up -d --build
```

---

## 🐛 Troubleshooting

### Problem: "Port already in use"

**Error:** `Bind for 0.0.0.0:8501 failed: port is already allocated`

**Solution:**
```bash
# Find what's using the port
netstat -ano | findstr :8501

# Stop the container using it
docker stop <container_id>

# Or change port in docker-compose.webapp.yml
ports:
  - "8502:8501"  # Use different port
```

### Problem: "Out of Memory"

**Error:** Container crashes or system becomes slow

**Solution:**
1. Close other applications
2. Increase Docker memory:
   - Docker Desktop → Settings → Resources → Memory
   - Set to at least 12GB
3. Use smaller model:
   ```bash
   docker exec ollama-server ollama pull llama3:latest
   ```
   Then select `llama3:latest` in web app

### Problem: "Model download is slow"

**Normal:** First download takes 10-30 minutes

**Check progress:**
```bash
docker exec ollama-server ollama list
```

**If stuck:**
```bash
# Restart Ollama
docker restart ollama-server

# Retry download
docker exec ollama-server ollama pull gpt-oss:20b
```

### Problem: "Connection refused"

**Error:** `Error: Connection refused on http://localhost:11434`

**Solution:**
```bash
# Check if Ollama is running
docker ps | findstr ollama

# Check Ollama health
curl http://localhost:11434

# Restart if needed
docker restart ollama-server
```

### Problem: "Ollama not responding"

**Solution:**
```bash
# Check logs
docker logs ollama-server

# Exec into container
docker exec -it ollama-server bash

# Check Ollama status
ollama list
```

---

## 🌐 Publishing to Cloud

### Docker Hub

```bash
# Login
docker login

# Tag image
docker tag product-advisor-webapp yourusername/ai-product-advisor:latest

# Push
docker push yourusername/ai-product-advisor:latest
```

### Deploy to AWS (ECS)

1. **Push to ECR:**
```bash
aws ecr create-repository --repository-name ai-product-advisor
docker tag product-advisor-webapp:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-product-advisor
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-product-advisor
```

2. **Create ECS Task:**
   - Use Fargate
   - 8 vCPU, 16GB RAM minimum
   - Mount EFS for model persistence

### Deploy to Azure (ACI)

```bash
az container create \
  --resource-group myResourceGroup \
  --name ai-product-advisor \
  --image yourusername/ai-product-advisor:latest \
  --dns-name-label ai-product-advisor \
  --ports 8501 11434 \
  --cpu 4 \
  --memory 16
```

### Deploy to Google Cloud (Cloud Run)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/ai-product-advisor

# Deploy
gcloud run deploy ai-product-advisor \
  --image gcr.io/PROJECT-ID/ai-product-advisor \
  --platform managed \
  --region us-central1 \
  --memory 16Gi \
  --cpu 4
```

---

## 🔒 Security Best Practices

### For Production Deployment

1. **Add Authentication**
   ```python
   # In app.py, add at the top:
   import streamlit_authenticator as stauth
   ```

2. **Use Environment Variables**
   ```yaml
   # docker-compose.webapp.yml
   environment:
     - OLLAMA_API_KEY=${OLLAMA_API_KEY}
   ```

3. **Enable HTTPS**
   - Use reverse proxy (nginx/Caddy)
   - Or cloud load balancer with SSL

4. **Limit Resource Usage**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '4'
         memory: 16G
   ```

5. **Regular Updates**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

---

## 📊 Performance Optimization

### Use GPU (if available)

```yaml
# docker-compose.webapp.yml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### Cache Models

Models are cached in `ollama-data` volume. They persist across container restarts.

### Use Faster Models

For faster responses:
- `llama3:latest` (4.7GB, ~15s response)
- `gpt-oss:20b` (13GB, ~60s response) ← Current
- `qwen3:30b` (18GB, ~90s response)

---

## 📈 Monitoring

### Basic Monitoring

```bash
# Resource usage
docker stats

# Disk usage
docker system df

# Container health
docker inspect ollama-server --format='{{.State.Health.Status}}'
```

### Advanced Monitoring

Use Docker monitoring tools:
- **Portainer** - Web UI for Docker
- **Prometheus** - Metrics collection
- **Grafana** - Visualization

---

## 🎓 Next Steps

### Enhancements
1. ✅ Add more AI models
2. ✅ Implement caching for faster responses
3. ✅ Add user authentication
4. ✅ Create API endpoints
5. ✅ Add product image generation
6. ✅ Implement chat history

### Sharing
1. **Share Locally:** Send Docker Compose file
2. **Share Online:** Deploy to cloud
3. **Create Tutorial:** Record demo video

---

## 💡 Tips & Tricks

### Speed Up Model Loading
```bash
# Pre-load models
docker exec ollama-server ollama pull llama3:latest
docker exec ollama-server ollama pull qwen3:30b
```

### Clean Up Space
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes (keeps ollama-data)
docker volume prune

# Full cleanup (WARNING: removes all data)
docker system prune -a --volumes
```

### Backup Models
```bash
# Export volume
docker run --rm -v ollama-data:/data -v ${PWD}:/backup alpine tar czf /backup/ollama-backup.tar.gz /data

# Restore volume
docker run --rm -v ollama-data:/data -v ${PWD}:/backup alpine tar xzf /backup/ollama-backup.tar.gz
```

---

## 📞 Support

### Issues?
1. Check logs: `docker-compose logs -f`
2. Restart services: `docker-compose restart`
3. Check system resources: `docker stats`
4. Rebuild: `docker-compose up -d --build`

### Resources
- **Ollama Docs:** https://ollama.ai/docs
- **Streamlit Docs:** https://docs.streamlit.io
- **Docker Docs:** https://docs.docker.com

---

**🎉 Congratulations! You're ready to deploy your AI Product Advisor!**

Choose your deployment option and run the commands above. For most users, I recommend starting with the **Streamlit Web App** (Option 2) as it provides the best user experience.

