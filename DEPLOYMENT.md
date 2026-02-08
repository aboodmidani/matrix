# Web Security Matrix - Deployment Guide

This guide provides step-by-step instructions for deploying the Web Security Matrix application to various platforms.

## 🚀 Quick Deployment

### Option 1: Render (Recommended)
1. **Fork the repository**
2. **Create Render account** at [render.com](https://render.com)
3. **Connect GitHub repository**
4. **Configure environment variables** (see below)
5. **Deploy!**

### Option 2: Railway
1. **Fork the repository**
2. **Create Railway account** at [railway.app](https://railway.app)
3. **Import GitHub repository**
4. **Configure environment variables**
5. **Deploy!**

### Option 3: Docker
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t matrix-backend ./backend
docker build -t matrix-frontend ./frontend
```

## 📋 Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Environment
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=10000
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=["https://your-frontend-url.com","https://your-app-name.onrender.com"]

# Security (optional)
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=https://your-backend-url.com
```

## 🔧 Platform-Specific Setup

### Render Configuration

#### Backend Service
1. **Service Type**: Web Service
2. **Runtime**: Python
3. **Build Command**: `cd backend && pip install -r requirements.txt`
4. **Start Command**: `cd backend && python main.py`
5. **Port**: `10000`

#### Frontend Service
1. **Service Type**: Static Site
2. **Build Command**: `cd frontend && npm install && npm run build`
3. **Publish Directory**: `frontend/dist`
4. **Environment**: Production

#### Environment Variables for Render
```env
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=10000
LOG_LEVEL=INFO
CORS_ORIGINS=["https://your-frontend.onrender.com"]
```

### Railway Configuration

#### Backend Service
1. **Service Type**: Web Service
2. **Runtime**: Python
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python main.py`
5. **Port**: `10000`

#### Frontend Service
1. **Service Type**: Static Site
2. **Build Command**: `npm install && npm run build`
3. **Publish Directory**: `dist`

#### Environment Variables for Railway
```env
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=10000
LOG_LEVEL=INFO
CORS_ORIGINS=["https://your-frontend.up.railway.app"]
```

### Netlify Configuration

#### Frontend Only (Connect to external backend)
1. **Connect GitHub repository**
2. **Build Command**: `npm run build`
3. **Publish Directory**: `dist`
4. **Environment Variables**:
   ```env
   VITE_API_URL=https://your-backend-url.com
   ```

### Vercel Configuration

#### Frontend Only
1. **Connect GitHub repository**
2. **Build Command**: `npm run build`
3. **Output Directory**: `dist`
4. **Environment Variables**:
   ```env
   VITE_API_URL=https://your-backend-url.com
   ```

## 🔒 Security Considerations

### Production Security Checklist

- [ ] **HTTPS**: Ensure both frontend and backend use HTTPS
- [ ] **Environment Variables**: Never commit secrets to repository
- [ ] **CORS**: Configure CORS origins for your specific domains
- [ ] **Rate Limiting**: Adjust rate limits based on your needs
- [ ] **Logging**: Monitor logs for security events
- [ ] **Updates**: Keep dependencies updated
- [ ] **Firewall**: Configure proper firewall rules
- [ ] **Backups**: Set up regular backups

### CORS Configuration

Update the `CORS_ORIGINS` environment variable to include only your trusted domains:

```env
CORS_ORIGINS=["https://your-frontend.com","https://your-app.onrender.com"]
```

### Rate Limiting

Adjust rate limits based on your expected traffic:

```env
RATE_LIMIT_REQUESTS=100    # Requests per window
RATE_LIMIT_WINDOW=60       # Window in seconds
```

## 🐳 Docker Deployment

### Docker Compose (Recommended)
```bash
# Clone and setup
git clone <repository-url>
cd matrix

# Build and deploy
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Deployment
```bash
# Build backend
cd backend
docker build -t matrix-backend .
docker run -d -p 10000:10000 --name matrix-backend matrix-backend

# Build frontend
cd frontend
docker build -t matrix-frontend .
docker run -d -p 80:80 --name matrix-frontend matrix-frontend
```

## 📊 Monitoring and Maintenance

### Health Checks
- **Backend**: `GET /health`
- **Frontend**: Check if static files load

### Logs
```bash
# View backend logs
docker logs matrix-backend

# View frontend logs
docker logs matrix-frontend

# Follow logs in real-time
docker logs -f matrix-backend
```

### Performance Monitoring
- Monitor response times
- Check error rates
- Track resource usage
- Review security logs

### Updates
```bash
# Pull latest changes
git pull

# Rebuild and redeploy
docker-compose down
docker-compose build
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

#### CORS Errors
- Check `CORS_ORIGINS` environment variable
- Ensure frontend and backend URLs match
- Verify HTTPS configuration

#### Connection Timeouts
- Check backend service is running
- Verify port configuration
- Check firewall rules

#### Missing Dependencies
- Ensure `requirements.txt` is up to date
- Check Python version compatibility
- Verify Docker images build correctly

#### Environment Variables Not Loading
- Check `.env` file location
- Verify environment variable names
- Restart services after changes

### Debug Mode
For development debugging:

```env
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

### Production Debugging
```bash
# Check service status
docker ps

# View container logs
docker logs container-name

# Enter container for debugging
docker exec -it container-name bash
```

## 📞 Support

For deployment issues:
1. Check the logs first
2. Verify environment variables
3. Test locally before deploying
4. Check platform-specific documentation
5. Create an issue with detailed information

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: render-oss/deploy-action@v1.1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### Automated Testing
```bash
# Run tests before deployment
python test_matrix_app.py

# Check for security vulnerabilities
pip install safety
safety check

# Lint code
pip install flake8
flake8 backend/
```

---

**Note**: Always test deployments in a staging environment before production. Monitor your application after deployment and be prepared to roll back if issues occur.