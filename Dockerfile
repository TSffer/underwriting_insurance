FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /underwriting_insurance

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project

ENV PATH="/underwriting_insurance/.venv/bin:$PATH"

COPY . .

RUN uv sync

EXPOSE 8501

# REMOVED: ENV OPENAI_API_KEY=... 
# (Docker will inject the variable from the .env file automatically)

CMD ["streamlit", "run", "src/infrastructure/app.py", "--server.port=8501", "--server.address=0.0.0.0"]