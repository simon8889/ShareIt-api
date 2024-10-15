from fastapi import HTTPException, status, UploadFile

from os import environ 
import boto3
import io

BUCKET_NAME = environ.get("AWS_BUCKET")
s3_client = boto3.client(
	's3',
	aws_access_key_id = environ.get("AWS_ACCESS_KEY_ID") ,
	aws_secret_access_key= environ.get("AWS_SECRET_ACCESS_KEY")
)

class FileStorage():

	def download(self, path: str):
		try:
			file_stream = io.BytesIO()
			s3_client.download_fileobj(BUCKET_NAME, path, file_stream)
			file_stream.seek(0)
			return file_stream
		except Exception as e:
			raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Error")
	
	async def upload(self, file_to_upload: UploadFile, path: str):
		await file_to_upload.seek(0)
		s3_client.upload_fileobj(file_to_upload.file, BUCKET_NAME, path)
		
		
	

		
		