import socket
import dns.resolver
import dns.reversename
from typing import Dict, List, Any
from tools import tool_manager

def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Get DNS information with fast fallback"""
    try:
        # Try fast Python DNS first (always works)
        records = get_dns_records_fast(domain)
        return {
            "raw_output": "Fast DNS lookup completed",
            "records": records
        }
    except Exception as e:
        return {"error": f"DNS scan error: {str(e)}"}

def get_dns_records_fast(domain: str) -> Dict[str, List[str]]:
    """Fast DNS lookup using Python's dns.resolver"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    try:
        # A records
        try:
            answers = dns.resolver.resolve(domain, 'A')
            for rdata in answers:
                records["A_records"].append(str(rdata.address))
        except Exception:
            pass
        
        # AAAA records
        try:
            answers = dns.resolver.resolve(domain, 'AAAA')
            for rdata in answers:
                records["AAAA_records"].append(str(rdata.address))
        except Exception:
            pass
        
        # MX records
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            for rdata in answers:
                records["MX_records"].append(str(rdata.exchange))
        except Exception:
            pass
        
        # NS records
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            for rdata in answers:
                records["NS_records"].append(str(rdata.target).rstrip('.'))
        except Exception:
            pass
        
        # TXT records
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                records["TXT_records"].append(' '.join(rdata.strings))
        except Exception:
            pass
            
    except Exception as e:
        pass
    
    return records

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
            parts = line.split('\t')
            if len(parts) >= 2:
                ip_part = parts[1].strip()
                ip_parts = ip_part.split()
                if len(ip_parts) >= 3:
                    ip = ip_parts[-1]
                    records["A_records"].append(ip)
        elif '\t AAAA ' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                ip_part = parts[1].strip()
                ip_parts = ip_part.split()
                if len(ip_parts) >= 3:
                    ip = ip_parts[-1]
                    records["AAAA_records"].append(ip)
        elif '\t MX ' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                mx_part = parts[1].strip()
                mx_parts = mx_part.split()
                if len(mx_parts) >= 3:
                    mx = mx_parts[-1]
                    records["MX_records"].append(mx)
        elif '\t NS ' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                ns_part = parts[1].strip()
                ns_parts = ns_part.split()
                if len(ns_parts) >= 3:
                    ns = ns_parts[-1]
                    records["NS_records"].append(ns)
        elif '\t TXT ' in line:
            parts = line.split('\t')
            if len(parts) >= 2:
                txt_part = parts[1].strip()
                txt_parts = txt_part.split()
                if len(txt_parts) >= 3:
                    txt = ' '.join(txt_parts[2:])
                    records["TXT_records"].append(txt)
    
    return records
