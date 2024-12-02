# contacts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()  # Створюємо об'єкт маршрутизатора

# Ендпоінт для створення нового контакту
@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db)):
    return crud.create_contact(db, contact)

# Ендпоінт для отримання списку контактів
@router.get("/", response_model=list[schemas.ContactResponse])
def get_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_contacts(db, skip, limit)

# Ендпоінт для отримання одного контакту за ID
@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(database.get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Ендпоінт для оновлення контакту
@router.put("/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact_update: schemas.ContactUpdate, db: Session = Depends(database.get_db)):
    updated_contact = crud.update_contact(db, contact_id, contact_update)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

# Ендпоінт для видалення контакту
@router.delete("/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db)):
    deleted_contact = crud.delete_contact(db, contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact

# Пошук
@router.get("/", response_model=list[schemas.ContactResponse])
def get_contacts(
    skip: int = 0,
    limit: int = 10,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    db: Session = Depends(database.get_db)
):
    # Передаємо параметри пошуку у функцію CRUD
    return crud.get_contacts(
        db,
        skip=skip,
        limit=limit,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

@router.get("/birthdays", response_model=list[schemas.ContactResponse])
def get_upcoming_birthdays(db: Session = Depends(database.get_db)):
    # Викликаємо функцію для отримання контактів
    return crud.get_upcoming_birthdays(db)

