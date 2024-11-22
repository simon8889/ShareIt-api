from fastapi import APIRouter, Response
from app.services.QRGenerator import QRGenerator

qr_generator_router = APIRouter()

@qr_generator_router.get("/generate", tags=["QR"])
def generate_qr(link: str):
	qr = QRGenerator(link).generate()
	response = Response(content=qr.getvalue(), media_type="image/png")
	response.headers["Content-Disposition"] = f"attachment; filename=qr_shareit.png"
	response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
	return response