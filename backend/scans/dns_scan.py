from typing import Dict, Any
from tools import tool_manager
import re

def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Run dnsrecon command"""
    if not tool_manager.check_tool_availability('dnsrecon'):
        return {"error": "dnsrecon not available"}
    
    success, stdout, stderr = tool_manager.run_command(
        ['dnsrecon', '-d', domain, '-t', 'std']
    )
    
    if success:
        return {
            "raw_output": stdout,
            "records": {
                "A_records": find_all_ips(stdout),
                "MX_records": find_all_domains(stdout),
                "NS_records": find_all_domains(stdout)
            }
        }
    else:
        return {"error": stderr, "raw_output": stdout}

def find_all_ips(text: str) -> list:
    """Find all IP addresses"""
    ips = set()
    for match in re.finditer(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', text):
        ip = match.group(1)
        if not ip.startswith('127.') and not ip.startswith('0.'):
            ips.add(ip)
    return list(ips)

def find_all_domains(text: str) -> list:
    """Find all domain-like patterns"""
    domains = set()
    for match in re.finditer(r'([a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,})', text):
        d = match.group(1)
        if '@' not in d and d not in domains:
            domains.add(d)
    return list(domains)
