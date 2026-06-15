from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UploadFileResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    filename: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
