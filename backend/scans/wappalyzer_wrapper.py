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

def get_technology_report(url: str) -> Dict[str, Any]:
    """Get a detailed technology detection report"""
    wrapper = WappalyzerWrapper()
    scan_result = wrapper.scan_target(url)
    
    report = {
        'summary': {
            'technologies_detected': len(scan_result.get('technologies', {})),
            'tool_used': scan_result.get('tool_info', {}).get('name', 'Wappalyzer')
        },
        'detailed_results': scan_result,
        'recommendations': wrapper._generate_recommendations(scan_result)
    }
    
    return report

def _generate_recommendations(self, scan_results: Dict[str, Any]) -> list:
    """Generate security recommendations based on technology detection"""
    recommendations = []
    
    technologies = scan_results.get('technologies', {})
    
    if technologies:
        recommendations.append(f"Detected {len(technologies)} technologies on the target")
        recommendations.append("Review each technology for known vulnerabilities")
        recommendations.append("Ensure all detected technologies are up to date")
        
        # Check for specific technologies that might need attention
        tech_names = [tech.lower() for tech in technologies.keys()]
        
        if any('wordpress' in name for name in tech_names):
            recommendations.append("WordPress detected - check for outdated plugins and themes")
        
        if any('php' in name for name in tech_names):
            recommendations.append("PHP detected - verify PHP version and security settings")
        
        if any('apache' in name or 'nginx' in name for name in tech_names):
            recommendations.append("Web server detected - review server configuration")
    else:
        recommendations.append("No technologies detected - consider using more comprehensive scanning")
    
    return recommendations