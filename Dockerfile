# Use the official uv image with Python pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Enable bytecode compilation and use copy mode (better for Docker layer caching)
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies first (separate layer for caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the project
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

RUN uv pip install -U "yt-dlp[default]" curl_cffi

# Make sure the venv is on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run the bot
CMD ["python", "-m", "main"]