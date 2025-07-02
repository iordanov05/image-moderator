# Image Moderator API

FastAPI-сервис для проверки изображений на NSFW через DeepAI NSFW Detector.

---

## Описание

- Принимает `.jpg`, `.png` изображения
- Использует DeepAI для анализа контента
- Возвращает статус `OK` или `REJECTED`

---

## Переменные окружения

В проекте есть пример файла:

`.env.example`


Скопируйте его и создайте свой `.env`:

```bash
cp .env.example .env
```

Заполните необходимые значения:
```bash
DEEPAI_API_KEY=your_deepai_api_key
NSFW_THRESHOLD=0.7
```
`DEEPAI_API_KEY` — ваш API-ключ от DeepAI (обязательно)

`NSFW_THRESHOLD` — пороговое значение (по умолчанию 0.7)

---

## Установка и запуск

### Локально (venv + Make)

```bash
python -m venv .venv
source .venv/bin/activate
make install
make dev
Приложение доступно на http://127.0.0.1:8000
```

### Docker (ручной запуск)

```bash
make docker
make run
```

### Docker Compose

```bash
make compose-up
make compose-down
```
---

## Документация

После запуска приложение доступно на:

- OpenAPI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
---


## Проверки

Запуск всех проверок:

```bash
make pre-commit
```

Или отдельно:

```bash
make lint     # Ruff
make format   # Ruff форматирование
make fix      # Ruff с авто-фиксом
make type     # Mypy типы
make test     # Pytest
```

---


Пример запроса

```bash
curl -X POST "http://localhost:8000/v1/moderate/" \
  -F "file=@example.jpg"
```

Пример ответа:

```json
{
  "status": "OK",
  "score": 0.03
}
```

Логи
Все логи в JSON-формате (stdout):

```json
{
  "level": "INFO",
  "time": "2025-07-03T12:34:56",
  "msg": "DeepAI score 0.045",
  "logger": "app.services.deepai_client",
  "request_id": "..."
}
```
---

## Стек технологий

- FastAPI
- Pydantic v2 + pydantic-settings
- httpx (Async HTTP client)
- orjson (для JSON-логирования)
- pytest (тесты)
- mypy (проверка типов)
- ruff (линтер и форматтер)
- pre-commit (хуки)
- Uvicorn (ASGI-сервер)
- Docker / Docker Compose
---

## License
MIT