import socket
from typing import Dict, Any
from tools import tool_manager

def scan_firewall(url: str) -> Dict[str, Any]:
    """Simple WAF detection"""
    try:
        # Check if wafw00f is available
        if not tool_manager.check_tool_availability('wafw00f'):
            # Use socket-based detection
            return detect_waf_socket(url)
        
        # Run simple wafw00f command
        success, stdout, stderr = tool_manager.run_command([
            'wafw00f', url, '-o', '/dev/stdout', '--no-color'
        ])
        
        if success:
            return parse_wafw00f_simple(stdout, url)
        else:
            return detect_waf_socket(url)
            
    except Exception as e:
        return detect_waf_socket(url)

def detect_waf_socket(url: str) -> Dict[str, Any]:
    """Simple WAF detection via response analysis"""
    import urllib.request
    import urllib.error
    
    try:
        # Parse domain from URL
        domain = url.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Make request and analyze response headers
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            headers = dict(response.headers)
        except urllib.error.HTTPError as e:
            headers = dict(e.headers)
        except:
            return {
                "waf_detection": {
                    "detected": False,
                    "waf_name": "Unknown",
                    "confidence": "Low",
                    "error": str(e)
                }
            }
        
        # Check for common WAF headers and patterns
        waf_indicators = []
        
        # Check headers
        server = headers.get('Server', '').lower()
        xPoweredBy = headers.get('X-Powered-By', '').lower()
        xWafInfo = headers.get('X-WAF-Info', '').lower()
        
        # Known WAF signatures
        if 'cloudflare' in server or 'cloudflare' in xPoweredBy:
            return {
                "waf_detection": {
                    "detected": True,
                    "waf_name": "Cloudflare",
                    "manufacturer": "Cloudflare",
                    "confidence": "High",
                    "evidence": [f"Server: {headers.get('Server', 'N/A')}"]
                }
            }
        
        if 'aws' in server or 'amazon' in server:
            return {
                "waf_detection": {
                    "detected": True,
                    "waf_name": "AWS WAF",
                    "manufacturer": "Amazon",
                    "confidence": "High",
                    "evidence": [f"Server: {headers.get('Server', 'N/A')}"]
                }
            }
        
        if 'waf' in server or 'waf' in xPoweredBy or 'waf' in xWafInfo:
            return {
                "waf_detection": {
                    "detected": True,
                    "waf_name": "WAF Detected",
                    "manufacturer": "Unknown",
                    "confidence": "Medium",
                    "evidence": [f"Server: {headers.get('Server', 'N/A')}"]
                }
            }
        
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "No WAF Detected",
                "manufacturer": "Unknown",
                "confidence": "Low",
                "evidence": [f"Server: {headers.get('Server', 'N/A')}"]
            }
        }
        
    except Exception as e:
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "Error",
                "confidence": "None",
                "error": str(e)
            }
        }

def parse_wafw00f_simple(output: str, url: str) -> Dict[str, Any]:
    """Simple WAF parsing"""
    output_lower = output.lower()
    
    if 'detected' in output_lower or 'waf' in output_lower:
        return {
            "waf_detection": {
                "detected": True,
                "waf_name": "WAF Detected",
                "confidence": "Medium",
                "output": output[:500]
            }
        }
    
    return {
        "waf_detection": {
            "detected": False,
            "waf_name": "No WAF Detected",
            "confidence": "Low",
            "output": output[:500]
        }
    }
