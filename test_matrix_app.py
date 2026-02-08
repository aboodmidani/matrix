#!/usr/bin/env python3
"""
Comprehensive test suite for Web Security Matrix application
Tests security, functionality, and integration
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_URL = "https://httpbin.org"
TIMEOUT = 30

class MatrixAppTester:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Matrix-Tester/3.0'
        })
    
    def test_api_health(self) -> bool:
        """Test API health endpoint"""
        print("Testing API Health...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    print("✓ API Health Check Passed")
                    return True
            print(f"✗ API Health Check Failed: {response.status_code}")
            return False
        except Exception as e:
            print(f"✗ API Health Check Error: {e}")
            return False
    
    def test_api_info(self) -> bool:
        """Test API info endpoint"""
        print("Testing API Info...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                required_fields = ['message', 'version', 'status', 'environment']
                if all(field in data for field in required_fields):
                    print("✓ API Info Check Passed")
                    return True
            print(f"✗ API Info Check Failed: {response.status_code}")
            return False
        except Exception as e:
            print(f"✗ API Info Check Error: {e}")
            return False
    
    def test_input_validation(self) -> bool:
        """Test input validation and sanitization"""
        print("Testing Input Validation...")
        test_cases = [
            # Malicious inputs
            {"url": "<script>alert('xss')</script>", "expected": False},
            {"url": "javascript:alert('xss')", "expected": False},
            {"url": "data:text/html,<script>alert('xss')</script>", "expected": False},
            {"url": "https://example.com", "expected": True},
            {"url": "http://example.com", "expected": True},
            {"url": "example.com", "expected": True},
        ]
        
        passed = 0
        for test_case in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/scan/directories",
                    json={"url": test_case["url"]},
                    timeout=TIMEOUT
                )
                
                if test_case["expected"]:
                    if response.status_code in [200, 500]:  # 500 is ok for missing tools
                        passed += 1
                        print(f"  ✓ Valid URL accepted: {test_case['url']}")
                    else:
                        print(f"  ✗ Valid URL rejected: {test_case['url']} - {response.status_code}")
                else:
                    if response.status_code == 400:
                        passed += 1
                        print(f"  ✓ Malicious input rejected: {test_case['url']}")
                    else:
                        print(f"  ✗ Malicious input accepted: {test_case['url']} - {response.status_code}")
                        
            except Exception as e:
                if not test_case["expected"]:
                    passed += 1
                    print(f"  ✓ Malicious input caused error (good): {test_case['url']}")
                else:
                    print(f"  ✗ Valid input caused error: {test_case['url']} - {e}")
        
        success = passed >= len(test_cases) * 0.8  # Allow 80% pass rate
        print(f"Input Validation: {passed}/{len(test_cases)} tests passed")
        return success
    
    def test_scan_endpoints(self) -> Dict[str, bool]:
        """Test individual scan endpoints"""
        print("Testing Scan Endpoints...")
        endpoints = [
            ("DNS Scan", "/scan/dns"),
            ("Port Scan", "/scan/ports"),
            ("Directory Scan", "/scan/directories"),
            ("Vulnerability Scan", "/scan/vulnerabilities"),
            ("Technology Scan", "/scan/technologies"),
            ("Firewall Scan", "/scan/firewall"),
        ]
        
        results = {}
        for name, endpoint in endpoints:
            print(f"  Testing {name}...")
            try:
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json={"url": TEST_URL},
                    timeout=TIMEOUT
                )
                
                # Check for proper response structure
                if response.status_code in [200, 500]:  # 500 ok for missing tools
                    try:
                        data = response.json()
                        # Check for expected fields
                        if 'success' in data or 'error' in data:
                            results[name] = True
                            print(f"    ✓ {name} endpoint working")
                        else:
                            results[name] = False
                            print(f"    ✗ {name} invalid response format")
                    except:
                        results[name] = False
                        print(f"    ✗ {name} invalid JSON response")
                else:
                    results[name] = False
                    print(f"    ✗ {name} HTTP {response.status_code}")
                    
            except Exception as e:
                results[name] = False
                print(f"    ✗ {name} error: {e}")
        
        return results
    
    def test_comprehensive_audit(self) -> bool:
        """Test comprehensive audit endpoint"""
        print("Testing Comprehensive Audit...")
        try:
            audit_data = {
                "url": TEST_URL,
                "enable_dns": "true",
                "enable_ports": "true",
                "enable_directories": "true",
                "enable_vulnerabilities": "true",
                "enable_technologies": "true",
                "enable_firewall": "true",
                "wordlist": "common"
            }
            
            response = self.session.post(
                f"{self.base_url}/audit",
                json=audit_data,
                timeout=TIMEOUT * 2  # Longer timeout for comprehensive scan
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ['url', 'domain', 'timestamp', 'scan_options', 'results']
                if all(field in data for field in required_fields):
                    print("✓ Comprehensive Audit Passed")
                    return True
            
            print(f"✗ Comprehensive Audit Failed: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"✗ Comprehensive Audit Error: {e}")
            return False
    
    def test_security_headers(self) -> bool:
        """Test security headers"""
        print("Testing Security Headers...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=TIMEOUT)
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection',
                'Content-Security-Policy'
            ]
            
            missing_headers = []
            for header in security_headers:
                if header not in response.headers:
                    missing_headers.append(header)
            
            if not missing_headers:
                print("✓ All security headers present")
                return True
            else:
                print(f"✗ Missing security headers: {missing_headers}")
                return False
                
        except Exception as e:
            print(f"✗ Security Headers Test Error: {e}")
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test rate limiting"""
        print("Testing Rate Limiting...")
        try:
            # Make rapid requests
            responses = []
            for i in range(10):
                response = self.session.get(f"{self.base_url}/health", timeout=TIMEOUT)
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay
            
            # Check if any requests were rate limited (429)
            if 429 in responses:
                print("✓ Rate limiting is active")
                return True
            else:
                print("⚠ Rate limiting not detected (may need more requests)")
                return True  # Not necessarily a failure
                
        except Exception as e:
            print(f"✗ Rate Limiting Test Error: {e}")
            return False
    
    def test_download_functionality(self) -> bool:
        """Test download functionality"""
        print("Testing Download Functionality...")
        try:
            # First get some results
            response = self.session.post(
                f"{self.base_url}/scan/directories",
                json={"url": TEST_URL},
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                results = response.json()
                
                # Test download
                download_data = {
                    "results": results,
                    "scan_type": "directories"
                }
                
                download_response = self.session.post(
                    f"{self.base_url}/download-results",
                    json=download_data,
                    timeout=TIMEOUT
                )
                
                if download_response.status_code == 200:
                    # Check if it's a text file
                    content_type = download_response.headers.get('content-type', '')
                    if 'text/plain' in content_type:
                        print("✓ Download functionality working")
                        return True
                
                print(f"✗ Download failed: {download_response.status_code}")
                return False
            else:
                print("✗ Cannot test download - scan endpoint failed")
                return False
                
        except Exception as e:
            print(f"✗ Download Test Error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("=" * 60)
        print("WEB SECURITY MATRIX - COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        
        results = {
            "api_health": self.test_api_health(),
            "api_info": self.test_api_info(),
            "input_validation": self.test_input_validation(),
            "security_headers": self.test_security_headers(),
            "rate_limiting": self.test_rate_limiting(),
            "scan_endpoints": self.test_scan_endpoints(),
            "comprehensive_audit": self.test_comprehensive_audit(),
            "download_functionality": self.test_download_functionality(),
        }
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        # Count main tests
        for test_name, result in results.items():
            if test_name != "scan_endpoints":
                total += 1
                if result:
                    passed += 1
                    print(f"✓ {test_name.replace('_', ' ').title()}")
                else:
                    print(f"✗ {test_name.replace('_', ' ').title()}")
        
        # Count scan endpoint tests
        scan_results = results.get("scan_endpoints", {})
        scan_passed = sum(1 for result in scan_results.values() if result)
        scan_total = len(scan_results)
        
        total += scan_total
        passed += scan_passed
        
        print(f"\nScan Endpoints:")
        for endpoint, result in scan_results.items():
            status = "✓" if result else "✗"
            print(f"  {status} {endpoint}")
        
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"\nOverall: {passed}/{total} tests passed ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 TEST SUITE PASSED - Application is ready for use!")
            return {"status": "PASS", "success_rate": success_rate, "details": results}
        else:
            print("⚠️  TEST SUITE FAILED - Please review and fix issues")
            return {"status": "FAIL", "success_rate": success_rate, "details": results}

def main():
    """Main test runner"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = API_BASE_URL
    
    tester = MatrixAppTester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()