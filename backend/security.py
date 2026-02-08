"""
Security utilities and middleware for Web Security Matrix API
"""
import re
import html
import logging
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import hashlib
import secrets

logger = logging.getLogger(__name__)


class InputValidator:
    """Input validation and sanitization"""
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input to prevent XSS attacks"""
        if not input_str:
            return ""
        
        # Remove any HTML/script tags
        sanitized = re.sub(r'<[^>]*>', '', input_str)
        
        # Remove javascript: protocol and other dangerous protocols
        sanitized = re.sub(r'^(javascript|data|vbscript|file):', '', sanitized, flags=re.IGNORECASE)
        
        # Remove any null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # HTML escape special characters
        sanitized = html.escape(sanitized)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_url(url: str) -> str:
        """Validate and normalize URL with XSS protection"""
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # First sanitize the input
        url = InputValidator.sanitize_input(url)
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Validate URL format
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.netloc:
                raise HTTPException(status_code=400, detail="Invalid URL format")
            
            # Additional validation: ensure the domain looks valid
            domain = parsed.netloc
            domain_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*(:[0-9]{1,5})?$')
            if not domain_pattern.match(domain):
                raise HTTPException(status_code=400, detail="Invalid domain format")
            
            return url
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")
    
    @staticmethod
    def validate_scan_options(options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate scan options"""
        valid_options = {}
        
        # Boolean options
        boolean_options = [
            'enable_dns', 'enable_ports', 'enable_technologies',
            'enable_firewall', 'enable_vulnerabilities', 'enable_directories'
        ]
        
        for option in boolean_options:
            value = options.get(option, False)
            if isinstance(value, str):
                valid_options[option] = value.lower() == 'true'
            else:
                valid_options[option] = bool(value)
        
        # Wordlist option
        wordlist = options.get('wordlist', 'common')
        valid_wordlists = ['common', 'fast', 'big', 'all']
        if wordlist not in valid_wordlists:
            valid_options['wordlist'] = 'common'
        else:
            valid_options['wordlist'] = wordlist
        
        return valid_options


# Global instances
rate_limiter = None  # Rate limiter not used in current implementation

def validate_and_sanitize_url(url: str) -> str:
    """Convenience function for URL validation"""
    return InputValidator.validate_url(url)

def sanitize_user_input(input_str: str) -> str:
    """Convenience function for input sanitization"""
    return InputValidator.sanitize_input(input_str)

def validate_scan_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for parameter validation"""
    return InputValidator.validate_scan_options(params)
