# --- build stage ----------------------------------------------------------
FROM python:3.11-slim AS base

# Установим системные зависимости 
RUN apt-get update && \
    apt-get install -y --no-install-recommends libmagic1 && \
    rm -rf /var/lib/apt/lists/*

# Создадим рабочую директорию
WORKDIR /app

# Копируем только файлы зависимостей — слои кешируются лучше
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Запускаем приложение
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
