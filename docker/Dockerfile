FROM python:3.11-slim

LABEL maintainer="Muhamad Ridwan <contact@muhamadridwanjr.xyz>"
LABEL org.opencontainers.image.title="GPIWD-Dragon"
LABEL org.opencontainers.image.description="Growth Protocol Intelligence WaterWall Defence"
LABEL org.opencontainers.image.version="1.0.0"

# --- System deps ---
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# --- Working dir ---
WORKDIR /app

# --- Python deps ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- App code ---
COPY . .

# --- Non-root user ---
RUN useradd -m -u 1001 gpiwd && chown -R gpiwd:gpiwd /app
USER gpiwd

# --- Port ---
EXPOSE 7777

# --- Health check ---
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:7777/health || exit 1

# --- Start ---
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "7777", "--workers", "4"]
