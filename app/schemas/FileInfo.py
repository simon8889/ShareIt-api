from sqlmodel import SQLModel
from datetime import datetime

class FileInfo(SQLModel):
	file_id: str
	filename: str
	has_password: bool
	created_at: datetime
	