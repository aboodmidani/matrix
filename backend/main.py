from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import logging
import time
import os
import re
import html
import json
import tempfile
from urllib.parse import urlparse, quote, unquote
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, validator
import asyncio
from datetime import datetime, timedelta
import secrets

# Import configuration and tools
from config import settings
from tools import tool_manager
from security import (
    InputValidator, rate_limiter,
    validate_and_sanitize_url, sanitize_user_input, validate_scan_parameters
)

# Import scan functions
from scans.directory_scan import run_dirsearch_scan
from scans.vulnerability_scan import run_nikto_scan
from scans.technology_scan import scan_technologies
from scans.firewall_scan import scan_firewall
from scans.dns_scan import run_dnsrecon
from scans.port_scan import run_nmap_scan
from scans.subdomain_scan import run_subfinder_scan

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Web Security Matrix API",
    description="Advanced web security scanning and analysis API",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security middleware configuration
if settings.ENVIRONMENT == "production":
    # Redirect HTTP to HTTPS in production
    app.add_middleware(HTTPSRedirectMiddleware)

# CORS middleware with proper environment-based configuration
if settings.ENVIRONMENT == "production":
    # Production CORS - more restrictive
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://matrix-audit.netlify.app/",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-API-Key"],
        max_age=3600,
        expose_headers=["Content-Disposition"]
    )
else:
    # Development CORS - more permissive for local development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-API-Key"],
        max_age=3600,
        allow_origin_regex=r"https?://localhost:\d+",
        expose_headers=["Content-Disposition"]
    )

# Trusted host middleware for production
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.onrender.com", "*.netlify.app"]
    )

def sanitize_input(input_str: str) -> str:
    """Sanitize user input to prevent XSS attacks"""
    if not input_str:
        return ""
    
    # Remove any HTML/script tags
    import re
    sanitized = re.sub(r'<[^>]*>', '', input_str)
    
    # Remove javascript: protocol and other dangerous protocols
    sanitized = re.sub(r'^(javascript|data|vbscript|file):', '', sanitized, flags=re.IGNORECASE)
    
    # Remove any null bytes
    sanitized = sanitized.replace('\x00', '')
    
    # HTML escape special characters
    sanitized = html.escape(sanitized)
    
    return sanitized.strip()

def validate_url(url: str) -> str:
    """Validate and normalize URL with XSS protection"""
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    # First sanitize the input
    url = sanitize_input(url)
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Validate URL format
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Additional validation: ensure the domain looks valid
        domain = parsed.netloc
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*(:[0-9]{1,5})?$', domain):
            raise HTTPException(status_code=400, detail="Invalid domain format")
        
        return url
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")

def get_domain_from_url(url: str) -> str:
    """Extract domain from URL"""
    parsed = urlparse(url)
    return parsed.netloc

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Web Security Matrix API",
        "version": "3.0.0",
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "available_tools": {
            "dnsrecon": tool_manager.check_tool_availability('dnsrecon'),
            "nmap": tool_manager.check_tool_availability('nmap'),
            "dirsearch": tool_manager.check_tool_availability('dirsearch'),
            "nikto": tool_manager.check_tool_availability('nikto'),
            "wafw00f": tool_manager.check_tool_availability('wafw00f'),
            "subfinder": tool_manager.check_tool_availability('subfinder'),
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": int(time.time())}

@app.post("/audit")
async def audit_website(request: Request):
    """
    Comprehensive security audit endpoint
    
    Performs multiple types of security scans on a target website
    """
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        domain = get_domain_from_url(url)
        
        # Get scan options
        scan_options = {
            'enable_dns': data.get('enable_dns', 'false').lower() == 'true',
            'enable_ports': data.get('enable_ports', 'false').lower() == 'true',
            'enable_technologies': data.get('enable_technologies', 'false').lower() == 'true',
            'enable_firewall': data.get('enable_firewall', 'false').lower() == 'true',
            'enable_vulnerabilities': data.get('enable_vulnerabilities', 'false').lower() == 'true',
            'enable_directories': data.get('enable_directories', 'false').lower() == 'true',
            'enable_subdomains': data.get('enable_subdomains', 'false').lower() == 'true',
            'wordlist': data.get('wordlist', 'common')
        }
        
        results = {
            "url": url,
            "domain": domain,
            "timestamp": int(time.time()),
            "scan_options": scan_options,
            "results": {}
        }
        
        # Perform scans based on options
        if scan_options['enable_dns']:
            try:
                dns_result = run_dnsrecon(domain)
                results["results"]["dns"] = dns_result
            except Exception as e:
                logger.error(f"DNS scan failed for {domain}: {e}")
                results["results"]["dns"] = {"error": f"DNS scan failed: {str(e)}"}
        
        if scan_options['enable_ports']:
            try:
                port_result = run_nmap_scan(domain)
                results["results"]["ports"] = port_result
            except Exception as e:
                logger.error(f"Port scan failed for {domain}: {e}")
                results["results"]["ports"] = [{"error": f"Port scan failed: {str(e)}"}]
        
        if scan_options['enable_directories']:
            try:
                dir_result = run_dirsearch_scan(url, scan_options['wordlist'])
                results["results"]["directories"] = dir_result
            except Exception as e:
                logger.error(f"Directory scan failed for {url}: {e}")
                results["results"]["directories"] = [{"error": f"Directory scan failed: {str(e)}"}]
        
        if scan_options['enable_vulnerabilities']:
            try:
                vuln_result = run_nikto_scan(url)
                results["results"]["vulnerabilities"] = vuln_result
            except Exception as e:
                logger.error(f"Vulnerability scan failed for {url}: {e}")
                results["results"]["vulnerabilities"] = [{"error": f"Vulnerability scan failed: {str(e)}"}]
        
        if scan_options['enable_technologies']:
            try:
                tech_result = scan_technologies(url)
                results["results"]["technologies"] = tech_result
            except Exception as e:
                logger.error(f"Technology scan failed for {url}: {e}")
                results["results"]["technologies"] = {"error": f"Technology scan failed: {str(e)}"}
        
        if scan_options['enable_firewall']:
            try:
                firewall_result = scan_firewall(url)
                results["results"]["firewall"] = firewall_result
            except Exception as e:
                logger.error(f"Firewall scan failed for {url}: {e}")
                results["results"]["firewall"] = {"error": f"Firewall scan failed: {str(e)}"}
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/scan/dns")
async def scan_dns(request: Request):
    """DNS reconnaissance scan endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        domain = get_domain_from_url(url)
        
        # Use the proper scan function
        result = run_dnsrecon(domain)
        
        # Format response for frontend
        if 'error' in result:
            return {
                "success": False,
                "url": url,
                "domain": domain,
                "scan_type": "dns",
                "command": "dnsrecon",
                "output": "",
                "error": result['error']
            }
        
        return {
            "success": True,
            "url": url,
            "domain": domain,
            "scan_type": "dns",
            "command": "dnsrecon",
            "output": result.get('raw_output', ''),
            "records": result.get('records', {}),
            "error": None
        }
    except Exception as e:
        logger.error(f"DNS scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/ports")
async def scan_ports(request: Request):
    """Port scanning endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        domain = get_domain_from_url(url)
        
        # Use the proper scan function
        result = run_nmap_scan(domain)
        
        # Format response for frontend
        if result and len(result) > 0 and 'error' in result[0]:
            return {
                "success": False,
                "url": url,
                "domain": domain,
                "scan_type": "ports",
                "command": "nmap",
                "output": "",
                "error": result[0]['error']
            }
        
        # Format ports for display
        port_list = []
        for port in result:
            port_list.append(f"Port {port['port']}/{port['protocol']}: {port['service']} ({port['state']})")
        
        return {
            "success": True,
            "url": url,
            "domain": domain,
            "scan_type": "ports",
            "command": "nmap",
            "output": "\n".join(port_list) if port_list else "No open ports found",
            "ports": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Port scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/directories")
async def scan_directories(request: Request):
    """Directory enumeration scan endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        wordlist = data.get('wordlist', 'common')
        
        # Use the proper scan function
        result = run_dirsearch_scan(url, wordlist)
        
        # Format response for frontend
        if result and len(result) > 0 and 'error' in result[0]:
            return {
                "success": False,
                "url": url,
                "scan_type": "directories",
                "command": "dirsearch",
                "output": "",
                "error": result[0]['error']
            }
        
        # Format directories for display
        dir_list = []
        for dir_entry in result:
            if dir_entry.get('found'):
                dir_list.append(f"{dir_entry['url']} (Status: {dir_entry['status_code']}, Size: {dir_entry.get('size', 'N/A')})")
        
        return {
            "success": True,
            "url": url,
            "scan_type": "directories",
            "command": "dirsearch",
            "output": "\n".join(dir_list) if dir_list else "No directories found",
            "directories": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Directory scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/vulnerabilities")
async def scan_vulnerabilities(request: Request):
    """Vulnerability scanning endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        
        # Use the Python nikto wrapper instead of command executor
        result = run_nikto_scan(url)
        
        # Format the result to match expected frontend structure
        if result and 'error' in result[0] if result else {}:
            return {
                "success": False,
                "url": url,
                "scan_type": "vulnerabilities",
                "command": "nikto",
                "output": "",
                "error": result[0]['error'] if result else "Unknown error"
            }
        
        # Format vulnerabilities for display
        vuln_list = []
        for vuln in result:
            severity = vuln.get('severity', 'Unknown')
            vuln_type = vuln.get('type', 'Unknown')
            description = vuln.get('description', 'No description')
            vuln_list.append(f"[{severity}] {vuln_type}: {description}")
        
        return {
            "success": True,
            "url": url,
            "scan_type": "vulnerabilities",
            "command": "nikto",
            "output": "\n".join(vuln_list) if vuln_list else "No vulnerabilities detected",
            "vulnerabilities": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Vulnerability scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/technologies")
async def scan_technologies_endpoint(request: Request):
    """Technology detection endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        
        # Use the Python Wappalyzer library instead of command executor
        result = scan_technologies(url)
        
        # Format the result to match expected frontend structure
        if 'error' in result:
            return {
                "success": False,
                "url": url,
                "scan_type": "technologies",
                "command": "python-wappalyzer",
                "output": "",
                "error": result['error']
            }
        
        # Format technologies for display
        tech_list = []
        for tech_name, tech_info in result.get('technologies', {}).items():
            version_str = f" v{tech_info.get('version', '')}" if tech_info.get('version') else ""
            confidence_str = f" ({tech_info.get('confidence', 0)}%)" if tech_info.get('confidence') else ""
            tech_list.append(f"{tech_name}{version_str}{confidence_str}")
        
        return {
            "success": True,
            "url": url,
            "scan_type": "technologies",
            "command": "python-wappalyzer",
            "output": "\n".join(tech_list) if tech_list else "No technologies detected",
            "technologies": result.get('technologies', {}),
            "error": None
        }
    except Exception as e:
        logger.error(f"Technology scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/firewall")
async def scan_firewall_endpoint(request: Request):
    """WAF detection endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        
        # Use the proper scan function
        result = scan_firewall(url)
        
        # Format response for frontend
        if 'error' in result:
            return {
                "success": False,
                "url": url,
                "scan_type": "firewall",
                "command": "wafw00f",
                "output": "",
                "error": result['error']
            }
        
        # Format firewall info for display
        waf_info = result.get('waf_detection', {})
        output_lines = []
        if waf_info.get('detected'):
            output_lines.append(f"WAF Detected: {waf_info.get('waf_name', 'Unknown')}")
            output_lines.append(f"Confidence: {waf_info.get('confidence', 'Unknown')}")
        else:
            output_lines.append("No WAF detected")
        
        return {
            "success": True,
            "url": url,
            "scan_type": "firewall",
            "command": "wafw00f",
            "output": "\n".join(output_lines),
            "waf_detection": waf_info,
            "error": None
        }
    except Exception as e:
        logger.error(f"Firewall scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan/subdomains")
async def scan_subdomains_endpoint(request: Request):
    """Subdomain discovery endpoint"""
    try:
        data = await request.form()
        url = validate_url(data.get('url'))
        domain = get_domain_from_url(url)
        
        # Use the proper scan function
        result = run_subfinder_scan(domain)
        
        # Format response for frontend
        if result and len(result) > 0 and 'error' in result[0]:
            return {
                "success": False,
                "url": url,
                "domain": domain,
                "scan_type": "subdomains",
                "command": "subfinder",
                "output": "",
                "error": result[0]['error']
            }
        
        # Format subdomains for display
        subdomain_list = []
        for subdomain in result:
            subdomain_list.append(f"{subdomain['subdomain']}")
        
        return {
            "success": True,
            "url": url,
            "domain": domain,
            "scan_type": "subdomains",
            "command": "subfinder",
            "output": "\n".join(subdomain_list) if subdomain_list else "No subdomains found",
            "subdomains": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Subdomain scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/download-results")
async def download_results(request: Request):
    """Download scan results as formatted text file"""
    try:
        data = await request.json()
        results = data.get('results', {})
        scan_type = data.get('scan_type', 'all')
        
        # Generate formatted report
        report_content = generate_report(results, scan_type)
        
        # Save to temporary file
        filename = f"scan_results_{scan_type}_{int(time.time())}.txt"
        filepath = f"/tmp/{filename}"
        
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type='text/plain'
        )
        
    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error occurred"}
    )

# Add explicit OPTIONS handler for all routes
@app.options("/{path:path}")
async def options_handler(request: Request):
    """Handle OPTIONS requests for CORS preflight"""
    response = JSONResponse(content={"message": "OK"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, X-API-Key"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response

def generate_report(results: Dict[str, Any], scan_type: str) -> str:
    """Generate formatted text report"""
    import time
    
    report = f"""
{'='*80}
                    WEB SECURITY MATRIX SCAN REPORT
{'='*80}

Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Target URL: {results.get('url', 'N/A')}
Domain: {results.get('domain', 'N/A')}
Scan Type: {scan_type.upper()}
Environment: {settings.ENVIRONMENT}

{'='*80}
"""
    
    if scan_type in ['all', 'dns'] and 'dns' in results.get('results', {}):
        report += f"""
DNS INFORMATION
{'-'*40}
"""
        dns_data = results['results']['dns']
        if 'records' in dns_data:
            records = dns_data['records']
            report += f"A Records: {', '.join(records.get('A_records', []))}\n"
            report += f"AAAA Records: {', '.join(records.get('AAAA_records', []))}\n"
            report += f"MX Records: {', '.join(records.get('MX_records', []))}\n"
            report += f"NS Records: {', '.join(records.get('NS_records', []))}\n"
            report += f"TXT Records: {', '.join(records.get('TXT_records', []))}\n"
        elif 'error' in dns_data:
            report += f"DNS Error: {dns_data['error']}\n"
    
    if scan_type in ['all', 'ports'] and 'ports' in results.get('results', {}):
        report += f"""
OPEN PORTS
{'-'*40}
"""
        ports = results['results']['ports']
        if ports and not any('error' in str(p) for p in ports):
            for port in ports:
                report += f"Port {port['port']}/{port['protocol']}: {port['service']} (Open)\n"
        elif ports and 'error' in str(ports[0]):
            report += f"Port Scan Error: {ports[0]['error']}\n"
        else:
            report += "No open ports found.\n"
    
    if scan_type in ['all', 'directories'] and 'directories' in results.get('results', {}):
        report += f"""
DIRECTORY SCAN RESULTS
{'-'*40}
"""
        directories = results['results']['directories']
        if directories and not any('error' in str(d) for d in directories):
            for directory in directories:
                if directory.get('found', False):
                    report += f"Found: {directory['url']} (Status: {directory['status_code']})\n"
        elif directories and 'error' in str(directories[0]):
            report += f"Directory Scan Error: {directories[0]['error']}\n"
        else:
            report += "No directories found.\n"
    
    if scan_type in ['all', 'vulnerabilities'] and 'vulnerabilities' in results.get('results', {}):
        report += f"""
VULNERABILITY SCAN RESULTS
{'-'*40}
"""
        vulnerabilities = results['results']['vulnerabilities']
        if vulnerabilities and not any('error' in str(v) for v in vulnerabilities):
            for vuln in vulnerabilities:
                report += f"{vuln['type']} ({vuln['severity']}): {vuln['description']}\n"
        elif vulnerabilities and 'error' in str(vulnerabilities[0]):
            report += f"Vulnerability Scan Error: {vulnerabilities[0]['error']}\n"
        else:
            report += "No vulnerabilities detected.\n"
    
    if scan_type in ['all', 'technologies'] and 'technologies' in results.get('results', {}):
        report += f"""
TECHNOLOGY DETECTION RESULTS
{'-'*40}
"""
        technologies = results['results']['technologies']
        if 'technologies' in technologies and technologies['technologies']:
            for tech in technologies['technologies']:
                report += f"{tech['name']} ({tech['confidence']})\n"
        elif 'error' in technologies:
            report += f"Technology Scan Error: {technologies['error']}\n"
        else:
            report += "No technologies detected.\n"
    
    if scan_type in ['all', 'firewall'] and 'firewall' in results.get('results', {}):
        report += f"""
FIREWALL DETECTION RESULTS
{'-'*40}
"""
        firewall = results['results']['firewall']
        if 'waf_detection' in firewall:
            waf = firewall['waf_detection']
            if waf['detected']:
                report += f"WAF Detected: {waf['waf_name']} ({waf['confidence']})\n"
            else:
                report += f"No WAF detected ({waf['confidence']})\n"
        elif 'error' in firewall:
            report += f"Firewall Scan Error: {firewall['error']}\n"
    
    report += f"""
{'='*80}
Report generated by Web Security Matrix v3.0
For educational and authorized security testing purposes only.
Environment: {settings.ENVIRONMENT}
{'='*80}
"""
    
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )