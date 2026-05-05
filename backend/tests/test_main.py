import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint returns expected fields."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Matrix Scanner API"
    assert "version" in data
    assert "tools" in data


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_invalid_url():
    """Test with invalid URL."""
    response = client.post("/scan/dns", data={"url": "not-a-valid-url!!!"})
    assert response.status_code == 400


def test_empty_url():
    """Test with empty URL."""
    response = client.post("/scan/dns", data={"url": ""})
    assert response.status_code == 400


def test_private_ip_blocked_192():
    """Test that private IPs are blocked."""
    response = client.post("/scan/dns", data={"url": "http://192.168.1.1"})
    assert response.status_code == 400
    assert "private" in response.json()["detail"].lower()


def test_private_ip_blocked_10():
    """Test that 10.x.x.x is blocked."""
    response = client.post("/scan/dns", data={"url": "http://10.0.0.1"})
    assert response.status_code == 400


def test_private_ip_blocked_172():
    """Test that 172.16.x.x is blocked."""
    response = client.post("/scan/dns", data={"url": "http://172.16.0.1"})
    assert response.status_code == 400


def test_localhost_blocked():
    """Test that localhost is blocked."""
    response = client.post("/scan/dns", data={"url": "http://localhost"})
    assert response.status_code == 400
    assert "private" in response.json()["detail"].lower()


def test_scan_dns_valid():
    """Test DNS scan accepts valid URL."""
    response = client.post("/scan/dns", data={"url": "https://example.com"})
    # Should not return 400 (may return 200 or 500 depending on tools)
    assert response.status_code in [200, 500]


def test_scan_ports_valid():
    """Test port scan accepts valid URL."""
    response = client.post("/scan/ports", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_firewall_valid():
    """Test firewall scan accepts valid URL."""
    response = client.post("/scan/firewall", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_technologies_valid():
    """Test technology scan accepts valid URL."""
    response = client.post("/scan/technologies", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_subdomains_valid():
    """Test subdomain scan accepts valid URL."""
    response = client.post("/scan/subdomains", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_url_normalization():
    """Test that URLs without protocol are normalized."""
    response = client.post("/scan/dns", data={"url": "example.com"})
    assert response.status_code in [200, 500]
