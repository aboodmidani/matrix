import re
import logging
import time
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from tools import check_tool
from scans.dns_scan import run_dnsrecon
from scans.port_scan import run_nmap_scan
from scans.firewall_scan import scan_firewall
from scans.technology_scan import scan_technologies
from scans.subdomain_scan import run_subfinder_scan

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Matrix Scanner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _validate_url(raw: str) -> str:
    """Normalize and validate a URL. Returns the clean URL or raises 400."""
    if not raw:
        raise HTTPException(status_code=400, detail="URL is required")
    url = raw.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    parsed = urlparse(url)
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")
    domain = parsed.netloc
    if not re.match(
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*(:[0-9]{1,5})?$',
        domain
    ):
        raise HTTPException(status_code=400, detail="Invalid domain")
    return url


def _domain(url: str) -> str:
    return urlparse(url).netloc


# ── Root / Health ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "Matrix Scanner API",
        "version": "1.0.0",
        "tools": {
            "nmap":      check_tool("nmap"),
            "dnsrecon":  check_tool("dnsrecon"),
            "wafw00f":   check_tool("wafw00f"),
            "subfinder": check_tool("subfinder"),
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": int(time.time())}


# ── Scan endpoints ────────────────────────────────────────────────────────────

@app.post("/scan/dns")
async def scan_dns(request: Request):
    data = await request.form()
    url = _validate_url(data.get("url", ""))
    domain = _domain(url)
    try:
        result = run_dnsrecon(domain)
        return {"success": True, "domain": domain, "records": result.get("records", {})}
    except Exception as e:
        logger.error(f"DNS scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/ports")
async def scan_ports(request: Request):
    data = await request.form()
    url = _validate_url(data.get("url", ""))
    domain = _domain(url)
    try:
        ports = run_nmap_scan(domain)
        return {"success": True, "domain": domain, "ports": ports}
    except Exception as e:
        logger.error(f"Port scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/firewall")
async def scan_firewall_endpoint(request: Request):
    data = await request.form()
    url = _validate_url(data.get("url", ""))
    try:
        result = scan_firewall(url)
        return {"success": True, "url": url, "firewall": result}
    except Exception as e:
        logger.error(f"Firewall scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/technologies")
async def scan_technologies_endpoint(request: Request):
    data = await request.form()
    url = _validate_url(data.get("url", ""))
    try:
        result = scan_technologies(url)
        return {"success": True, "url": url, "technologies": result.get("technologies", {})}
    except Exception as e:
        logger.error(f"Technology scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/subdomains")
async def scan_subdomains(request: Request):
    data = await request.form()
    url = _validate_url(data.get("url", ""))
    domain = _domain(url)
    try:
        subdomains = run_subfinder_scan(domain)
        return {"success": True, "domain": domain, "subdomains": subdomains}
    except Exception as e:
        logger.error(f"Subdomain scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Global error handler ──────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=settings.DEBUG, log_level=settings.LOG_LEVEL.lower())
