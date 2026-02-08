import logging
from typing import Dict, Any, Optional
from wappalyzer import analyze

logger = logging.getLogger(__name__)

class WappalyzerWrapper:
    """Wrapper class for Wappalyzer tool integration"""
    
    def __init__(self):
        self.tool_name = "Wappalyzer"
        self.tool_version = "1.0.20"
    
    def scan_target(self, target_url: str) -> Dict[str, Any]:
        """
        Scan target URL using Wappalyzer and return structured results
        
        Args:
            target_url (str): The URL to scan for technology detection
            
        Returns:
            Dict[str, Any]: Structured scan results
        """
        try:
            logger.info(f"Running Wappalyzer scan for: {target_url}")
            
            # Use Wappalyzer analyze function
            wappalyzer_output = analyze(target_url)
            
            # Process the results
            return self._process_wappalyzer_output(target_url, wappalyzer_output)
            
        except Exception as e:
            logger.error(f"Wappalyzer scan error: {str(e)}")
            return self._create_error_result(target_url, str(e))
    
    def _process_wappalyzer_output(self, target_url: str, wappalyzer_output: dict) -> Dict[str, Any]:
        """
        Process Wappalyzer output and convert to structured format
        
        Args:
            target_url (str): Original target URL
            wappalyzer_output (dict): Wappalyzer output
            
        Returns:
            Dict[str, Any]: Structured results
        """
        if not wappalyzer_output or target_url not in wappalyzer_output:
            return self._create_error_result(target_url, "No technologies detected")
        
        # Get technologies for the target URL
        technologies_data = wappalyzer_output[target_url]
        
        # Create structured response
        structured_result = {
            'url': target_url,
            'timestamp': 0,  # Wappalyzer doesn't provide timestamp
            'technologies': {},
            'status': 'success',
            'tool_info': {
                'name': self.tool_name,
                'version': self.tool_version,
                'output_format': 'dict'
            }
        }
        
        # Process each detected technology
        for tech_name, tech_details in technologies_data.items():
            structured_result['technologies'][tech_name] = {
                'version': tech_details.get('version', ''),
                'confidence': tech_details.get('confidence', 0),
                'categories': tech_details.get('categories', []),
                'groups': tech_details.get('groups', [])
            }
        
        return structured_result
    
    def _create_error_result(self, target_url: str, error_message: str) -> Dict[str, Any]:
        """Create error result structure"""
        return {
            'url': target_url,
            'timestamp': 0,
            'technologies': {},
            'status': 'error',
            'error': error_message,
            'tool_info': {
                'name': self.tool_name,
                'version': self.tool_version
            }
        }

def scan_technologies(url: str) -> Dict[str, Any]:
    """Main function to scan for technologies using Wappalyzer"""
    wrapper = WappalyzerWrapper()
    return wrapper.scan_target(url)

