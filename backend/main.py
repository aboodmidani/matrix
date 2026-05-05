import re
import asyncio
import logging
import time
import ipaddress
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ── Helpers ──────────────────────────────────────────────────────────────────

_PRIVATE_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]


def _is_private_ip(hostname: str) -> bool:
    """Check if a hostname resolves to a private/internal IP."""
    import socket
    try:
        infos = socket.getaddrinfo(hostname, None)
        for info in infos:
            ip = ipaddress.ip_address(info[4][0])
            for network in _PRIVATE_NETWORKS:
                if ip in network:
                    return True
    except (socket.gaierror, ValueError):
        pass
    return False


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
    domain = parsed.netloc.split(':')[0]
    if not re.match(
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$',
        domain
    ):
        raise HTTPException(status_code=400, detail="Invalid domain")
    if _is_private_ip(domain):
        raise HTTPException(status_code=400, detail="Scanning private/internal IP addresses is not allowed")
    return url


def _domain(url: str) -> str:
    return urlparse(url).netloc.split(':')[0]


async def _get_scan_url(request: Request) -> str:
    """Dependency to extract and validate URL from form data."""
    data = await request.form()
    return _validate_url(data.get("url", ""))


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
@limiter.limit("30/minute")
async def scan_dns(request: Request, url: str = Depends(_get_scan_url)):
    domain = _domain(url)
    try:
        result = await asyncio.to_thread(run_dnsrecon, domain)
        return {"success": True, "domain": domain, "records": result.get("records", {})}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("DNS scan error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/ports")
@limiter.limit("20/minute")
async def scan_ports(request: Request, url: str = Depends(_get_scan_url)):
    domain = _domain(url)
    try:
        ports = await asyncio.to_thread(run_nmap_scan, domain)
        return {"success": True, "domain": domain, "ports": ports}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Port scan error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/firewall")
@limiter.limit("30/minute")
async def scan_firewall_endpoint(request: Request, url: str = Depends(_get_scan_url)):
    try:
        result = await asyncio.to_thread(scan_firewall, url)
        return {"success": True, "url": url, "firewall": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Firewall scan error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/technologies")
@limiter.limit("30/minute")
async def scan_technologies_endpoint(request: Request, url: str = Depends(_get_scan_url)):
    try:
        result = await asyncio.to_thread(scan_technologies, url)
        return {"success": True, "url": url, "technologies": result.get("technologies", {})}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Technology scan error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/subdomains")
@limiter.limit("15/minute")
async def scan_subdomains(request: Request, url: str = Depends(_get_scan_url)):
    domain = _domain(url)
    try:
        subdomains = await asyncio.to_thread(run_subfinder_scan, domain)
        return {"success": True, "domain": domain, "subdomains": subdomains}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Subdomain scan error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Global error handler ──────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT,
                reload=settings.DEBUG, log_level=settings.LOG_LEVEL.lower())
