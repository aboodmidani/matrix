# 🚀 Deployment Guide - Web Security Matrix

## Overview

This guide covers deploying the Web Security Matrix to **Netlify** (frontend) and **Render** (backend).

## 🖥️ Frontend Deployment (Netlify)

### Method 1: Automatic (Recommended)

1. **Connect Repository:**
   - Go to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   - Select the `matrix` repository

2. **Build Settings:**
   ```
   Base directory: frontend/
   Build command: npm run build
   Publish directory: frontend/dist
   ```

3. **Environment Variables:**
   ```
   VITE_API_URL=https://matrix-9s9s.onrender.com
   NODE_VERSION=18
   ```

4. **Deploy:**
   - Netlify will auto-deploy on git pushes
   - Your site will be available at: `https://your-app-name.netlify.app`

### Method 2: Manual Upload

1. **Build Locally:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Upload `dist` folder:**
   - Drag and drop the `dist` folder to Netlify's deploy area
   - Or use Netlify CLI: `netlify deploy --prod --dir=frontend/dist`

### Netlify Configuration

The `frontend/netlify.toml` file contains:
- ✅ Build settings
- ✅ Environment variables
- ✅ Security headers
- ✅ SPA routing redirects
- ✅ Asset caching

## 🔧 Backend Deployment (Render)

### Method 1: Automatic (Recommended)

1. **Connect Repository:**
   - Go to [Render](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `matrix` repository

2. **Service Configuration:**
   ```
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
   ```

3. **Environment Variables:**
   ```
   ENVIRONMENT=production
   CORS_ORIGINS=https://your-netlify-app.netlify.app
   DEBUG=false
   SECRET_KEY=your-secret-key-here
   ```

4. **Deploy:**
   - Render will auto-deploy on git pushes
   - Your API will be available at: `https://your-app-name.onrender.com`

### Method 2: Manual Deployment

1. **Push to Render:**
   - Use Render's dashboard to deploy
   - Or use Render CLI if installed

### Render Configuration

The `backend/render.yaml` file contains:
- ✅ Service type and runtime
- ✅ Build and start commands
- ✅ Environment variables
- ✅ Health check configuration

## 🔗 Connecting Frontend to Backend

### 1. Update Frontend Environment Variable

After deploying both services, update the frontend's `VITE_API_URL`:

**In Netlify Dashboard:**
```
VITE_API_URL=https://your-render-app.onrender.com
```

**Or update `frontend/netlify.toml`:**
```toml
[build.environment]
  VITE_API_URL = "https://your-render-app.onrender.com"
```

### 2. Update Backend CORS

In Render dashboard, set:
```
CORS_ORIGINS=https://your-netlify-app.netlify.app
```

## 🌐 Custom Domain (Optional)

### Netlify Custom Domain:
1. Go to Site settings → Domain management
2. Add your custom domain
3. Configure DNS records as instructed

### Render Custom Domain:
1. Go to Service settings → Custom Domains
2. Add your custom domain
3. Update CORS origins with new domain

## 🔒 Security Considerations

### Environment Variables:
- ✅ Never commit secrets to git
- ✅ Use Render/Netlify environment variables
- ✅ Rotate keys regularly

### CORS Configuration:
- ✅ Only allow your frontend domain
- ✅ Use HTTPS in production
- ✅ Set appropriate headers

### SSL/TLS:
- ✅ Netlify provides automatic SSL
- ✅ Render provides automatic SSL
- ✅ Both use Let's Encrypt certificates

## 🚀 Deployment Checklist

### Frontend (Netlify):
- [ ] Repository connected
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Custom domain (optional)
- [ ] SSL certificate active

### Backend (Render):
- [ ] Repository connected
- [ ] Runtime set to Python 3
- [ ] Build command configured
- [ ] Start command configured
- [ ] Environment variables set
- [ ] CORS origins configured

### Integration:
- [ ] Frontend `VITE_API_URL` updated
- [ ] Backend CORS allows frontend
- [ ] Both services deployed successfully
- [ ] Test full application flow

## 🔍 Testing Deployment

### Frontend Tests:
```bash
# Test build locally
cd frontend
npm run build
npm run preview
```

### Backend Tests:
```bash
# Test API locally
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Integration Tests:
1. Visit frontend URL
2. Try a basic scan
3. Check browser network tab for API calls
4. Verify CORS is working

## 🐛 Troubleshooting

### Common Issues:

**Build Failures:**
- Check build logs in Netlify/Render dashboard
- Ensure all dependencies are in requirements.txt/package.json
- Verify Python/Node versions match

**CORS Errors:**
- Check CORS_ORIGINS in backend
- Verify VITE_API_URL in frontend
- Ensure HTTPS URLs are used

**Environment Variables:**
- Check variable names match exactly
- Ensure no extra spaces or quotes
- Verify variables are set in correct service

**API Connection Issues:**
- Check backend is running and healthy
- Verify API endpoints are accessible
- Check firewall/network restrictions

## 📞 Support

- **Netlify Docs:** https://docs.netlify.com
- **Render Docs:** https://docs.render.com
- **GitHub Issues:** For project-specific issues

---

**🎉 Your Web Security Matrix is now ready for production deployment!**
