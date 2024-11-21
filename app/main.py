from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config.database import init_db
from .routers.files import files_router
from .routers.qr_generator import qr_generator_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield

app = FastAPI(lifespan=lifespan)

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Disposition"], 
)

app.include_router(files_router, prefix="/v1/files")
app.include_router(qr_generator_router, prefix="/v1/qr")

@app.get("/")
def health_check():
	return { "status": "Running" }
