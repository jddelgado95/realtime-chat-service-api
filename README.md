# realtime-chat-service-api

WebSocket-driven chat backend with user auth, channels, presence tracking, and message history.

### Tech Stack:

- FastAPI
- PostgreSQL + SQLAlchemy
- Redis
- WebSockets
- Docker

### To Run:

```bash
docker-compose build
docker-compose up -d
```

Inspect logs to verify

```bash
docker-compose logs -f api
```

Logs should look like this:

```bash
INFO:     Started server process [1]
api_1    | INFO:     Waiting for application startup.
api_1    | INFO:     Application startup complete.
api_1    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Alembic Commands:

```bash
alembic init alembic
alembic revision --autogenerate -m "init"
alembic upgrade head
```
