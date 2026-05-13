# Stage 1: Build
FROM python:3.12-slim-bookworm as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/install/bin:$PATH"
ENV PYTHONPATH="/app/backend:/app/backend/apps:$PYTHONPATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /install
COPY . .

RUN chmod +x docker/backend/entrypoint.sh

ENTRYPOINT ["docker/backend/entrypoint.sh"]
