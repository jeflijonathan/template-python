from typing import Any, Optional
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.uploadFile.upload_file_model import (
    UploadFileModel,
)


class UploadFileRepository(BaseMySQLService[UploadFileModel]):
    def __init__(self):
        super().__init__(UploadFileModel)

    def create_upload(self, db: Session, data: dict[str, Any]) -> UploadFileModel:
        return self.create(db, data)

    def find_by_user_id(self, db: Session, user_id: str) -> Optional[UploadFileModel]:
        return self.find_one(db, {"user_id": user_id})

    def delete_upload(self, db: Session, id: str) -> Optional[UploadFileModel]:
        return self.delete(db, {"id": id})
