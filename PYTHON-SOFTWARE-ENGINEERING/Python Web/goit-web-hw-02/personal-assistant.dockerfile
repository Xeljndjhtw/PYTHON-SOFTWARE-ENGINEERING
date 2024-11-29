# Базовий образ із потрібною версією Python
FROM python:3.10

# Директорія в контейнері для застосунку
WORKDIR /app

# Копіюємо файли проєкту до контейнера
COPY . /app

# Встановлення Poetry
RUN pip install poetry

# Інсталяція залежностей через Poetry
RUN poetry install --no-root

# Встановлюємо команду для запуску застосунку
CMD ["poetry", "run", "python", "main.py"]
