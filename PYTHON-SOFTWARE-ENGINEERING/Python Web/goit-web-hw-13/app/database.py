# database.property

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

# Налаштування URL для підключення до бази даних PostgreSQL
DATABASE_URL = "postgresql://postgres:admin@localhost/contacts_db"

# Створення двигуна бази даних
engine = create_engine(DATABASE_URL)

# Конфігурація фабрики сесій для роботи з базою даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для створення моделей SQLAlchemy
Base = declarative_base()

# Функція для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
