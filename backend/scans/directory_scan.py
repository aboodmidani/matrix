import subprocess
from typing import Dict, List, Any

def run_dirsearch_scan(url: str, wordlist: str = "common") -> List[Dict[str, Any]]:
    """Run dirsearch command to scan directories"""
    try:
        # Check if dirsearch is available
        check_result = subprocess.run(
            ['which', 'dirsearch'],
            capture_output=True,
            text=True
        )
        
        if check_result.returncode != 0:
            return [{
                "error": "Directory scanning tool (dirsearch) not available in this environment. Please use a platform that supports system packages or configure dirsearch manually."
            }]
        
        # Map wordlist names to actual file paths
        wordlist_map = {
            "common": "/usr/share/dirb/wordlists/common.txt",
            "fast": "/usr/share/dirb/wordlists/small.txt",
            "big": "/usr/share/dirb/wordlists/big.txt",
            "all": "/usr/share/dirb/wordlists/vulns/cgis.txt"
        }
        
        wordlist_path = wordlist_map.get(wordlist, wordlist_map["common"])
        
        result = subprocess.run(
            ['dirsearch', '-u', url, '-w', wordlist_path, '-t', '50', '--plain-text-report', '/tmp/dirsearch_results.txt'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            output = result.stdout
            results = parse_dirsearch_output(output)
            return results
        else:
            return [{"error": f"Directory scan failed: {result.stderr}"}]
            
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