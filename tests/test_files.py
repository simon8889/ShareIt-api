import pytest
from fastapi import status, UploadFile
from fastapi.testclient import TestClient
from app.main import app
from app.utils.supported_files import MAX_FILE_SIZE
from unittest.mock import patch
from io import BytesIO
import tempfile

client = TestClient(app)

@pytest.fixture
def mock_save_file():
	with patch("app.services.SaveFile") as MockSaveFile:
		mock_instance = MockSaveFile.return_value
		mock_instance.save.return_value = "test_file_id"
		yield mock_instance
		
def test_upload_file_success_2(mock_save_file):
	with tempfile.TemporaryFile(delete=True) as temp_file:
		# Write some data to the file
		temp_file.write(b'This is some temporary data.')
		
		# Move to the beginning of the file to read the data
		temp_file.seek(0)
		data = temp_file.read()

	# Realiza la solicitud de prueba
	response = client.post(
		"/v1/files/upload",
		files={"file": ("test.txt", tempfile, "text/plain")},  # Agrega el tipo de contenido
		params={"password": "test_password"}  # Si tu endpoint necesita la contraseña
	)

	# Verifica la respuesta
	assert response.status_code == status.HTTP_200_OK
	assert "File" in response.json()
	assert response.json()["File"] == "test_file_id" 



def test_upload_file_success(mock_save_file):
	test_file = BytesIO(b"test content")
	test_file.name = "test_file.txt"

	# Realiza la solicitud de prueba
	response = client.post(
		"/v1/files/upload",
		files={"file": (test_file.name, test_file, "text/plain")},  # Agrega el tipo de contenido
		params={"password": "test_password"}  # Si tu endpoint necesita la contraseña
	)

	# Verifica la respuesta
	assert response.status_code == status.HTTP_200_OK
	assert "File" in response.json()
	assert response.json()["File"] == "test_file_id" 


def test_upload_file_size_invalid(mock_save_file):
	test_file = BytesIO(b"test content" * (MAX_FILE_SIZE))
	
	response = client.post(
		"/v1/files/upload",
		files={"file": ("test.txt", test_file, "text/plain")},
		data={"password": "1234"}
	)
	
	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert "File not allowed" in response.json()["detail"]
	mock_save_file.save.assert_not_called()

def test_upload_file_no_password(mock_save_file):
	test_file = BytesIO(b"test content")
	
	response = client.post(
		"/v1/files/upload",
		files={"file": ("test.txt", test_file, "text/plain")}
	)
	
	assert response.status_code == status.HTTP_200_OK
	mock_save_file.save.assert_called_once()

def test_upload_file_extension_invalid(mock_save_file):
	test_file = BytesIO(b"test content")
	
	response = client.post(
		"/v1/files/upload",
		files={"file": ("test.ttttt", test_file, "text/plain")},
	)
	
	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert "File not allowed" in response.json()["detail"]
	mock_save_file.save.assert_not_called()
