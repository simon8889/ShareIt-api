from fastapi import HTTPException, status
from sqlmodel import Session

from app.utils.supported_files import SUPPORTED_FILE_TYPES, MAX_FILE_SIZE
from app.utils.hash_password import hash_password
from app.models.SavedFileModel import SavedFileModel
from app.schemas.FileToSave import FileToSave
from app.services.FileStorage import FileStorage

from os import path
from uuid import uuid4

class SaveFile():
	def __init__(self, file_to_save: FileToSave, db: Session):
		self.file = file_to_save.file
		self.password = file_to_save.password
		filename_splited = path.splitext(self.file.filename)[1]
		self.extension = filename_splited[1:]
		self.file_id = f"{uuid4()}.{self.extension}"
		self.db = db
	
	def check_allowed_size(self, size: int) -> bool:
		return 0 < size < MAX_FILE_SIZE
	
	def get_path(self) -> str:
		return f"uploads/files/{self.file_id}"
		
	def check_allowed_extension(self) -> bool:
		return self.extension in SUPPORTED_FILE_TYPES.values()
	
	def is_file_empty(self) -> bool:
		return self.file.file.readable() and self.file.file.read(1) == b""
		
	async def check_allowed_file(self) -> bool:
		await self.file.seek(0)
		file_content = await self.file.read()
		await self.file.seek(0)
		size = len(file_content)
		
		valid_extension = self.check_allowed_extension()
		valid_size = self.check_allowed_size(size)
		file_is_not_empty = not self.is_file_empty()
		
		return valid_size and valid_extension and file_is_not_empty
	
	async def store_file(self):
		file_path = self.get_path()
		await FileStorage().upload(self.file, file_path)
	
	def hash_password_if_is_needed(self):
		if self.password:
			self.password = hash_password(self.password)
			
	def save_into_db(self):
		self.hash_password_if_is_needed()
		file_to_save = SavedFileModel(file_path = self.get_path(),
									 file_id = self.file_id,
									 filename = self.file.filename,
									 password = self.password if self.password else None)
		self.db.add(file_to_save)
		self.db.commit()

	async def save(self) -> str:
		if not await self.check_allowed_file():
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not allowed")
		try:
			await self.store_file()
			self.save_into_db()
			return self.file_id
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File not saved")
	