# Web Security Matrix

**Advanced web security scanning and analysis platform with comprehensive security features and Matrix-themed UI**

## 🚀 Features

### 🔒 Security-First Architecture
- **Input Validation & Sanitization**: XSS protection, SQL injection prevention
- **Rate Limiting**: Prevents abuse and DoS attacks
- **Security Headers**: Comprehensive OWASP security headers
- **Error Handling**: Secure error responses without information leakage
- **CORS Protection**: Environment-based CORS configuration

### 🛡️ Comprehensive Security Scanning
- **DNS Reconnaissance**: Domain analysis and record enumeration
- **Port Scanning**: Nmap-based port and service detection
- **Directory Enumeration**: Dirsearch-powered directory discovery
- **Vulnerability Assessment**: Nikto-based security vulnerability scanning
- **Technology Detection**: Wappalyzer-based tech stack identification
- **WAF Detection**: Firewall identification and bypass testing

### 🎨 Matrix-Themed UI
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Matrix Animation**: CSS-based Matrix rain background
- **Terminal-style Interface**: Authentic hacker terminal aesthetic
- **Progress Indicators**: Real-time scan progress with animations
- **Error Handling**: User-friendly error messages and notifications

### 🏗️ Modern Architecture
- **FastAPI Backend**: High-performance Python API
- **Vue.js Frontend**: Reactive single-page application
- **Docker Support**: Containerized deployment
- **Environment-based Configuration**: Development/Production modes
- **Comprehensive Testing**: Automated test suite with security validation

## 📋 Requirements

### Backend
- Python 3.8+
- FastAPI
- Uvicorn
- Various security and scanning tools (see `backend/requirements.txt`)

### Frontend
- Node.js 16+
- Vue.js 3
- Vite
- Tailwind CSS

### Optional (for scanning tools)
- Nmap
- Dirsearch
- Nikto
- Wafw00f
- DNSRecon

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd matrix
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
Create `.env` files:

**Backend (.env):**
```env
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

### 5. Run the Application
```bash
# Start backend
cd backend
python main.py

# In another terminal, start frontend
cd frontend
npm run dev
```

### 6. Access the Application
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

**Backend Configuration:**
- `ENVIRONMENT`: `development` or `production`
- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `CORS_ORIGINS`: Allowed CORS origins (JSON array)

**Frontend Configuration:**
- `VITE_API_URL`: Backend API URL

### Security Configuration
The application includes comprehensive security features:

1. **Input Validation**: All user inputs are sanitized and validated
2. **Rate Limiting**: 100 requests per minute per IP
3. **Security Headers**: OWASP-recommended headers
4. **Error Handling**: Secure error responses
5. **CORS Protection**: Environment-based CORS configuration

## 🧪 Testing

### Run Test Suite
```bash
python test_matrix_app.py
```

### Test Coverage
The test suite covers:
- ✅ API health and info endpoints
- ✅ Input validation and sanitization
- ✅ Security headers verification
- ✅ Rate limiting functionality
- ✅ All scan endpoints
- ✅ Comprehensive audit functionality
- ✅ Download functionality

### Security Testing
The application includes security-focused tests:
- XSS attack prevention
- SQL injection prevention
- Input sanitization validation
- Security header verification
- Rate limiting effectiveness

## 🐳 Docker Deployment

### Build and Run
```bash
# Build images
docker-compose build

# Run services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Docker Compose Services
- `backend`: FastAPI application server
- `frontend`: Vue.js frontend with Nginx
- `redis`: Rate limiting and caching (optional)

## 📊 API Endpoints

### Core Endpoints
- `GET /` - API root and tool availability
- `GET /health` - Health check
- `POST /audit` - Comprehensive security audit

### Individual Scan Endpoints
- `POST /scan/dns` - DNS reconnaissance
- `POST /scan/ports` - Port scanning
- `POST /scan/directories` - Directory enumeration
- `POST /scan/vulnerabilities` - Vulnerability scanning
- `POST /scan/technologies` - Technology detection
- `POST /scan/firewall` - WAF detection

### Utility Endpoints
- `POST /download-results` - Download scan results

## 🔒 Security Features

### Input Validation
- URL format validation
- XSS prevention through HTML escaping
- Dangerous protocol filtering
- Null byte removal

### Rate Limiting
- 100 requests per minute per IP
- Sliding window implementation
- Automatic cleanup of old requests

### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Content-Security-Policy`
- `Strict-Transport-Security`

### Error Handling
- Secure error messages
- No information leakage
- Structured error responses
- Logging for security events

## 🎨 UI Components

### MatrixUI Component
- Matrix rain background animation
- Loading overlays with progress
- Error and success toasts
- Responsive design

### Scan Components
- Individual scan pages for each type
- Real-time progress indicators
- Download functionality
- Error handling and validation

### Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Adaptive layouts
- Performance optimized

## 📈 Performance Optimization

### Backend Optimizations
- Async request handling
- Connection pooling
- Efficient error handling
- Minimal dependencies

### Frontend Optimizations
- Lazy loading
- Efficient state management
- Optimized CSS animations
- Minimal bundle size

### Security Optimizations
- Input validation caching
- Rate limiting efficiency
- Secure session handling
- Minimal attack surface

## 🚨 Security Considerations

### For Production Use
1. **Use HTTPS**: Always use HTTPS in production
2. **Firewall Configuration**: Configure proper firewall rules
3. **Rate Limiting**: Adjust rate limits based on your needs
4. **Logging**: Monitor security logs regularly
5. **Updates**: Keep dependencies updated

### Legal Compliance
- **Authorization**: Only scan systems you own or have permission to test
- **Compliance**: Follow local laws and regulations
- **Responsible Disclosure**: Report vulnerabilities responsibly
- **Data Protection**: Handle scan results securely

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use Vue.js best practices for frontend
- Maintain security-focused coding practices
- Document all changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛡️ Security Disclaimer

This tool is intended for:
- Educational purposes
- Authorized security testing
- Security research
- Defensive security applications

**Important**: Only use this tool on systems you own or have explicit permission to test. Unauthorized scanning may be illegal and is strictly prohibited.

## 📞 Support

For issues, questions, or contributions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include logs and reproduction steps
4. Follow security best practices

## 🔄 Changelog

### Version 3.0.0
- Complete security overhaul
- Input validation and sanitization
- Rate limiting implementation
- Security headers
- Matrix-themed UI redesign
- Comprehensive test suite
- Docker support
- Performance optimizations

### Previous Versions
- Version 2.x: Initial Vue.js frontend
- Version 1.x: Basic FastAPI backend

---

**⚠️ Warning**: This tool is for educational and authorized security testing purposes only. Use responsibly and in compliance with all applicable laws and regulations.