from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .. import crud, schemas, database, models
from slowapi import Limiter
from slowapi.util import get_remote_address
from schemas import ContactCreate

# Створюємо маршрутизатор для операцій з контактами
router = APIRouter()

# Налаштовуємо схему OAuth2 для отримання токена доступу
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Декодер токену для отримання поточного користувача
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Приймає: токен доступу.
    Перевіряє валідність токену та отримує користувача з бази даних.
    """
    try:
        payload = crud.decode_token(token)  # Розшифровуємо токен
        email = payload.get("sub")  # Отримуємо email користувача
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")  # Помилка: Невалідний токен

    # Пошук користувача за email у базі даних
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")  # Помилка: Користувача не знайдено

    return user

# Маршрут для отримання всіх контактів користувача
@router.get("/contacts", response_model=list[schemas.ContactResponse])
def get_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """
    Повертає список контактів, що належать поточному користувачу.
    Приймає: параметри пагінації (skip, limit).
    """
    return crud.get_user_contacts(db, current_user.id, skip=skip, limit=limit)

router.post("/contacts")
@limiter.limit("5/minute")  # Обмеження: 5 запитів на хвилину
# Маршрут для створення нового контакту
@router.post("/contacts", response_model=schemas.ContactResponse, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """
    Створює новий контакт для поточного користувача.
    Приймає: дані нового контакту у форматі JSON.
    """
    return crud.create_contact(db, contact, current_user.id)

# Маршрут для оновлення існуючого контакту
@router.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """
    Оновлює дані контакту, що належить поточному користувачу.
    Приймає: ID контакту та оновлені дані у форматі JSON.
    """
    return crud.update_contact(db, contact_id, contact, current_user.id)

# Маршрут для видалення контакту
@router.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """
    Видаляє контакт, що належить поточному користувачу.
    Приймає: ID контакту.
    """
    crud.delete_contact(db, contact_id, current_user.id)
    return {"message": "Contact deleted successfully"}
