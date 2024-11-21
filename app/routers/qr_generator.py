from fastapi import APIRouter, Response
from app.services.QRGenerator import QRGenerator

qr_generator_router = APIRouter()

@qr_generator_router.get("/generate", tags=["QR"])
def generate_qr(link: str):
	qr = QRGenerator(link).generate()
	return Response(content=qr.getvalue(), media_type="image/png")