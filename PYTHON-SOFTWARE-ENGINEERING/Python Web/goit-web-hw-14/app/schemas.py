# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# Базова схема для контактів (загальні поля)
class ContactBase(BaseModel):
    first_name: str  # Ім'я
    last_name: str  # Прізвище
    email: EmailStr  # Електронна пошта
    phone: str  # Номер телефону
    birthday: date  # День народження
    additional_info: Optional[str] = None  # Додаткова інформація

# Схема для створення нового контакту
class ContactCreate(ContactBase):
    pass  # Використовує ті ж поля, що й базова схема

# Схема для оновлення контакту
class ContactUpdate(BaseModel):
    first_name: Optional[str]  # Ім'я (може бути пропущене)
    last_name: Optional[str]  # Прізвище
    email: Optional[EmailStr]  # Електронна пошта
    phone: Optional[str]  # Номер телефону
    birthday: Optional[date]  # День народження
    additional_info: Optional[str]  # Додаткова інформація

# Схема для відповіді API (включає ID контакту)
class ContactResponse(ContactBase):
    id: int  # ID контакту

    class Config:
        orm_mode = True  # Дозволяє працювати з ORM-моделями

# Схема для реєстрації користувача
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Схема для відповіді з користувачем
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# Схема для логіну
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
