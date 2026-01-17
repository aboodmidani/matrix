# Web Security Matrix

> **Professional Penetration Testing Framework** - Pure Python Implementation with Matrix-themed Interface

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.4+-brightgreen.svg)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive web security audit framework featuring pure Python implementation, advanced vulnerability detection, and a stunning Matrix-themed interface. No external tools required - everything runs natively in Python.

## 🚀 **Key Features**

### **🔒 Security Analysis Modules**
- **SSL Certificate Analysis**: Validity, issuer, expiration with smart error handling
- **Security Headers Check**: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, etc.
- **DNS Intelligence**: A, AAAA, MX, TXT, CNAME, NS records enumeration
- **Technology Detection**: 50+ frameworks, CMS, servers, CDNs with confidence scoring
- **Port Scanning**: Nmap-powered service detection (21, 22, 25, 53, 80, 443, 993, 995, 3306, 5432)
- **Advanced Vulnerability Scanning**:
  - SQL Injection (10+ payloads, error pattern detection)
  - Cross-Site Scripting (XSS) with multiple attack vectors
  - Command Injection testing
  - Directory Traversal vulnerabilities
  - Open Redirect detection
  - Information Disclosure (sensitive paths)
  - Security Headers validation

### **🎨 Professional Interface**
- **Matrix-themed UI**: Cyberpunk aesthetics with animated background
- **Real-time Progress**: Live scanning status with accurate module tracking
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode**: Professional terminal-style interface
- **Live Clock**: Always displays current time in header
- **Smooth Animations**: Professional transitions and effects

### **⚡ Performance & Security**
- **Pure Python**: No external tools - zero installation dependencies
- **Smart IP/Domain Handling**: Auto-detects and adjusts scanning strategy
- **Rate Limiting**: Built-in protection against abuse
- **Input Sanitization**: Comprehensive validation and SSRF protection
- **Error Handling**: Graceful degradation with user-friendly messages
- **Fast Scanning**: Optimized algorithms with timeout management

## 🛠 **Tech Stack**

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend** | Python FastAPI | 3.8+ | RESTful API with async support |
| **Frontend** | Vue.js 3 + Vite | 3.4+ | Reactive SPA with hot reload |
| **Styling** | Tailwind CSS | 3.3+ | Utility-first responsive design |
| **Animation** | Framer Motion | 11.0+ | Smooth transitions and effects |
| **Icons** | Icons8 API | Latest | Professional technology icons |

## 📦 **Installation**

### **Prerequisites**
- **Python 3.8+**: [Download from python.org](https://python.org)
- **Node.js 16+**: [Download from nodejs.org](https://nodejs.org)

### **🚀 Quick Start**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aboodmidani/matrix.git
   cd matrix
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Setup Frontend** (in new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### **🐳 Docker Deployment** (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:5173
```

## 🎯 **Usage**

1. **Accept Disclaimer**: Review and accept the legal disclaimer
2. **Configure Scan**: Select target URL and choose scan modules:
   - `[DNS]` Domain enumeration and reconnaissance
   - `[NET]` Port scanning and service detection
   - `[VULN]` Vulnerability assessment
   - `[DIR]` Directory traversal checking
3. **Initiate Audit**: Click "INITIATE SCAN" to begin analysis
4. **Monitor Progress**: Watch real-time scanning progress
5. **Review Results**: Analyze comprehensive security report

## 📊 **API Documentation**

### **Endpoints**
- `GET /` - API health check
- `POST /audit` - Perform security audit

### **Request Format**
```json
{
  "url": "https://example.com",
  "enable_dns": true,
  "enable_ports": true,
  "enable_vulns": true,
  "enable_directories": true
}
```

### **Response Structure**
```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "ssl_info": {...},
  "headers": {...},
  "technologies": [...],
  "vulnerabilities": [...],
  "directories": [...],
  "dns": {...},
  "ports": [...]
}
```

## 🔐 **Security & Legal**

### **⚠️ Important Notice**
This tool is designed for **educational and authorized security testing purposes only**.

- **Always obtain explicit permission** before scanning websites
- **Unauthorized scanning** may violate laws and terms of service
- **Use responsibly** and ethically
- **Report vulnerabilities** to website owners, not exploit them

### **🛡️ Built-in Security**
- **Input Validation**: Comprehensive URL and parameter sanitization
- **SSRF Protection**: Prevents server-side request forgery attacks
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Safe failure modes with no sensitive data exposure

## 🧪 **Testing**

```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests
cd frontend
npm run test

# End-to-end testing
npm run test:e2e
```

## 🐳 **Deployment**

### **Production Setup**
```bash
# Build frontend
cd frontend
npm run build

# Production backend (no --reload)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Docker Production**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web-security-matrix:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository on GitHub
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgements**

- **FastAPI** for the excellent async web framework
- **Vue.js** for the reactive frontend framework
- **Nmap** for network scanning capabilities
- **Tailwind CSS** for utility-first styling
- **Icons8** for professional technology icons

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/aboodmidani/matrix/issues)
- **Discussions**: [GitHub Discussions](https://github.com/aboodmidani/matrix/discussions)
- **Email**: abood@example.com

---

**Made with ❤️ for the cybersecurity community**
