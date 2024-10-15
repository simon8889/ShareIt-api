from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config.database import init_db
from .routers.files import files_router
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(files_router, prefix="/v1/files")

@app.get("/")
def health_check():
	return { "status": "Running" }
