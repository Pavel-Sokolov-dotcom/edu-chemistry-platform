FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir .
COPY src/ ./src/
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
