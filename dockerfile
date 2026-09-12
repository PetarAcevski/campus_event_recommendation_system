FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY backend ./backend
COPY scripts ./scripts
COPY data ./data

EXPOSE 8000

CMD ["sh", "-c", "uv run python -m scripts.create_tables && uv run python -m scripts.import_data && uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000"]