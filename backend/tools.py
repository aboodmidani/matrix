import subprocess
import json
import tempfile
import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from config import settings

logger = logging.getLogger(__name__)

class ToolManager:
    """Manager for CLI tool operations and validation"""
    
    def __init__(self):
        self.tools = {
            'dirsearch': {
                'command': 'dirsearch',
                'required': False,
                'description': 'Directory enumeration tool'
            },
            'nikto': {
                'command': 'nikto',
                'required': False,
                'description': 'Web vulnerability scanner'
            },
            'nmap': {
                'command': 'nmap',
                'required': False,
                'description': 'Network scanner'
            },
            'dnsrecon': {
                'command': 'dnsrecon',
                'required': False,
                'description': 'DNS reconnaissance tool'
            },
            'wafw00f': {
                'command': 'wafw00f',
                'required': False,
                'description': 'WAF detection tool'
            }
        }
    
    def check_tool_availability(self, tool_name: str) -> bool:
        """Check if a tool is available in the system"""
        try:
            result = subprocess.run(
                ['which', self.tools[tool_name]['command']],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Failed to check {tool_name} availability: {e}")
            return False
    
    def run_command(self, command: List[str], timeout: Optional[int] = None) -> Tuple[bool, str, str]:
        """
        Run a command and return success status, stdout, and stderr
        
        Returns:
            Tuple of (success: bool, stdout: str, stderr: str)
        """
        if timeout is None:
            timeout = settings.SCAN_TIMEOUT
            
        try:
            logger.info(f"Executing command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
            
            if success:
                logger.info(f"Command completed successfully: {' '.join(command)}")
            else:
                logger.warning(f"Command failed with return code {result.returncode}: {' '.join(command)}")
                logger.warning(f"Stderr: {stderr}")
            
            return success, stdout, stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds: {' '.join(command)}")
            return False, "", f"Command timed out after {timeout} seconds"
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return False, "", str(e)

tool_manager = ToolManager()