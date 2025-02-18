# Используем официальный базовый образ Python 3.10
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем остальной код приложения в контейнер
COPY . .

# Команда для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
