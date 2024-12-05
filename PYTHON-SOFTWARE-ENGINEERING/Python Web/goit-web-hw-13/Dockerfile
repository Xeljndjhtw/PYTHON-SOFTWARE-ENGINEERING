# 1. Визначаємо базовий образ, від якого будемо будувати свій контейнер
FROM python:3.12

# 2. Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# 3. Копіюємо requirements.txt в контейнер
COPY requirements.txt /app/

# 4. Встановлюємо залежності, вказані в requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копіюємо увесь код проекту в контейнер
COPY . /app/

# 6. Відкриваємо порт для FastAPI
EXPOSE 8000

# 7. Команда для запуску FastAPI через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
