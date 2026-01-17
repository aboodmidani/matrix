from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from scanners import *
from intelligence import *
from vulnerabilities import check_vulnerabilities, check_advanced_vulnerabilities
from directories import *
import re
import os

app = FastAPI(title="Web Security Audit API")

def validate_and_sanitize_url(url: str) -> str:
    """Validate and sanitize URL to prevent SSRF and other attacks"""
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    # Remove any leading/trailing whitespace
    url = url.strip()

    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # If no scheme, add https (secure by default)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    # Validate URL format
    if not url_pattern.match(url):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    parsed = urlparse(url)

    # Prevent SSRF by checking for private/internal IPs
    import socket
    try:
        hostname = parsed.netloc.split(':')[0]
        ip = socket.gethostbyname(hostname)
        if ip.startswith(('127.', '10.', '172.', '192.168.', '169.254.')):
            raise HTTPException(status_code=400, detail="Internal/private IP addresses are not allowed")
        # Check for IPv6 localhost
        if ip in ['::1', '0:0:0:0:0:0:0:1']:
            raise HTTPException(status_code=400, detail="Localhost addresses are not allowed")
    except socket.gaierror:
        pass  # Allow if DNS resolution fails, but scanner will handle it

    # Validate port if specified
    if ':' in parsed.netloc:
        port_part = parsed.netloc.split(':')[1]
        try:
            port = int(port_part)
            if port < 1 or port > 65535:
                raise HTTPException(status_code=400, detail="Invalid port number (must be 1-65535)")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid port format")

    # Limit URL length
    if len(url) > 2048:
        raise HTTPException(status_code=400, detail="URL too long")

    return url

# CORS middleware - dynamically configured from environment
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
if cors_origins:
    # Split by comma and strip whitespace for multiple origins
    allowed_origins = [origin.strip() for origin in cors_origins.split(",")]
else:
    allowed_origins = ["http://localhost:5173"]  # fallback

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Web Security Audit API"}

@app.post("/audit")
async def audit_website(request: Request):
    data = await request.form()
    url = data.get('url')
    url = validate_and_sanitize_url(url)

    # Get scan options (handle checkbox values - unchecked checkboxes are not sent)
    enable_dns = data.get('enable_dns', 'false') == 'true'
    enable_ports = data.get('enable_ports', 'false') == 'true'
    enable_vulns = data.get('enable_vulns', 'false') == 'true'
    enable_directories = data.get('enable_directories', 'false') == 'true'
    nmap_options = data.get('nmap_options', '-sV --version-intensity 2')

    try:
        parsed = urlparse(url)
        domain = parsed.netloc

        # Check if domain is IP or hostname
        import ipaddress
        try:
            ipaddress.ip_address(domain)
            is_ip = True
        except ValueError:
            is_ip = False

        results = {
            "url": url,
            "domain": domain,
        }

        # Conditional scanning based on options
        if enable_dns:
            try:
                if not is_ip:
                    # Only do DNS lookups for domain names, not IPs
                    results["dns"] = get_dns_info(domain)
                    results["hostnames"] = get_related_hostnames(domain)
                    # Get IP info using the resolved IP
                    dns_info = get_dns_info(domain)
                    ip_addr = dns_info.get('A_records', [domain])[0] if dns_info.get('A_records') else domain
                    results["ip_info"] = get_ip_info(ip_addr)
                else:
                    # For IP addresses, just get IP info
                    results["ip_info"] = get_ip_info(domain)
                    results["dns"] = {"note": "DNS resolution not applicable for IP addresses"}
            except Exception as e:
                results["dns_error"] = f"DNS scan failed: {str(e)}"

        # SSL and security headers are always scanned as they provide basic security info
        try:
            results["ssl_info"] = get_ssl_info(domain)
        except Exception as e:
            results["ssl_info"] = {"error": f"SSL check failed: {str(e)}"}

        try:
            results["headers"] = get_security_headers(url)
        except Exception as e:
            results["headers"] = {"error": f"Header check failed: {str(e)}"}

        # Technology detection - only run if target is responsive
        try:
            tech_results = detect_technologies(url)
            # Only include technology results if no error occurred
            if not any('error' in str(result) for result in tech_results):
                results["technologies"] = tech_results
        except Exception as e:
            # Don't include technology results if detection fails
            pass

        if enable_ports:
            try:
                # Use the full netloc (which includes port if specified)
                target_host = parsed.netloc
                results["ports"] = scan_ports(target_host, nmap_options)
            except Exception as e:
                results["ports"] = [{"error": f"Port scan failed: {str(e)}"}]

        # Run vulnerability checks separately
        if enable_vulns:
            try:
                vuln_results = check_vulnerabilities(url)
                results["vulnerabilities"] = vuln_results
            except Exception as e:
                results["vulnerabilities"] = [{"type": "Scan Error", "severity": "Info", "description": f"Vulnerability scan failed: {str(e)}"}]
        else:
            results["vulnerabilities"] = [{
                "type": "Vulnerability Scan Disabled",
                "severity": "Info",
                "description": "Vulnerability scanning was disabled in scan options"
            }]

        # Run directory scan separately
        if enable_directories:
            try:
                dir_results = check_directories(url)
                results["directories"] = dir_results
            except Exception as e:
                results["directories"] = [{"type": "Directory Scan Error", "severity": "Info", "description": f"Directory scanning failed: {str(e)}"}]
        else:
            results["directories"] = [{
                "type": "Directory Scan Disabled",
                "severity": "Info",
                "description": "Directory scanning was disabled in scan configuration"
            }]

        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
