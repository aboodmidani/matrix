import subprocess
import re
from typing import Dict, List, Any

def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Run dnsrecon command to get DNS information"""
    try:
        # Check if dnsrecon is available
        check_result = subprocess.run(
            ['which', 'dnsrecon'],
            capture_output=True,
            text=True
        )
        
        if check_result.returncode != 0:
            return {
                "error": "DNS scanning tool (dnsrecon) not available in this environment. Please use a platform that supports system packages or configure dnsrecon manually."
            }
        
        result = subprocess.run(
            ['dnsrecon', '-d', domain, '-t', 'std'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output = result.stdout
            dns_info = {
                "raw_output": output,
                "records": parse_dnsrecon_output(output)
            }
            return dns_info
        else:
            return {"error": f"DNS scan failed: {result.stderr}"}
            
    except subprocess.TimeoutExpired:
        return {"error": "DNS lookup timed out"}
    except Exception as e:
        return {"error": f"DNS scan error: {str(e)}"}

def parse_dnsrecon_output(output: str) -> Dict[str, List[str]]:
    """Parse dnsrecon output to extract DNS records"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if '\t A ' in line:
            # A records - format: \t A domain.com ip
            parts = line.split('\t')
            if len(parts) >= 2:
                # The IP is in the second part after splitting by tab
                ip_part = parts[1].strip()
                # Extract IP from "A domain.com ip" format
                ip_parts = ip_part.split()
                if len(ip_parts) >= 3:
                    ip = ip_parts[-1]
                    records["A_records"].append(ip)
        elif '\t AAAA ' in line:
            # AAAA records - format: \t AAAA domain.com ip
            parts = line.split('\t')
            if len(parts) >= 2:
                # The IP is in the second part after splitting by tab
                ip_part = parts[1].strip()
                # Extract IP from "AAAA domain.com ip" format
                ip_parts = ip_part.split()
                if len(ip_parts) >= 3:
                    ip = ip_parts[-1]
                    records["AAAA_records"].append(ip)
        elif '\t MX ' in line:
            # MX records - format: \t MX domain.com mailserver
            parts = line.split('\t')
            if len(parts) >= 2:
                # The mailserver is in the second part after splitting by tab
                mx_part = parts[1].strip()
                # Extract mailserver from "MX domain.com mailserver" format
                mx_parts = mx_part.split()
                if len(mx_parts) >= 3:
                    mx = mx_parts[-1]
                    records["MX_records"].append(mx)
        elif '\t NS ' in line:
            # NS records - format: \t NS domain.com nameserver
            parts = line.split('\t')
            if len(parts) >= 2:
                # The nameserver is in the second part after splitting by tab
                ns_part = parts[1].strip()
                # Extract nameserver from "NS domain.com nameserver" format
                ns_parts = ns_part.split()
                if len(ns_parts) >= 3:
                    ns = ns_parts[-1]
                    records["NS_records"].append(ns)
        elif '\t TXT ' in line:
            # TXT records - format: \t TXT domain.com "text"
            parts = line.split('\t')
            if len(parts) >= 2:
                # The text is in the second part after splitting by tab
                txt_part = parts[1].strip()
                # Extract text from "TXT domain.com text" format
                txt_parts = txt_part.split()
                if len(txt_parts) >= 3:
                    txt = ' '.join(txt_parts[2:])
                    records["TXT_records"].append(txt)
    
    return records
