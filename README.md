# Web Security Matrix - Simplified Edition

A comprehensive web security audit framework that uses built-in command-line tools (nslookup, nmap, curl) to perform security scans and displays results in a Matrix-themed interface.

## 🚀 **Quick Start**

### **Start the Backend (Terminal 1)**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

### **Start the Frontend (Terminal 2)**
```bash
cd frontend
npm run dev
```

### **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## 🛠 **Features**

### **Backend (Python + FastAPI)**
- **DNS Scan**: Uses `nslookup` to enumerate DNS records (A, AAAA, MX, NS, TXT)
- **Port Scan**: Uses `nmap` to scan common ports (21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432)
- **Directory Scan**: Uses `curl` to check for common directories and files
- **Vulnerability Scan**: Uses `curl` to test for SQL injection, XSS, and directory traversal

### **Frontend (Vue.js)**
- **Matrix-themed Interface**: Cyberpunk aesthetics with animated background
- **Real-time Progress**: Live scanning status with module tracking
- **Professional Results Display**: Organized security reports
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📊 **Scan Modules**

1. **[DNS] Domain Enumeration**
   - A, AAAA, MX, NS, TXT record lookup
   - Uses `nslookup` command

2. **[NET] Port Reconnaissance**
   - Scans 13 common ports
   - Service detection and version info
   - Uses `nmap` command

3. **[DIR] Directory Traversal**
   - Checks 11 common directories
   - Tests for exposed files and paths
   - Uses `curl` command

4. **[VULN] Vulnerability Assessment**
   - SQL injection testing
   - Cross-Site Scripting (XSS) testing
   - Directory traversal testing
   - Uses `curl` command

## 🔧 **Requirements**

### **Backend**
- Python 3.8+
- FastAPI
- Uvicorn
- Requests

### **Frontend**
- Node.js 16+
- Vue.js 3
- Vite
- Tailwind CSS

### **System Tools** (Must be installed on system)
- `nslookup` (for DNS queries)
- `nmap` (for port scanning)
- `curl` (for HTTP requests)

## 🚨 **Legal Notice**

This tool is for **educational and authorized security testing purposes only**.

- **Always obtain explicit permission** before scanning websites
- **Unauthorized scanning** may violate laws and terms of service
- **Use responsibly** and ethically
- **Report vulnerabilities** to website owners, not exploit them

## 📝 **Usage**

1. **Accept Disclaimer**: Review and accept the legal disclaimer
2. **Configure Scan**: Select target URL and choose scan modules
3. **Initiate Audit**: Click "INITIATE SCAN" to begin analysis
4. **Monitor Progress**: Watch real-time scanning progress
5. **Review Results**: Analyze comprehensive security report

## 🛡️ **Security Features**

- **Input Validation**: Comprehensive URL and parameter sanitization
- **Error Handling**: Safe failure modes with no sensitive data exposure
- **Timeout Protection**: Built-in timeouts for all external commands
- **Rate Limiting**: Protection against abuse

## 🐛 **Troubleshooting**

### **Backend Issues**
- Ensure Python virtual environment is activated
- Check that required packages are installed
- Verify system has nslookup, nmap, and curl installed

### **Frontend Issues**
- Ensure Node.js and npm are installed
- Check that all dependencies are installed
- Verify backend is running on port 8000

### **Scan Issues**
- Check target URL is valid and accessible
- Verify system tools (nslookup, nmap, curl) are working
- Check firewall settings for outbound connections

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/web-security-matrix/issues)
- **Documentation**: See this README for usage instructions

---

**Made with ❤️ for the cybersecurity community**