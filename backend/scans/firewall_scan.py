import subprocess
import json
import logging
import tempfile
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WAFW00FWrapper:
    """Wrapper class for WAFW00F tool integration"""
    
    def __init__(self):
        self.tool_name = "WAFW00F"
        self.tool_version = "2.4.2"
    
    def scan_target(self, target_url: str) -> Dict[str, Any]:
        """
        Scan target URL using WAFW00F and return structured results
        
        Args:
            target_url (str): The URL to scan for WAF detection
            
        Returns:
            Dict[str, Any]: Structured scan results
        """
        try:
            # Create temporary file for JSON output
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_filename = temp_file.name
            
            try:
                # Run WAFW00F command with JSON output
                cmd = [
                    'wafw00f',
                    '-o', temp_filename,
                    '-f', 'json',
                    target_url
                ]
                
                logger.info(f"Running WAFW00F scan: {' '.join(cmd)}")
                
                # Execute the command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60  # 60 second timeout
                )
                
                # Check if command was successful
                if result.returncode != 0:
                    logger.error(f"WAFW00F scan failed: {result.stderr}")
                    return self._create_error_result(target_url, result.stderr)
                
                # Read and parse JSON output
                with open(temp_filename, 'r') as f:
                    wafw00f_output = json.load(f)
                
                # Process the results
                return self._process_wafw00f_output(target_url, wafw00f_output)
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
                    
        except subprocess.TimeoutExpired:
            logger.error(f"WAFW00F scan timed out for {target_url}")
            return self._create_error_result(target_url, "Scan timed out")
        except Exception as e:
            logger.error(f"WAFW00F scan error: {str(e)}")
            return self._create_error_result(target_url, str(e))
    
    def _process_wafw00f_output(self, target_url: str, wafw00f_output: list) -> Dict[str, Any]:
        """
        Process WAFW00F JSON output and convert to structured format
        
        Args:
            target_url (str): Original target URL
            wafw00f_output (list): WAFW00F JSON output
            
        Returns:
            Dict[str, Any]: Structured results
        """
        if not wafw00f_output or not isinstance(wafw00f_output, list):
            return self._create_error_result(target_url, "Invalid WAFW00F output")
        
        # Get the first (and usually only) result
        result_data = wafw00f_output[0]
        
        # Create structured response
        structured_result = {
            'url': target_url,
            'timestamp': result_data.get('timestamp', 0),
            'waf_detection': {
                'detected': result_data.get('detected', False),
                'waf_name': result_data.get('firewall', 'None'),
                'manufacturer': result_data.get('manufacturer', 'Unknown'),
                'confidence': 'High' if result_data.get('detected', False) else 'None',
                'detection_method': 'WAFW00F analysis',
                'trigger_url': result_data.get('trigger_url', None),
                'evidence': []
            },
            'headers_analysis': {},
            'evasion_results': [],
            'status': 'success' if not result_data.get('detected', False) or result_data.get('firewall') != 'None' else 'failed',
            'tool_info': {
                'name': self.tool_name,
                'version': self.tool_version,
                'output_format': 'JSON'
            }
        }
        
        # Add evidence if WAF was detected
        if result_data.get('detected', False) and result_data.get('firewall') != 'None':
            structured_result['waf_detection']['evidence'].append(
                f"WAFW00F detected {result_data.get('firewall')} firewall"
            )
            if result_data.get('manufacturer'):
                structured_result['waf_detection']['evidence'].append(
                    f"Manufacturer: {result_data.get('manufacturer')}"
                )
        
        return structured_result
    
    def _create_error_result(self, target_url: str, error_message: str) -> Dict[str, Any]:
        """Create error result structure"""
        return {
            'url': target_url,
            'timestamp': 0,
            'waf_detection': {
                'detected': False,
                'waf_name': 'Error',
                'manufacturer': 'Unknown',
                'confidence': 'None',
                'detection_method': 'Error',
                'trigger_url': None,
                'evidence': [f"WAFW00F scan failed: {error_message}"]
            },
            'headers_analysis': {},
            'evasion_results': [],
            'status': 'error',
            'error': error_message,
            'tool_info': {
                'name': self.tool_name,
                'version': self.tool_version
            }
        }

def scan_firewall(url: str) -> Dict[str, Any]:
    """Main function to scan for web application firewalls using WAFW00F"""
    wrapper = WAFW00FWrapper()
    return wrapper.scan_target(url)

def get_firewall_report(url: str) -> Dict[str, Any]:
    """Get a detailed WAFW00F detection report"""
    wrapper = WAFW00FWrapper()
    scan_result = wrapper.scan_target(url)
    
    report = {
        'summary': {
            'waf_detected': scan_result.get('waf_detection', {}).get('detected', False),
            'waf_name': scan_result.get('waf_detection', {}).get('waf_name', 'None'),
            'manufacturer': scan_result.get('waf_detection', {}).get('manufacturer', 'Unknown'),
            'confidence': scan_result.get('waf_detection', {}).get('confidence', 'None'),
            'tool_used': scan_result.get('tool_info', {}).get('name', 'WAFW00F')
        },
        'detailed_results': scan_result,
        'recommendations': wrapper._generate_recommendations(scan_result)
    }
    
    return report

def _generate_recommendations(self, scan_results: Dict[str, Any]) -> list:
    """Generate security recommendations based on WAFW00F detection"""
    recommendations = []
    
    waf_detection = scan_results.get('waf_detection', {})
    
    if waf_detection.get('detected', False):
        waf_name = waf_detection.get('waf_name', 'Unknown')
        manufacturer = waf_detection.get('manufacturer', 'Unknown')
        recommendations.append(f"WAF detected: {waf_name} by {manufacturer}")
        recommendations.append("Ensure WAF rules are properly configured and updated")
        recommendations.append("Regularly test WAF effectiveness against new attack vectors")
    else:
        recommendations.append("No WAF detected - Consider implementing web application firewall protection")
        recommendations.append("Implement rate limiting and DDoS protection")
        recommendations.append("Add security headers and input validation")
    
    return recommendations
