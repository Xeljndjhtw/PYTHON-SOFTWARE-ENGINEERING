# auth.py

"""
Модуль auth.py
Містить функції для створення та перевірки JWT токенів, а також для хешування паролів.
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Налаштування для JWT
SECRET_KEY = os.getenv("SECRET_KEY", "Xelj050791")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Тривалість дії токену доступу
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Тривалість дії токену оновлення

# Контекст для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функція для хешування пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Функція для перевірки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функція для створення JWT токена доступу
def create_access_token(data: dict, expires_delta: timedelta = None):
   
    """
    Створює JWT токен доступу.

    Args:
        data (dict): Дані для токена.

    Returns:
        str: Згенерований JWT токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для створення JWT токена оновлення
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для перевірки токена
def verify_token(token: str):
    """
    Розшифровує JWT токен та повертає його вміст.

    Args:
        token (str): JWT токен.

    Returns:
        dict: Дані, закодовані в токені.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
