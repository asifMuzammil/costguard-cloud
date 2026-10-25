# Lightweight, Zero-Dependency Base
FROM python:3.11-slim

LABEL maintainer="Asif Muzammil <https://github.com/asifMuzammil>"
LABEL description="CostGuard Cloud (AWS) - Zero-Knowledge AWS Zombie Resource & Waste Audit"

WORKDIR /app

# Install dependencies (strictly minimal)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY costguard /app/costguard

# Create report output directory & set environment default
ENV COSTGUARD_OUTPUT_DIR=/app/output
RUN mkdir -p /app/output

# Set default entrypoint
ENTRYPOINT ["python3", "-m", "costguard.cli"]
