# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from . import auth
from .database import engine, Base
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import aioredis
from app.routers import contacts, users, avatars
from app.cache import cache_user, get_user_from_cache

app = FastAPI()  # Створюємо об'єкт FastAPI

# Створення таблиць у базі даних, якщо вони не існують
Base.metadata.create_all(bind=engine)

# Підключаємо маршрути для роботи з контактами
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

# Ініціалізація обмежувача запитів
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Middleware для обробки обмежень
@app.middleware("http")
async def slowapi_middleware(request, call_next):
    response = await limiter.middleware(request, call_next)
    return response

from fastapi.middleware.cors import CORSMiddleware

# Увімкнення CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення Redis
redis = aioredis.from_url("redis://localhost")

@app.on_event("startup")
async def startup():
    await FastAPILimiter.init("redis://localhost:6379")

@app.get("/limited-route")
@limiter.limit("5 per minute")  # Обмеження 5 запитів на хвилину
async def limited_route():
    return {"message": "You are allowed to access this route"}

# Пшдключення роутерів
app.include_router(avatars.router, prefix="/avatars", tags=["avatars"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])