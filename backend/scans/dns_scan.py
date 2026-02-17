import re
import socket
from typing import Dict, Any, List
from tools import tool_manager


def run_dnsrecon(domain: str) -> Dict[str, Any]:
    """Run dnsrecon command"""
    if not tool_manager.check_tool_availability('dnsrecon'):
        # Fallback to basic DNS lookup
        return basic_dns_lookup(domain)
    
    success, stdout, stderr = tool_manager.run_command(
        ['dnsrecon', '-d', domain, '-t', 'std'], timeout=60
    )
    
    if success:
        return parse_dns_output(stdout, domain)
    else:
        # Fallback to basic DNS lookup on failure
        return basic_dns_lookup(domain)


def basic_dns_lookup(domain: str) -> Dict[str, Any]:
    """Basic DNS lookup using socket module"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    try:
        # A record
        ip = socket.gethostbyname(domain)
        if ip:
            records["A_records"].append(ip)
    except:
        pass
    
    try:
        # MX records
        mx_records = socket.gethostbyname_ex(domain)
        # gethostbyname_ex returns (hostname, aliaslist, ipaddrlist)
        for ip in mx_records[2]:
            if ':' not in ip:  # IPv4
                records["A_records"].append(ip)
    except:
        pass
    
    return {"records": records, "raw_output": ""}


def parse_dns_output(text: str, domain: str) -> Dict[str, Any]:
    """Parse dnsrecon output"""
    records = {
        "A_records": [],
        "AAAA_records": [],
        "MX_records": [],
        "NS_records": [],
        "TXT_records": []
    }
    
    for line in text.split('\n'):
        line = line.strip()
        
        # A records
        if 'A' in line and domain in line:
            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            if match and not match.group(1).startswith('127.'):
                ip = match.group(1)
                if ip not in records["A_records"]:
                    records["A_records"].append(ip)
        
        # AAAA records (IPv6)
        if 'AAAA' in line:
            match = re.search(r'([a-fA-F0-9:]+:+[a-fA-F0-9:]+)', line)
            if match:
                records["AAAA_records"].append(match.group(1))
        
        # MX records
        if 'MX' in line:
            match = re.search(r'(\S+\.' + re.escape(domain) + ')', line)
            if match:
                mx = match.group(1)
                if mx not in records["MX_records"]:
                    records["MX_records"].append(mx)
        
        # NS records
        if 'NS' in line:
            match = re.search(r'(\S+\.' + re.escape(domain) + ')', line)
            if match:
                ns = match.group(1)
                if ns not in records["NS_records"]:
                    records["NS_records"].append(ns)
    
    return {"records": records, "raw_output": text}
