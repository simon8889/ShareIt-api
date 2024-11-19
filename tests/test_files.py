from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.utils.supported_files import MAX_FILE_SIZE
from io import BytesIO
import os
import pytest

client = TestClient(app)

@pytest.fixture
def set_up_file_with_invalid_size():
	file_path = "test.txt"
	with open(file_path, "wb+") as f:
		f.write(b"holii" * MAX_FILE_SIZE)
	yield file_path
	os.remove(file_path)

@pytest.fixture
def set_up_valid_file():
	file_path = "test.txt"
	with open(file_path, "wb+") as f:
		f.write(b"holii")
	yield file_path
	os.remove(file_path)

def delete_file(file_id):
	delete_response = client.delete(
		"/v1/files/delete",
		params={"file_id": file_id}
	)
	return delete_response.status_code, delete_response.json()

def test_delete_file(set_up_valid_file):
	with open(set_up_valid_file, "rb+") as test_file:
		response = client.post(
			"/v1/files/upload",
			files={"file": ("test.txt", test_file, "text/plain")},
			json={"password": "1234"} 
		)
	assert response.status_code == status.HTTP_200_OK
	response_body = response.json()
	file_id = response_body["File"]
	delete_status, delete_response = delete_file(file_id)
	assert delete_status == status.HTTP_200_OK
	assert delete_response["message"] == "file deleted"

def test_file_not_exists():
	exists_response = client.get(
			"/v1/files/exists",
			params={"file_id": "file_not_exists"}
		)	
	assert exists_response.status_code == status.HTTP_200_OK
	assert exists_response.json()["exists"] == False
 
def test_file_exists(set_up_valid_file):
	with open(set_up_valid_file, "rb+") as test_file:
			response = client.post(
				"/v1/files/upload",
				files={"file": ("test.txt", test_file, "text/plain")},
				json={"password": "1234"} 
			)
	assert response.status_code == status.HTTP_200_OK
	response_body = response.json()
	file_id = response_body["File"]
	exists_response = client.get(
		"/v1/files/exists",
		params={"file_id": file_id}
	)	
	assert exists_response.status_code == status.HTTP_200_OK
	assert exists_response.json()["exists"] == True
	delete_file(file_id)
	
def test_upload_file_size_invalid(set_up_file_with_invalid_size):
	with open(set_up_file_with_invalid_size, "rb") as test_file:
		response = client.post(
			"/v1/files/upload",
			files={"file": ("test.txt", test_file, "text/plain")},
			json={"password": "1234"} 
		)
	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert "File not allowed" in response.json()["detail"]

def test_file_upload(set_up_valid_file):
	with open(set_up_valid_file, "rb+") as test_file:
		response = client.post(
			"/v1/files/upload",
			files={"file": ("test.txt", test_file, "text/plain")},
			json={"password": "1234"} 
		)
	assert response.status_code == status.HTTP_200_OK
	response_body = response.json()
	file_id = response_body["File"]
	file_info_request = client.get(
		"/v1/files/info",
		params={"file_id": file_id}
	)
	file_info = file_info_request.json()
	assert response_body["File"] == file_info["file_id"]
	delete_file(file_info["file_id"])

def test_upload_file_no_password(set_up_valid_file):
	with open(set_up_valid_file, "rb") as test_file:
		response = client.post(
			"/v1/files/upload",
			files={"file": ("test.txt", test_file, "text/plain")}
		)
	assert response.status_code == status.HTTP_200_OK
	response_body = response.json()
	file_id = response_body["File"]
	file_info_request = client.get(
		"/v1/files/info",
		params={"file_id": file_id}
	)
	file_info = file_info_request.json()
	assert response_body["File"] == file_info["file_id"]
	delete_file(file_info["file_id"])
	

def test_upload_file_extension_invalid():
	test_file = BytesIO(b"test content")
	
	response = client.post(
		"/v1/files/upload",
		files={"file": ("test.ttttt", test_file, "text/plain")},
	)
	
	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert "File not allowed" in response.json()["detail"]
