from fastapi import HTTPException, status, UploadFile

from os import environ 
import boto3
import io

class FileStorage():
	def __init__(self):
		self.bucket= environ.get("AWS_BUCKET")
		self.s3_client = boto3.client(
			's3',
			aws_access_key_id = environ.get("AWS_ACCESS_KEY_ID") ,
			aws_secret_access_key= environ.get("AWS_SECRET_ACCESS_KEY")
		)

	def download(self, path: str):
		try:
			file_stream = io.BytesIO()
			self.s3_client.download_fileobj(self.bucket, path, file_stream)
			file_stream.seek(0)
			return file_stream
		except Exception as e:
			raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Error")
	
	async def upload(self, file_to_upload: UploadFile, path: str):
		try:
			await file_to_upload.seek(0)
			self.s3_client.upload_fileobj(file_to_upload.file, self.bucket, path)
		except Exception as e:
			raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")
	
	def delete(self, path: str):
		try:
			self.s3_client.delete_object(Bucket=self.bucket, Key=path)
		except Exception as e:
			raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error")
	
			
		
		
	

		
		