FROM python:3.11-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /build
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv "$VIRTUAL_ENV" \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git openssh-client ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory /app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . /app

# Fail the image build early if any source file contains a syntax error.
RUN python -m compileall -q xioca

CMD ["python", "-m", "xioca"]
