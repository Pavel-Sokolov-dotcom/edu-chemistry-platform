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


### Запуск нагрузочного тестирования с помощьюLocust
1. Запустить проект с помощью Docker Compose:
```bash
docker-compose up --build
```
2. Создать второй терминал для запуска тестов Locust:
```bash
locust -f load_tests/locustfile.py
```
3. Запустится веб-версия тестов:
[[<img width="1439" height="718" alt="locust" src="https://github.com/user-attachments/assets/395ec825-9e86-429e-afea-b0f6b9939716" />
]] заполнить как на скрине
4. На данный момент, тест запустится на три ручки: проверка логина /api/v1/auth/login, /health и /tasks.
Тест не останавливается автоматически. Его нужно остановить самому. Когда тест остановлен, будут примерно такие данные:
<img width="1437" height="510" alt="locust_finish" src="https://github.com/user-attachments/assets/8cabcd37-f5cf-4c8e-9b00-7492bcd1f6d6" />
