from sqlmodel import SQLModel
from fastapi import UploadFile
from typing import Optional

class FileToSave(SQLModel):
	file: UploadFile
	password: Optional[str] = None