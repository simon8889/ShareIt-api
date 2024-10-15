from sqlmodel import SQLModel
from typing import Optional

class FileToSearch(SQLModel):
	file_id: str
	password: Optional[str] = None
	