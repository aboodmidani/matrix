import subprocess
import json
import os
from typing import Dict, Any, List
from urllib.parse import urlparse

class CommandExecutor:
    def __init__(self, commands_file: str = "commands.json"):
        self.commands_file = commands_file
        self.commands = self.load_commands()
    
    def load_commands(self) -> Dict[str, Any]:
        """Load commands from JSON configuration file"""
        try:
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
    
    def get_domain_from_url(self, url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc
    
    def execute_command(self, scan_type: str, url: str) -> Dict[str, Any]:
        """Execute scan command and return results"""
        if scan_type not in self.commands:
            return {
                "error": f"Scan type '{scan_type}' not configured",
                "url": url,
                "scan_type": scan_type
            }
        
        command_config = self.commands[scan_type]
        command_template = command_config["command"]
        
        # Replace placeholders in command
        domain = self.get_domain_from_url(url)
        command = command_template.replace("{url}", url).replace("{domain}", domain)
        
        try:
            # Execute command
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "url": url,
                    "scan_type": scan_type,
                    "command": command,
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else None
                }
            else:
                return {
                    "success": False,
                    "url": url,
                    "scan_type": scan_type,
                    "command": command,
                    "output": result.stdout,
                    "error": result.stderr or f"Command failed with exit code {result.returncode}"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "url": url,
                "scan_type": scan_type,
                "command": command,
                "output": "",
                "error": "Command timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "scan_type": scan_type,
                "command": command,
                "output": "",
                "error": f"Command execution failed: {str(e)}"
            }

# Create global instance
command_executor = CommandExecutor()