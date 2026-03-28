# Тестовое задание DevOps — Effective Mobile

Простое веб-приложение работает за реверс-прокси **nginx**; оба сервиса запускаются в **Docker**. Снаружи доступен только порт **80** у nginx, а backend слушает порт **8080** только во внутренней сети Docker Compose.

## Требования

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/) v2+

## Быстрый старт

1. Склонируйте репозиторий и перейдите в каталог проекта.

2. Создайте файл окружения из примера:

   ```bash
   cp .env.example .env
   ```

   В `.env` из примера уже задана переменная **`APP_PORT`** — это внутренний порт backend внутри Docker-сети (по умолчанию **8080**). Его значение **должно совпадать** с портом, указанным в `upstream` в `nginx/nginx.conf`. Если вы измените порт, пересоберите образ nginx.

3. Соберите образы и запустите сервисы:

   ```bash
   docker compose up -d --build
   ```

   Собранные образы получают явные теги (см. `docker-compose.yml`): `effective-mobile/devops-backend:1.0.0` и `effective-mobile/devops-nginx:1.0.0`. При публикации в registry замените префикс `effective-mobile/` на своё пространство имён.

   **Порядок запуска:** для `backend` в Compose настроен `healthcheck`, поэтому `nginx` запускается только после того, как backend получит статус `healthy`.

4. Остановка:

   ```bash
   docker compose down
   ```

## Проверка работоспособности

В терминале:

```bash
curl http://localhost
```

Ожидаемое **тело ответа** (без кавычек):

```text
Hello from Effective Mobile!
```

Либо откройте в браузере страницу `http://localhost`.

## Как устроена схема

```text
  Пользователь (curl / браузер)
            │
            ▼  :80 (только этот порт на хосте)
     ┌──────────────┐
     │    nginx     │  reverse proxy (Dockerfile на базе nginx:stable-alpine)
     └──────┬───────┘
            │  HTTP → backend:APP_PORT (в сети Docker)
            ▼
     ┌──────────────┐
     │   backend    │  Python (http.server), порт не публикуется наружу
     └──────────────┘
```

1. Запрос приходит на **nginx** на порту **80**.
2. `nginx` проксирует запрос на внутренний порт приложения по имени сервиса **`backend`** (значение `APP_PORT`, по умолчанию **8080**).
3. Backend отвечает на путь **`/`** текстом `Hello from Effective Mobile!`; остальные пути — **404**.

## Структура репозитория

```text
├── backend/
│   ├── Dockerfile
│   └── app.py
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

## Технологии

- **Python 3.12** — минимальный HTTP-сервер (`http.server` / `HTTPServer`)
- **Nginx** (Alpine) — образ на базе `nginx:stable-alpine`, отдельный `Dockerfile`, подмена штатного `default.conf` пользовательским `nginx.conf`, `upstream` и `proxy_pass`
- **Docker / Docker Compose** — изоляция сервисов, пользовательская bridge-сеть

