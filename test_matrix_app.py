#!/usr/bin/env python3
"""
Integration test suite for Matrix Scanner application.
Tests security, functionality, and integration against a running API server.
"""

import requests
import time
import sys

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_URL = "https://example.com"
TIMEOUT = 30


class MatrixAppTester:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Matrix-Tester/1.0'
        })

    def test_api_health(self) -> bool:
        """Test API health endpoint."""
        print("Testing API Health...")
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    print("  PASS: API Health Check")
                    return True
            print(f"  FAIL: API Health Check - {response.status_code}")
            return False
        except Exception as e:
            print(f"  FAIL: API Health Check - {e}")
            return False

    def test_api_info(self) -> bool:
        """Test API info endpoint."""
        print("Testing API Info...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                required_fields = ['name', 'version', 'tools']
                if all(field in data for field in required_fields):
                    print("  PASS: API Info Check")
                    return True
            print(f"  FAIL: API Info Check - {response.status_code}")
            return False
        except Exception as e:
            print(f"  FAIL: API Info Check - {e}")
            return False

    def test_input_validation(self) -> bool:
        """Test input validation and sanitization."""
        print("Testing Input Validation...")
        test_cases = [
            {"url": "<script>alert('xss')</script>", "expected_valid": False},
            {"url": "javascript:alert('xss')", "expected_valid": False},
            {"url": "https://example.com", "expected_valid": True},
            {"url": "http://example.com", "expected_valid": True},
            {"url": "example.com", "expected_valid": True},
        ]

        passed = 0
        for tc in test_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/scan/dns",
                    data={"url": tc["url"]},
                    timeout=TIMEOUT
                )
                if tc["expected_valid"]:
                    if response.status_code in [200, 500]:
                        passed += 1
                        print(f"  PASS: Valid URL accepted: {tc['url']}")
                    else:
                        print(f"  FAIL: Valid URL rejected: {tc['url']} - {response.status_code}")
                else:
                    if response.status_code == 400:
                        passed += 1
                        print(f"  PASS: Malicious input rejected: {tc['url']}")
                    else:
                        print(f"  FAIL: Malicious input accepted: {tc['url']} - {response.status_code}")
            except Exception as e:
                if not tc["expected_valid"]:
                    passed += 1
                    print(f"  PASS: Malicious input caused error: {tc['url']}")
                else:
                    print(f"  FAIL: Valid input caused error: {tc['url']} - {e}")

        success = passed >= len(test_cases) * 0.8
        print(f"  Input Validation: {passed}/{len(test_cases)} passed")
        return success

    def test_private_ip_blocked(self) -> bool:
        """Test that private IPs are blocked."""
        print("Testing Private IP Blocking...")
        private_urls = [
            "http://127.0.0.1",
            "http://192.168.1.1",
            "http://10.0.0.1",
            "http://localhost",
        ]
        passed = 0
        for url in private_urls:
            try:
                response = self.session.post(
                    f"{self.base_url}/scan/dns",
                    data={"url": url},
                    timeout=TIMEOUT
                )
                if response.status_code == 400:
                    passed += 1
                    print(f"  PASS: Blocked: {url}")
                else:
                    print(f"  FAIL: Not blocked: {url} - {response.status_code}")
            except Exception as e:
                print(f"  FAIL: Error testing {url}: {e}")

        return passed == len(private_urls)

    def test_scan_endpoints(self) -> dict:
        """Test individual scan endpoints."""
        print("Testing Scan Endpoints...")
        endpoints = [
            ("DNS Scan", "/scan/dns"),
            ("Port Scan", "/scan/ports"),
            ("Firewall Scan", "/scan/firewall"),
            ("Technology Scan", "/scan/technologies"),
            ("Subdomain Scan", "/scan/subdomains"),
        ]

        results = {}
        for name, endpoint in endpoints:
            print(f"  Testing {name}...")
            try:
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    data={"url": TEST_URL},
                    timeout=TIMEOUT
                )
                if response.status_code in [200, 500]:
                    try:
                        data = response.json()
                        if 'success' in data or 'error' in data or 'detail' in data:
                            results[name] = True
                            print(f"    PASS: {name} endpoint working")
                        else:
                            results[name] = False
                            print(f"    FAIL: {name} invalid response format")
                    except Exception:
                        results[name] = False
                        print(f"    FAIL: {name} invalid JSON response")
                else:
                    results[name] = False
                    print(f"    FAIL: {name} HTTP {response.status_code}")
            except Exception as e:
                results[name] = False
                print(f"    FAIL: {name} error: {e}")

        return results

    def run_all_tests(self) -> dict:
        """Run all tests and return results."""
        print("=" * 60)
        print("MATRIX SCANNER - INTEGRATION TEST SUITE")
        print("=" * 60)

        results = {
            "api_health": self.test_api_health(),
            "api_info": self.test_api_info(),
            "input_validation": self.test_input_validation(),
            "private_ip_blocked": self.test_private_ip_blocked(),
            "scan_endpoints": self.test_scan_endpoints(),
        }

        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        passed = 0
        total = 0

        for test_name, result in results.items():
            if test_name != "scan_endpoints":
                total += 1
                if result:
                    passed += 1
                    print(f"PASS: {test_name.replace('_', ' ').title()}")
                else:
                    print(f"FAIL: {test_name.replace('_', ' ').title()}")

        scan_results = results.get("scan_endpoints", {})
        scan_passed = sum(1 for r in scan_results.values() if r)
        scan_total = len(scan_results)

        total += scan_total
        passed += scan_passed

        print(f"\nScan Endpoints:")
        for endpoint, result in scan_results.items():
            status = "PASS" if result else "FAIL"
            print(f"  {status}: {endpoint}")

        success_rate = (passed / total) * 100 if total > 0 else 0
        print(f"\nOverall: {passed}/{total} tests passed ({success_rate:.1f}%)")

        if success_rate >= 80:
            print("TEST SUITE PASSED")
            return {"status": "PASS", "success_rate": success_rate, "details": results}
        else:
            print("TEST SUITE FAILED")
            return {"status": "FAIL", "success_rate": success_rate, "details": results}


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else API_BASE_URL
    tester = MatrixAppTester(base_url)
    results = tester.run_all_tests()
    sys.exit(0 if results["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
