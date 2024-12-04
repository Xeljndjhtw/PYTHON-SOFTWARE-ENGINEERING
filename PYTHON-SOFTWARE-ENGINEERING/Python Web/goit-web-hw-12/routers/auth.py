# auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import crud, schemas, database, models

# Створюємо маршрутизатор для обробки запитів, пов'язаних із авторизацією
router = APIRouter()

# Маршрут для реєстрації нового користувача
@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Реєструє нового користувача.
    Перевіряє, чи існує користувач з таким email у базі даних.
    У разі успішної реєстрації повертає дані нового користувача.
    """
    if crud.get_user_by_email(db, user.email):  # Перевіряємо, чи користувач вже існує
        raise HTTPException(status_code=409, detail="User already exists")  # Помилка 409: Конфлікт
    return crud.create_user(db, user)  # Створюємо нового користувача

# Маршрут для логіну користувача
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Виконує аутентифікацію користувача.
    Приймає дані (email та пароль) через форму OAuth2.
    Повертає токени доступу (access_token) та оновлення (refresh_token).
    """
    # Отримуємо користувача за email
    user = crud.get_user_by_email(db, form_data.username)
    
    # Якщо користувача не існує або пароль неправильний
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")  # Помилка 401: Невірні дані

    # Створюємо токен доступу
    access_token = crud.create_access_token({"sub": user.email})
    
    # Створюємо токен оновлення
    refresh_token = crud.create_refresh_token({"sub": user.email})

    # Повертаємо об'єкт із токенами
    return {
        "access_token": access_token,  # Токен доступу
        "refresh_token": refresh_token,  # Токен оновлення
        "token_type": "bearer"  # Тип токену
    }
