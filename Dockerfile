
FROM python:3.13-bullseye

ENV PYTHONUNBUFFERED=1

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install the application dependencies.
WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY ./api .

EXPOSE 5000

# Run the application.
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug", "--workers", "1", "--timeout-keep-alive", "60", "--lifespan", "on", "--proxy-headers", "proxy_headers", "True", "forwarded_allow_ips","'*'"]
# CMD uv run gunicorn -w 1 -k uvicorn.workers.UvicornWorker api.main:app --bind 0.0.0.0:5000 --timeout-keep-alive 60 --workers 1 --lifespan on --proxy-headers True forwarded_allow_ips '*'