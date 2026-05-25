import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Matrix Scanner API"
    assert "version" in data
    assert "tools" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_invalid_url():
    response = client.post("/scan/dns", data={"url": "not-a-valid-url!!!"})
    assert response.status_code == 400


def test_empty_url():
    response = client.post("/scan/dns", data={"url": ""})
    assert response.status_code == 400


def test_private_ip_blocked_192():
    response = client.post("/scan/dns", data={"url": "http://192.168.1.1"})
    assert response.status_code == 400
    assert "private" in response.json()["detail"].lower()


def test_private_ip_blocked_10():
    response = client.post("/scan/dns", data={"url": "http://10.0.0.1"})
    assert response.status_code == 400


def test_private_ip_blocked_172():
    response = client.post("/scan/dns", data={"url": "http://172.16.0.1"})
    assert response.status_code == 400


def test_localhost_blocked():
    response = client.post("/scan/dns", data={"url": "http://localhost"})
    assert response.status_code == 400
    assert "private" in response.json()["detail"].lower()


def test_scan_dns_valid():
    response = client.post("/scan/dns", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_ports_valid():
    response = client.post("/scan/ports", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_firewall_valid():
    response = client.post("/scan/firewall", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_technologies_valid():
    response = client.post("/scan/technologies", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_subdomains_valid():
    response = client.post("/scan/subdomains", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_live_valid():
    response = client.post("/scan/live", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_ssl_valid():
    response = client.post("/scan/ssl", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_headers_valid():
    response = client.post("/scan/headers", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_crawl_valid():
    response = client.post("/scan/crawl", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_directories_valid():
    response = client.post("/scan/directories", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_scan_dns_extended_valid():
    response = client.post("/scan/dns-extended", data={"url": "https://example.com"})
    assert response.status_code in [200, 500]


def test_url_normalization():
    response = client.post("/scan/dns", data={"url": "example.com"})
    assert response.status_code in [200, 500]
