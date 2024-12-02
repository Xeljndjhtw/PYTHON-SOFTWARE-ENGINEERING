# main.py

from fastapi import FastAPI
from .routers import contacts
from .database import engine, Base

app = FastAPI()  # Створюємо об'єкт FastAPI

# Створення таблиць у базі даних, якщо вони не існують
Base.metadata.create_all(bind=engine)

# Підключаємо маршрути для роботи з контактами
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
