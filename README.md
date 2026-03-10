# Проект "Платформа для подготовки к ЕГЭ по Химии" (Edu Chemistry Platform).

Backend-платформа для подготовки к ЕГЭ по химии с REST API, JWT-аутентификацией, автоматизированным и нагрузочным тестированием.

### Основная цель проекта: демонстрация практик backend-разработки и автоматизации тестирования.

### Архитектура проекта

Backend:
- FastAPI
- PostgreSQL
- Docker
- Docker Compose

Тестирование:
- Pytest
- Locust

### Основные возможности

- JWT аутентификация
- регистрация пользователей
- login / refresh token

### Структура проекта
```text
app/
   api/
   services/
   models/

tests/
   api/
   auth/

locust/

docker-compose.yml
```

### Запуск проекта
```bash
docker-compose up --build
```

API документация:
http://localhost:8000/docs
