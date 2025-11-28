import os
import shutil
import uuid
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.params import File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Photos
from db import get_session
# from shema import PhotoSave



app = APIRouter(prefix="/photos", tags=["Photos"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# сохранение фото
@app.post("/creat_photo")
def save_photo(title:str, 
               file:UploadFile = File(...), 
               session:Session = Depends(get_session)):
    photo = Photos(title=title)
    session.add(photo)
    session.commit()
    session.refresh(photo)

    # создаём уникальное имя
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # сохраняем файл на fдиск
    with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
     # обновляем URL в базе
    photo.url = file_path
    session.commit()
    return {"id": photo.id, "status": "saved", "filename": filename, "url": photo.url}


# получить фото по id
@app.get("/photo/{id}")
def get_photo(id: int, session: Session = Depends(get_session)):
    photo = session.scalar(select(Photos).where(Photos.id == id))

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return FileResponse(photo.url)

# скачать фото
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Определяем MIME-тип (можно расширить при желании)
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=filename
    )