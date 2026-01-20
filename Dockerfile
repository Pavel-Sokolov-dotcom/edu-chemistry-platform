FROM python:3.11-slim
WORKDIR /app

# 1. Сначала устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 2. Копируем ТОЛЬКО файл зависимостей
COPY pyproject.toml .

# 3. Устанавливаем зависимости отдельно 
RUN pip install --no-cache-dir .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 4. Копируем исходный код ПОСЛЕ установки зависимостей
# Это улучшает кэширование Docker layers
COPY src/ ./src/

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]