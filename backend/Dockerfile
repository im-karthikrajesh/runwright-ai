FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system runwright \
    && adduser --system --ingroup runwright runwright

COPY backend/pyproject.toml ./pyproject.toml
COPY backend/src ./src

RUN python -m pip install --upgrade pip \
    && python -m pip install .

USER runwright

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["python", "-m", "uvicorn", "runwright.main:app", "--host", "0.0.0.0", "--port", "8000"]