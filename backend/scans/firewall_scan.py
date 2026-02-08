import json
import logging
import tempfile
import os
from typing import Dict, Any, Optional
from tools import tool_manager
from .wafw00f_wrapper import WAFW00FWrapper

logger = logging.getLogger(__name__)

def scan_firewall(url: str) -> Dict[str, Any]:
    """Main function to scan for web application firewalls using WAFW00F"""
    try:
        # Check if wafw00f is available
        if not tool_manager.check_tool_availability('wafw00f'):
            return {
                "waf_detection": {
                    "detected": False,
                    "waf_name": "Not Available",
                    "manufacturer": "Unknown",
                    "confidence": "None",
                    "detection_method": "Tool not available",
                    "trigger_url": None,
                    "evidence": ["WAFW00F tool not available in this environment. Please use a platform that supports system packages or configure wafw00f manually."]
                },
                "headers_analysis": {},
                "evasion_results": [],
                "status": "error",
                "error": "WAFW00F tool not available in this environment"
            }
        
        wrapper = WAFW00FWrapper()
        return wrapper.scan_target(url)
    except Exception as e:
        return {
            "waf_detection": {
                "detected": False,
                "waf_name": "Error",
                "manufacturer": "Unknown",
                "confidence": "None",
                "detection_method": "Error",
                "trigger_url": None,
                "evidence": [f"WAFW00F scan error: {str(e)}"]
            },
            "headers_analysis": {},
            "evasion_results": [],
            "status": "error",
            "error": str(e)
        }
