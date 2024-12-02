# models.py

from sqlalchemy import Column, Integer, String, Date
from .database import Base

# Описуємо модель для таблиці "contacts"
class Contact(Base):
    __tablename__ = "contacts"  # Назва таблиці в базі даних

    id = Column(Integer, primary_key=True, index=True)  # Первинний ключ
    first_name = Column(String, index=True)  # Ім'я
    last_name = Column(String, index=True)  # Прізвище
    email = Column(String, unique=True, index=True)  # Електронна пошта (унікальна)
    phone = Column(String, unique=True)  # Номер телефону (унікальний)
    birthday = Column(Date)  # День народження
    additional_info = Column(String, nullable=True)  # Додаткова інформація (необов'язкова)
