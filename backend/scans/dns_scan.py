import re
import socket
from typing import Dict, List, Any
from tools import tool_manager

def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Get DNS information with simple command"""
    try:
        # Check if dnsrecon is available
        if not tool_manager.check_tool_availability('dnsrecon'):
            # Fallback to Python DNS
            return get_dns_python(domain)
        
        # Run simple dnsrecon command
        success, stdout, stderr = tool_manager.run_command(
            ['dnsrecon', '-d', domain, '-t', 'std', '--timeout', '30']
        )
        
        if success:
            records = parse_dnsrecon_simple(stdout)
            return {
                "raw_output": stdout,
                "records": records
            }
        else:
            # Fallback to Python DNS
            return get_dns_python(domain)
            
    except Exception as e:
        return get_dns_python(domain)

def get_dns_python(domain: str) -> Dict[str, Any]:
    """Fast Python DNS lookup"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    try:
        # A records
        ip = socket.gethostbyname(domain)
        records["A_records"].append(ip)
    except:
        pass
    
    return {
        "raw_output": "DNS lookup completed",
        "records": records
    }

def parse_dnsrecon_simple(output: str) -> Dict[str, List[str]]:
    """Simple DNS parsing"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    # Look for various formats
    for line in output.split('\n'):
        line = line.strip()
        
        # Simple IP extraction
        if 'A' in line and not 'AAAA' in line:
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            if ip_match and '127.0.0.1' not in line:
                if ip_match.group(1) not in records["A_records"]:
                    records["A_records"].append(ip_match.group(1))
        
        # MX records
        if 'MX' in line:
            mx_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]+)', line)
            if mx_match:
                mx = mx_match.group(1)
                if mx not in records["MX_records"] and '@' not in mx:
                    records["MX_records"].append(mx)
        
        # NS records
        if 'NS' in line and 'TXT' not in line:
            ns_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]+)', line)
            if ns_match:
                ns = ns_match.group(1)
                if ns not in records["NS_records"] and '@' not in ns:
                    records["NS_records"].append(ns)
    
    return records

def parse_dnsrecon_output(output: str) -> Dict[str, List[str]]:
    """Parse dnsrecon output"""
    return parse_dnsrecon_simple(output)
