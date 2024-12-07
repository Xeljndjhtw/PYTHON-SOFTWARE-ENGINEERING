# models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

# Клас моделі для користувачів
class User(Base):
    __tablename__ = "users"  # Назва таблиці в базі даних

    id = Column(Integer, primary_key=True, index=True)  # Унікальний ідентифікатор
    email = Column(String, unique=True, index=True, nullable=False)  # Унікальний email користувача
    hashed_password = Column(String, nullable=False)  # Хешований пароль користувача
    contacts = relationship("Contact", back_populates="owner")  # Зв'язок із контактами (1 до багатьох)
    is_verified = Column(Boolean, default=False)  # Додавання статусу верифікації
    avatar_url = Column(String, nullable=True)  # Поле для аватара


# Клас моделі для контактів
class Contact(Base):
    __tablename__ = "contacts"  # Назва таблиці в базі даних

    id = Column(Integer, primary_key=True, index=True)  # Унікальний ідентифікатор контакту
    first_name = Column(String, index=True)  # Ім'я контакту
    last_name = Column(String, index=True)  # Прізвище контакту
    email = Column(String, unique=True, index=True)  # Унікальний email контакту
    phone = Column(String, unique=True)  # Унікальний номер телефону контакту
    birthday = Column(String)  # Дата народження контакту
    additional_info = Column(String, nullable=True)  # Додаткова інформація (необов'язково)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Зовнішній ключ на таблицю користувачів
    owner = relationship("User", back_populates="contacts")  # Зв'язок із власником контакту (користувачем)
