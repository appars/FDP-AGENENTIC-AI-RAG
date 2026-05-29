FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cicd_agent.py .
COPY templates/ ./templates/ 2>/dev/null || true

# Create log directory
RUN mkdir -p /app/logs

# Create non-root user
RUN useradd -m -u 1000 cicd && chown -R cicd:cicd /app
USER cicd

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expose port
EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "--access-logfile", "/app/logs/access.log", "--error-logfile", "/app/logs/error.log", "cicd_agent:app"]
