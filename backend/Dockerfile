FROM python:3.11-slim

# ── Environment ───────────────────────────────────────────────────────────────
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production

# ── System dependencies + scanning tools ─────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    curl \
    wget \
    unzip \
    git \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dnsrecon
RUN pip install --no-cache-dir dnsrecon

# Install wafw00f
RUN pip install --no-cache-dir wafw00f

# Install subfinder (Go binary)
RUN wget -q https://github.com/projectdiscovery/subfinder/releases/download/v2.6.3/subfinder_2.6.3_linux_amd64.zip \
    -O /tmp/subfinder.zip \
    && cd /tmp && unzip -q subfinder.zip subfinder \
    && mv /tmp/subfinder /usr/local/bin/subfinder \
    && chmod +x /usr/local/bin/subfinder \
    && rm /tmp/subfinder.zip

# ── App setup ─────────────────────────────────────────────────────────────────
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ── Non-root user ─────────────────────────────────────────────────────────────
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

# ── Runtime ───────────────────────────────────────────────────────────────────
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
