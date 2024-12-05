# cache.py

import redis
from app.models import User

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Функція для кешування користувача
def cache_user(user_id: int, user: User):
    redis_client.set(f"user:{user_id}", user.json(), ex=3600)  # Зберігає на 1 годину

# Функція для отримання користувача з кешу
def get_user_from_cache(user_id: int):
    user_data = redis_client.get(f"user:{user_id}")
    if user_data:
        return User.parse_raw(user_data)
    return None
