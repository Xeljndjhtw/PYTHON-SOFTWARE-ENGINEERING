# avatars.py

from fastapi import APIRouter, UploadFile, File, Depends
import cloudinary
import cloudinary.uploader
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session

# Підключення до Cloudinary
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

router = APIRouter()

@router.post("/upload-avatar")
def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db)):
    response = cloudinary.uploader.upload(file.file)
    avatar_url = response['secure_url']
    
    user = db.query(User).filter(User.email == "example@example.com").first()  # Змінити за потребою
    if user:
        user.avatar_url = avatar_url
        db.commit()
    
    return {"message": "Avatar uploaded successfully", "avatar_url": avatar_url}
