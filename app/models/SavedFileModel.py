from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class SavedFileModel(SQLModel, table=True):
	id: int = Field(default=None, primary_key=True)
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	file_path: str
	file_id: str
	filename: str
	password: Optional[str] = None