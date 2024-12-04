# main.py

from fastapi import FastAPI
from .routers import contacts, auth
from .database import engine, Base

app = FastAPI()  # Створюємо об'єкт FastAPI

# Створення таблиць у базі даних, якщо вони не існують
Base.metadata.create_all(bind=engine)

# Підключаємо маршрути для роботи з контактами
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

# Підключаємо маршрути для роботи з реєстраціями
app.include_router(auth.router, prefix="/auth", tags=["auth"])
