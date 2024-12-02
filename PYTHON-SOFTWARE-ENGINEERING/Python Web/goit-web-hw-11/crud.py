# crud.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
from datetime import datetime, timedelta

# Функція для створення нового контакту
def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())  # Перетворюємо дані на модель SQLAlchemy
    db.add(db_contact)  # Додаємо в сесію
    db.commit()  # Зберігаємо зміни в базі
    db.refresh(db_contact)  # Оновлюємо об'єкт
    return db_contact  # Повертаємо створений контакт

# Функція для отримання списку контактів
def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

# Функція для отримання одного контакту за ID
def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

# Функція для оновлення контакту
def update_contact(db: Session, contact_id: int, contact_update: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)  # Отримуємо існуючий контакт
    if not db_contact:
        return None  # Якщо контакт не знайдено, повертаємо None
    # Оновлюємо поля, які були передані
    for key, value in contact_update.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()  # Зберігаємо зміни
    db.refresh(db_contact)  # Оновлюємо об'єкт
    return db_contact  # Повертаємо оновлений контакт

# Функція для видалення контакту
def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)  # Отримуємо контакт за ID
    if db_contact:
        db.delete(db_contact)  # Видаляємо з бази
        db.commit()  # Підтверджуємо зміни
    return db_contact  # Повертаємо видалений контакт

# Функція для отримання контактів з фільтрацією
def get_contacts(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    first_name: str = None,
    last_name: str = None,
    email: str = None
):
    # Базовий запит
    query = db.query(models.Contact)

    # Додаємо фільтри, якщо параметри задано
    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))

    # Застосовуємо пагінацію
    return query.offset(skip).limit(limit).all()

# Функція для отримання контактів з днями народження у найближчі 7 днів
def get_upcoming_birthdays(db: Session):
    today = datetime.today().date()  # Сьогоднішня дата
    next_week = today + timedelta(days=7)  # Дата через 7 днів

    # Врахування "перехіду року".
    return db.query(models.Contact).filter(
        or_(
            # Якщо день народження у цьому році
            models.Contact.birthday.between(today, next_week),
            # Якщо день народження у наступному році (перехід через Новий рік)
            models.Contact.birthday.between(
                today.replace(year=today.year - 1), 
                next_week.replace(year=today.year - 1)
            )
        )
    ).all()
