import requests
from typing import Dict, Any
from tools import tool_manager


def scan_firewall(url: str) -> Dict[str, Any]:
    """Scan for WAF using wafw00f or basic detection"""
    # Try using wafw00f if available
    if tool_manager.check_tool_availability('wafw00f'):
        success, stdout, stderr = tool_manager.run_command([
            'wafw00f', url, '-o', '/dev/stdout'
        ], timeout=30)
        
        if success or stdout:
            return parse_waf_output(stdout, url)
    
    # Fallback to basic WAF detection
    return basic_waf_detection(url)


def basic_waf_detection(url: str) -> Dict[str, Any]:
    """Basic WAF detection by checking headers and response"""
    waf_indicators = {
        'cloudflare': ['cf-ray', 'cf-cache-status', '__cfduid', 'cloudflare'],
        'akamai': ['akamai-origin-hop', 'akamai-x-cache'],
        'aws': ['x-amz-cf-id', 'x-amz-cf-pop'],
        'imperva': ['incapsula', 'imperva'],
        'sucuri': ['sucuri', 'x-sucuri'],
        'ddos-guard': ['ddos-guard'],
        'fastly': ['fastly-debug', 'x-served-by'],
        'incapsula': ['incapsula'],
        'stackpath': ['x-cache'],
        'cloudfront': ['x-amz-cf-id']
    }
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        headers = {k.lower(): v.lower() for k, v in response.headers.items()}
        
        # Check headers for WAF indicators
        for waf_name, indicators in waf_indicators.items():
            for indicator in indicators:
                if indicator in headers or indicator in response.text.lower():
                    return {
                        "waf_detection": {
                            "detected": True,
                            "waf_name": waf_name.title(),
                            "confidence": "High"
                        }
                    }
        
        # Check response status and content
        if response.status_code in [403, 405, 501]:
            return {
                "waf_detection": {
                    "detected": True,
                    "waf_name": "Generic WAF",
                    "confidence": "Medium"
                }
            }
        
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "No WAF",
                "confidence": "Low"
            }
        }
    except Exception as e:
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "Unknown",
                "confidence": "Low",
                "error": str(e)
            }
        }


def parse_waf_output(output: str, url: str) -> Dict[str, Any]:
    """Parse wafw00f output"""
    output_lower = output.lower()
    
    waf_names = {
        'cloudflare': 'Cloudflare',
        'aws': 'AWS WAF', 
        'akamai': 'Akamai',
        'imperva': 'Imperva',
        'incapsula': 'Incapsula',
        'sucuri': 'Sucuri',
        'fortiweb': 'FortiWeb',
        'bigip': 'BIG-IP',
        'barracuda': 'Barracuda',
        'modsecurity': 'ModSecurity'
    }
    
    for key, name in waf_names.items():
        if key in output_lower:
            return {
                "waf_detection": {
                    "detected": True,
                    "waf_name": name,
                    "confidence": "High"
                }
            }
    
    if 'waf' in output_lower or 'detected' in output_lower:
        return {
            "waf_detection": {
                "detected": True,
                "waf_name": "WAF Detected",
                "confidence": "Medium"
            }
        }
    
    return {
        "waf_detection": {
            "detected": False,
            "waf_name": "No WAF",
            "confidence": "Low"
        }
    }
