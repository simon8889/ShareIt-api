from fastapi import APIRouter, HTTPException, status, Depends, UploadFile
from fastapi.responses import JSONResponse

from app.services.SaveFile import SaveFile
from app.services.SearchFile import SearchFile
from app.schemas.FileToSave import FileToSave
from app.schemas.FileToSearch import FileToSearch
from app.schemas.FileInfo import FileInfo
from app.config.database import get_session

from typing import Optional

files_router = APIRouter()

@files_router.get("/info", tags=["files"])
def get_info(file_id: str, session = Depends(get_session)) -> FileInfo:
	file_to_search = FileToSearch(file_id = file_id)
	file_searcher = SearchFile(file_to_search, session)
	try:
		return file_searcher.get_file_info()
	except HTTPException as e:
		raise e
	
@files_router.post("/download", tags=["files"])
def download_file(file_to_search: FileToSearch, session = Depends(get_session)):
	file_searcher = SearchFile(file_to_search, session)
	try:
		file_response = file_searcher.get_file_from_storage()
		return file_response
	except HTTPException as e:
		raise e

@files_router.post("/upload", tags=["files"])
async def upload_file(file: UploadFile, password: Optional[str] = None, session = Depends(get_session)):
	file_to_save = FileToSave(file = file, password = password)
	save_file = SaveFile(file_to_save, session)
	try:
		file_id = await save_file.save()
		return JSONResponse(status_code = status.HTTP_200_OK, content = {"File": file_id})
	except HTTPException as e:
		raise e
	