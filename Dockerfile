# ============================
# Base builder (dependency layer)
# ============================
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps kept minimal. faiss-cpu installs from wheels on most platforms.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage pip cache: copy requirements first
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ============================
# Runtime image
# ============================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only the installed site-packages and binaries from builder
COPY --from=base /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=base /usr/local/bin /usr/local/bin

WORKDIR /app

# Copy app code and docs
COPY app ./app
COPY docs ./docs

# Create an unprivileged user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Healthcheck (optional but handy in containers)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',8000)); s.close()" || exit 1

# ENVs (override at runtime; never bake secrets into image)
# ENV OPENAI_API_KEY=""
# ENV DOCS_PATH="./docs"
# ENV EMBEDDING_MODEL="text-embedding-3-small"

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
