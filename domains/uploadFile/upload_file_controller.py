import os
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from domains.uploadFile.upload_file_model import UploadFileModel

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


class UploadFileController:
    @staticmethod
    def get_all(db: Session):
        return db.query(UploadFileModel).all()

    @staticmethod
    async def create(title: str, description: str, file: UploadFile, db: Session):
        title_exists = (
            db.query(UploadFileModel).filter(UploadFileModel.title == title).first()
        )
        if title_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File dengan judul ini sudah ada!",
            )

        if not file or not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File berkas wajib diunggah!",
            )

        file_ext = os.path.splitext(file.filename).lower()
        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".pdf",
            ".docx",
        ]

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Format file tidak didukung! Hanya diizinkan: {', '.join(allowed_extensions)}",
            )

        filename_to_save = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename_to_save)

        try:
            contents = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gagal menyimpan file ke penyimpanan server: {str(e)}",
            )
        finally:
            await file.close()

        new_file = UploadFileModel(
            title=title, description=description, filename=filename_to_save
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        return new_file
