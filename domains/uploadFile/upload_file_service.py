import os
import shutil
import re
from fastapi import UploadFile
from sqlalchemy.orm import Session
from common.base.baseMysql import BaseMySQLService
from domains.users.user_model import UserModel, UploadFileModel
from common.utils.compressor import compress_file

TEMP_DIR = "static/temp"
UPLOAD_DIR = "static/uploads"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

BANNED_EXTENSIONS = {
    ".exe",
    ".bat",
    ".cmd",
    ".sh",
    ".bash",
    ".msi",
    ".com",
    ".vbs",
    ".php",
    ".phtml",
    ".php3",
    ".php4",
    ".php5",
    ".phps",
    ".asp",
    ".aspx",
    ".jsp",
    ".jspx",
    ".cgi",
    ".pl",
    ".py",
    ".html",
    ".htm",
    ".xhtml",
    ".svg",
    ".js",
    ".ts",
    ".vtt",
    ".swf",
}


class UploadService:
    def __init__(self):
        self._upload_repo = BaseMySQLService(UploadFileModel)
        self._user_repo = BaseMySQLService(UserModel)

    def _sanitize_filename(self, filename: str) -> str:
        base_name = os.path.basename(filename)
        name_part, ext_part = os.path.splitext(base_name)
        clean_name = re.sub(r"[^a-zA-Z0-9_\-]", "", name_part)
        if not clean_name:
            clean_name = "unnamed_file"
        return f"{clean_name}{ext_part.lower()}"

    async def secure_process_file(
        self, db: Session, user_id: str, file: UploadFile
    ) -> UploadFileModel:
        original_filename = file.filename
        clean_filename = self._sanitize_filename(original_filename)
        _, ext = os.path.splitext(clean_filename)

        if ext in BANNED_EXTENSIONS or file.content_type in [
            "text/html",
            "image/svg+xml",
            "application/javascript",
        ]:
            raise ValueError(
                "Security Violation: This file type is restricted due to security policies."
            )

        user = self._user_repo.find_one(db, {"id": user_id})
        if not user:
            raise ValueError("Target user not found.")

        unique_filename = f"file_{user_id}_{os.urandom(8).hex()}{ext}"
        temp_path = os.path.join(TEMP_DIR, unique_filename)
        permanent_path = os.path.join(UPLOAD_DIR, unique_filename)

        try:
            max_size = 10 * 1024 * 1024
            current_size = 0

            with open(temp_path, "wb") as buffer:
                while chunk := await file.read(64 * 1024):
                    current_size += len(chunk)
                    if current_size > max_size:
                        raise ValueError(
                            "File size limit exceeded! Maximum allowed size is 10MB."
                        )
                    buffer.write(chunk)

            with open(temp_path, "rb") as check_buffer:
                content_preview = check_buffer.read(500 * 1024)  # Scan first 500KB

                malicious_patterns = [
                    b"<script",
                    b"javascript:",
                    b"onerror",
                    b"onload",
                    b"<?php",
                    b"<%=",
                    b"<html",
                    b"<body",
                    b"<iframe>",
                ]
                for pattern in malicious_patterns:
                    if pattern in content_preview.lower():
                        raise ValueError(
                            "Security Violation: Malicious script injection or embedded XSS detected within file bytes."
                        )

                compression_result = compress_file(file_data, clean_filename)

                if compression_result["is_compressed"]:
                    with open(temp_path, "wb") as temp_write:
                        temp_write.write(compression_result["buffer"])

                    if compression_result["encoding"] == "gzip":
                        clean_filename = clean_filename + ".gz"
                        unique_filename = unique_filename + ".gz"
                        permanent_path = os.path.join(UPLOAD_DIR, unique_filename)
                        file.content_type = "application/gzip"

                shutil.move(temp_path, permanent_path)

                file_size_formatted = (
                    f"{round(os.path.getsize(permanent_path) / 1024, 2)} KB"
                )

                existing_file = self._upload_repo.find_one(db, {"user_id": user_id})

                if existing_file:
                    if os.path.exists(existing_file.file_path):
                        try:
                            os.remove(existing_file.file_path)
                        except OSError:
                            pass

                    update_payload = {
                        "filename": clean_filename,
                        "file_path": permanent_path,
                        "file_type": file.content_type,
                        "file_size": file_size_formatted,
                    }
                    return self._upload_repo.update(
                        db, existing_file.id, update_payload
                    )
                else:
                    insert_payload = {
                        "filename": clean_filename,
                        "file_path": permanent_path,
                        "file_type": file.content_type,
                        "file_size": file_size_formatted,
                        "user_id": user_id,
                    }
                    return self._upload_repo.create(db, insert_payload)

        except Exception as error:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise error
