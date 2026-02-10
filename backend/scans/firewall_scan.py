from typing import Dict, Any
from tools import tool_manager

def scan_firewall(url: str) -> Dict[str, Any]:
    """Run wafw00f command"""
    if not tool_manager.check_tool_availability('wafw00f'):
        return {"error": "wafw00f not available"}
    
    success, stdout, stderr = tool_manager.run_command([
        'wafw00f', url, '-o', '/dev/stdout'
    ])
    
    if success or 'WAF' in stdout or 'detected' in stdout:
        return parse_waf_output(stdout, url)
    else:
        return {"error": stderr}

def parse_waf_output(output: str, url: str) -> Dict[str, Any]:
    """Parse wafw00f output"""
    output_lower = output.lower()
    
    if 'cloudflare' in output_lower:
        return {
            "waf_detection": {
                "detected": True,
                "waf_name": "Cloudflare",
                "confidence": "High"
            }
        }
    elif 'aws' in output_lower or 'amazon' in output_lower:
        return {
            "waf_detection": {
                "detected": True,
                "waf_name": "AWS WAF",
                "confidence": "High"
            }
        }
    elif 'waf' in output_lower or 'detected' in output_lower:
        return {
            "waf_detection": {
                "detected": True,
                "waf_name": "WAF Detected",
                "confidence": "Medium"
            }
        }
    else:
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "No WAF",
                "confidence": "Low"
            }
        }
