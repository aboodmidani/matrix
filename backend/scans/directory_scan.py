import subprocess
from typing import Dict, List, Any
from tools import tool_manager
from config import settings

def run_dirsearch_scan(url: str, wordlist: str = "common") -> List[Dict[str, Any]]:
    """Run dirsearch command to scan directories"""
    try:
        # Check if dirsearch is available
        if not tool_manager.check_tool_availability('dirsearch'):
            return [{
                "error": "Directory scanning tool (dirsearch) not available in this environment. Please use a platform that supports system packages or configure dirsearch manually."
            }]
        
        # Map wordlist names to actual file paths
        wordlist_path = settings.WORDLISTS.get(wordlist, settings.WORDLISTS["common"])
        
        success, stdout, stderr = tool_manager.run_command([
            'dirsearch', '-u', url, '-w', wordlist_path, '-t', '50', 
            '-o', '/tmp/dirsearch_results.txt'
        ])
        
        if success:
            results = parse_dirsearch_output(stdout)
            return results
        else:
            return [{"error": f"Directory scan failed: {stderr}"}]
            
    except subprocess.TimeoutExpired:
        return [{"error": "Directory scan timed out"}]
    except Exception as e:
        return [{"error": f"Directory scan error: {str(e)}"}]

def parse_dirsearch_output(output: str) -> List[Dict[str, Any]]:
    """Parse dirsearch output to extract found directories"""
    results = []
    
    lines = output.split('\n')
    for line in lines:
        if '[+]' in line and 'Code:' in line:
            # Parse line like: "[+] https://example.com/admin | Code: 200 | Size: 1234"
            parts = line.split('|')
            if len(parts) >= 3:
                url_part = parts[0].replace('[+]', '').strip()
                code_part = parts[1].replace('Code:', '').strip()
                size_part = parts[2].replace('Size:', '').strip()
                
                result_data = {
                    "url": url_part,
                    "status_code": int(code_part),
                    "size": int(size_part),
                    "found": True
                }
                results.append(result_data)
    
    return results
