# syntax=docker/dockerfile:1

# ---- builder stage: build wheels so runtime layer stays slim
FROM python:3.11-slim AS builder
WORKDIR /wheels
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --wheel-dir /wheels -r requirements.txt

# ---- runtime stage
FROM python:3.11-slim

# Create non-root user and writable app/data dirs
RUN useradd -m -u 10001 appuser && mkdir -p /app /data && chown -R appuser:appuser /app /data
WORKDIR /app

# Install deps from wheels only (no build tools kept)
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# Copy app
COPY . .

# Environment defaults
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    DATA_DIR=/data

# Expose the Flask port
EXPOSE 8080

# HEALTHCHECK calls /health
COPY healthcheck.py /app/healthcheck.py
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python /app/healthcheck.py

# Drop privileges
USER appuser

# Run
CMD ["python","app.py"]