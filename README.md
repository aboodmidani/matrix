# Matrix Scanner

> A focused web security assessment platform with a Matrix-themed UI.  
> **For authorized use only — only scan systems you own or have explicit permission to test.**

Demo: https://matrix-audit.netlify.app/

---

## Features

| Scan | Tool | Fallback |
|------|------|----------|
| DNS Reconnaissance | `dnsrecon` | Python `socket` |
| Port Scan | `nmap` | Python `socket` |
| Firewall / WAF Detection | `wafw00f` | HTTP header analysis |
| Technology Detection | Wappalyzer (via `python-Wappalyzer`) | Header/body heuristics |
| Subdomain Discovery | `subfinder` | DNS brute-force |

**Frontend:**
- Matrix rain background (katakana + latin chars)
- Real-time per-scan progress with status dots
- Stop scan at any time (AbortController)
- Export results as `.txt` report
- Pixel disintegration disclaimer animation
- Responsive — mobile + desktop

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Frontend | Vue 3, Vite, Tailwind CSS |
| Fonts | Orbitron, Share Tech Mono |
| Deployment | Docker (backend), Nginx (frontend) |

---

## Quick Start (Local)

### 1. Clone
```bash
git clone https://github.com/aboodmidani/matrix.git
cd matrix
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Install scanning tools (optional — fallbacks are used if missing):
```bash
# nmap
sudo apt install nmap          # Debian/Ubuntu
brew install nmap              # macOS

# dnsrecon + wafw00f (Python)
pip install dnsrecon wafw00f

# subfinder (Go binary)
# https://github.com/projectdiscovery/subfinder/releases
```

Create `backend/.env`:
```env
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

Start backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend
```bash
cd frontend
npm install
```

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

Start frontend:
```bash
npm run dev
```

Open: http://localhost:5173

---

## Docker

### Backend
```bash
docker build -t matrix-backend ./backend
docker run -p 8000:8000 matrix-backend
```

### Frontend
```bash
docker build -t matrix-frontend ./frontend
docker run -p 80:80 matrix-frontend
```

### Docker Compose (both together)
```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

```bash
docker compose up -d
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info + tool availability |
| `GET` | `/health` | Health check |
| `POST` | `/scan/dns` | DNS reconnaissance |
| `POST` | `/scan/ports` | Port scan (nmap) |
| `POST` | `/scan/firewall` | WAF / firewall detection |
| `POST` | `/scan/technologies` | Technology detection |
| `POST` | `/scan/subdomains` | Subdomain discovery |

All scan endpoints accept `application/x-www-form-urlencoded` with a `url` field:
```bash
curl -X POST http://localhost:8000/scan/dns \
  -d "url=https://example.com"
```

Interactive docs: http://localhost:8000/docs

---

## Environment Variables

### Backend (`backend/.env`)
| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `production` | `development` or `production` |
| `DEBUG` | `false` | Enable debug mode |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Bind port |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

### Frontend (`frontend/.env`)
| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend URL (e.g. `http://localhost:8000`) |

> **Note:** Never commit `.env` files. Both are listed in `.gitignore`.

---

## Project Structure

```
matrix/
├── backend/
│   ├── main.py              # FastAPI app, 5 scan endpoints
│   ├── config.py            # Settings (pydantic)
│   ├── tools.py             # check_tool(), run_command()
│   ├── requirements.txt
│   ├── Dockerfile
│   └── scans/
│       ├── dns_scan.py      # dnsrecon → socket fallback
│       ├── port_scan.py     # nmap → socket fallback
│       ├── firewall_scan.py # wafw00f → header fallback
│       ├── technology_scan.py
│       └── subdomain_scan.py # subfinder → brute-force fallback
└── frontend/
    ├── src/
    │   ├── views/Home.vue
    │   ├── components/
    │   │   ├── MatrixBackground.vue
    │   │   ├── ScanCard.vue
    │   │   ├── RecordGroup.vue
    │   │   └── DisclaimerCard.vue
    │   ├── composables/useScanner.js
    │   └── utils/exportReport.js
    ├── Dockerfile
    └── package.json
```

---

## Legal Disclaimer

This tool is for **educational purposes** and **authorized security testing only**.  
Only scan systems you own or have explicit written permission to test.  
Unauthorized scanning may be illegal in your jurisdiction.

---

## License

MIT — see [LICENSE](LICENSE)
