from typing import Dict, Any
from tools import tool_manager

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
                "A_records": extract_ips(stdout),
                "MX_records": extract_mx(stdout),
                "NS_records": extract_ns(stdout)
            }
        }
    else:
        return {"error": stderr}

def extract_ips(output: str) -> list:
    """Extract IP addresses from output"""
    import re
    ips = []
    for line in output.split('\n'):
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if match and match.group(1) != '127.0.0.1':
            if match.group(1) not in ips:
                ips.append(match.group(1))
    return ips

def extract_mx(output: str) -> list:
    """Extract MX records from output"""
    import re
    mx = []
    for line in output.split('\n'):
        if 'MX' in line:
            match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]+)', line)
            if match and '@' not in match.group(1):
                if match.group(1) not in mx:
                    mx.append(match.group(1))
    return mx

def extract_ns(output: str) -> list:
    """Extract NS records from output"""
    import re
    ns = []
    for line in output.split('\n'):
        if ' NS ' in line or '\tNS' in line:
            match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]+)', line)
            if match and '@' not in match.group(1):
                if match.group(1) not in ns:
                    ns.append(match.group(1))
    return ns
