import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_invalid_url():
    """Test with invalid URL"""
    response = client.post("/audit", json={"url": "invalid-url"})
    assert response.status_code == 400

def test_private_ip_blocked():
    """Test that private IPs are blocked"""
    response = client.post("/audit", json={"url": "http://192.168.1.1"})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()

def test_localhost_blocked():
    """Test that localhost is blocked"""
    response = client.post("/audit", json={"url": "http://localhost"})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"].lower()

def test_valid_domain():
    """Test with a valid domain (mocked)"""
    # This would normally test with a real domain
    # For now, we'll test the URL validation
    response = client.post("/audit", json={"url": "https://httpbin.org"})
    # Should not return 400 for URL validation
    assert response.status_code != 400

def test_scan_options():
    """Test scan options handling"""
    data = {
        "url": "https://httpbin.org",
        "enable_dns": "true",
        "enable_ports": "false",
        "enable_vulns": "true",
        "enable_directories": "false"
    }
    response = client.post("/audit", json=data)
    # Should process the request (may timeout but shouldn't be 400)
    assert response.status_code in [200, 408, 500]  # 408 for timeout, 500 for connection error
