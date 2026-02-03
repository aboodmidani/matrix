from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import subprocess
import json
import os
import re
import time
from urllib.parse import urlparse
from scans.dns_scan import run_dnsrecon
from scans.port_scan import run_nmap_scan
from scans.directory_scan import run_dirsearch_scan
from scans.vulnerability_scan import run_nikto_scan
from scans.technology_scan import scan_technologies
from scans.firewall_scan import scan_firewall

# Get CORS origins from environment variable
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

app = FastAPI(title="Web Security Audit API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(',') if CORS_ORIGINS else ["http://localhost:5173", "https://matrix-audit.netlify.app"],
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
    
    # Basic URL validation
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Validate URL format
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Get scan options
    enable_dns = data.get('enable_dns', 'false') == 'true'
    enable_ports = data.get('enable_ports', 'false') == 'true'
    enable_technologies = data.get('enable_technologies', 'false') == 'true'
    enable_firewall = data.get('enable_firewall', 'false') == 'true'
    enable_vulns = data.get('enable_vulns', 'false') == 'true'
    enable_directories = data.get('enable_directories', 'false') == 'true'
    wordlist = data.get('wordlist', 'common')
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        results = {
            "url": url,
            "domain": domain,
        }
        
        # DNS Scan
        if enable_dns:
            try:
                dns_result = run_dnsrecon(domain)
                results["dns"] = dns_result
            except Exception as e:
                results["dns"] = {"error": f"DNS scan failed: {str(e)}"}
        
        # Port Scan
        if enable_ports:
            try:
                port_result = run_nmap_scan(domain)
                # Only add to results if there are actual ports or errors
                if port_result and not (len(port_result) == 1 and 'error' in port_result[0]):
                    results["ports"] = port_result
                else:
                    results["ports"] = port_result
            except Exception as e:
                results["ports"] = [{"error": f"Port scan failed: {str(e)}"}]
        
        # Directory Scan
        if enable_directories:
            try:
                dir_result = run_dirsearch_scan(url, wordlist)
                results["directories"] = dir_result
            except Exception as e:
                results["directories"] = [{"error": f"Directory scan failed: {str(e)}"}]
        
        # Vulnerability Scan
        if enable_vulns:
            try:
                vuln_result = run_nikto_scan(url)
                results["vulnerabilities"] = vuln_result
            except Exception as e:
                results["vulnerabilities"] = [{"error": f"Vulnerability scan failed: {str(e)}"}]
        
        # Technology Scan (Manual)
        if enable_technologies:
            try:
                tech_result = scan_technologies(url)
                # Only add to results if there are actual technologies or errors
                if tech_result and not (tech_result.get('technologies') == {} and 'error' not in tech_result):
                    results["technologies"] = tech_result
                else:
                    results["technologies"] = tech_result
            except Exception as e:
                results["technologies"] = {"error": f"Technology scan failed: {str(e)}"}
        else:
            results["technologies"] = {"error": "Technology scan disabled"}
        
        # Firewall Scan (Manual)
        if enable_firewall:
            try:
                firewall_result = scan_firewall(url)
                # Only add to results if there are actual results or errors
                if firewall_result and not (firewall_result.get('waf_detection', {}).get('detected') == False and 'error' not in firewall_result):
                    results["firewall"] = firewall_result
                else:
                    results["firewall"] = firewall_result
            except Exception as e:
                results["firewall"] = {"error": f"Firewall scan failed: {str(e)}"}
        else:
            results["firewall"] = {"error": "Firewall scan disabled"}
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/download-results")
async def download_results(request: Request):
    """Download scan results as formatted text file"""
    data = await request.json()
    results = data.get('results', {})
    scan_type = data.get('scan_type', 'all')
    
    try:
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
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error occurred"}
    )

def generate_report(results: dict, scan_type: str) -> str:
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

{'='*80}
"""
    
    if scan_type in ['all', 'dns'] and 'dns' in results:
        report += f"""
DNS INFORMATION
{'-'*40}
"""
        dns_data = results['dns']
        if 'records' in dns_data:
            records = dns_data['records']
            report += f"A Records: {', '.join(records.get('A_records', []))}\n"
            report += f"AAAA Records: {', '.join(records.get('AAAA_records', []))}\n"
            report += f"MX Records: {', '.join(records.get('MX_records', []))}\n"
            report += f"NS Records: {', '.join(records.get('NS_records', []))}\n"
            report += f"TXT Records: {', '.join(records.get('TXT_records', []))}\n"
        elif 'error' in dns_data:
            report += f"DNS Error: {dns_data['error']}\n"
    
    if scan_type in ['all', 'ports'] and 'ports' in results:
        report += f"""
OPEN PORTS
{'-'*40}
"""
        ports = results['ports']
        if ports and not any('error' in str(p) for p in ports):
            for port in ports:
                report += f"Port {port['port']}/{port['protocol']}: {port['service']} (Open)\n"
        elif ports and 'error' in str(ports[0]):
            report += f"Port Scan Error: {ports[0]['error']}\n"
        else:
            report += "No open ports found.\n"
    
    if scan_type in ['all', 'directories'] and 'directories' in results:
        report += f"""
DIRECTORY SCAN RESULTS
{'-'*40}
"""
        directories = results['directories']
        if directories and not any('error' in str(d) for d in directories):
            for directory in directories:
                if directory.get('found', False):
                    report += f"Found: {directory['url']} (Status: {directory['status_code']})\n"
        elif directories and 'error' in str(directories[0]):
            report += f"Directory Scan Error: {directories[0]['error']}\n"
        else:
            report += "No directories found.\n"
    
    if scan_type in ['all', 'vulnerabilities'] and 'vulnerabilities' in results:
        report += f"""
VULNERABILITY SCAN RESULTS
{'-'*40}
"""
        vulnerabilities = results['vulnerabilities']
        if vulnerabilities and not any('error' in str(v) for v in vulnerabilities):
            for vuln in vulnerabilities:
                report += f"{vuln['type']} ({vuln['severity']}): {vuln['description']}\n"
        elif vulnerabilities and 'error' in str(vulnerabilities[0]):
            report += f"Vulnerability Scan Error: {vulnerabilities[0]['error']}\n"
        else:
            report += "No vulnerabilities detected.\n"
    
    if scan_type in ['all', 'technologies'] and 'technologies' in results:
        report += f"""
TECHNOLOGY DETECTION RESULTS
{'-'*40}
"""
        technologies = results['technologies']
        if 'technologies' in technologies and technologies['technologies']:
            for tech in technologies['technologies']:
                report += f"{tech['name']} ({tech['confidence']})\n"
        elif 'error' in technologies:
            report += f"Technology Scan Error: {technologies['error']}\n"
        else:
            report += "No technologies detected.\n"
    
    if scan_type in ['all', 'firewall'] and 'firewall' in results:
        report += f"""
FIREWALL DETECTION RESULTS
{'-'*40}
"""
        firewall = results['firewall']
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
Report generated by Web Security Matrix
For educational and authorized security testing purposes only.
{'='*80}
"""
    
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)