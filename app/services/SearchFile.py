from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from app.schemas.FileToSearch import FileToSearch
from app.schemas.FileInfo import FileInfo
from app.services.FileStorage import FileStorage
from app.models.SavedFileModel import SavedFileModel

from ..utils.hash_password import hash_password, verify_password

class SearchFile():
	def __init__(self, file_to_search: FileToSearch, db: Session):
		self.file_id  = file_to_search.file_id
		self.password  = file_to_search.password
		self.db = db 
	
	def search_in_db(self) -> SavedFileModel:
		query = select(SavedFileModel).where(SavedFileModel.file_id == self.file_id)
		result = self.db.exec(query).first()
		if not result:
			raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="File not found")
		return result
	
	def get_file_info(self) -> FileInfo:
		file_info = self.search_in_db()
		has_password = file_info.password != None
		return FileInfo(file_id = file_info.file_id,
				  		filename = file_info.filename,
						created_at = file_info.created_at,
						has_password = has_password)
		
	def get_file_from_storage(self):
		file_info = self.search_in_db()
		has_password = file_info.password != None
		password_is_correct = verify_password(self.password, file_info.password)
		if has_password and not password_is_correct:
			raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Wrong password") 
		file_stream = FileStorage().download(file_info.file_path)
		response = StreamingResponse(file_stream, media_type="application/octet-stream")
		response.headers["Content-Disposition"] = f"attachment; filename={file_info.filename}"
		return response
	