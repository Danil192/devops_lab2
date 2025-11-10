# Базовый образ
FROM python:3.10

# Рабочая директория
WORKDIR /app

# Копируем файлы
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем приложение
CMD ["python", "app.py"]
