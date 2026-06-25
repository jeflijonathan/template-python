from fastapi import Depends, status, File, UploadFile, Request
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.uploadFile.upload_file_service import UploadService
from domains.uploadFile.dto.upload_file_dto import UploadResponseDTO
from config.limiter.limiter import limiter


class UploadController(BaseController, prefix="/uploads", tags=["Secured Uploads"]):
    _upload_service = UploadService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/file", status_code=status.HTTP_200_OK)
        @limiter.limit("100/minute")
        async def get_upload_file(request: Request, db: Session = Depends(get_db)):
            try:
                upload_file = cls._upload_service.get_all_upload_file(db)
                return cls.handle_success(
                    data=upload_file, message="File retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/file/{user_id}", status_code=status.HTTP_200_OK)
        @limiter.limit("5/minute")
        async def secure_upload(
            request: Request,
            user_id: str,
            file: UploadFile = File(...),
            db: Session = Depends(get_db),
        ):
            try:
                processed_file = await cls._upload_service.secure_process_file(
                    db, user_id, file
                )
                response_payload = UploadResponseDTO.from_orm(processed_file)

                return cls.handle_success(
                    data=response_payload.model_dump(),
                    message="File underwent verification scanning and was securely stored.",
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


UploadController.register_routes()
