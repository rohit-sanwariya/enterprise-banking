FROM python:3.14-slim

WORKDIR /app
RUN mkdir -p /app/logs

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000