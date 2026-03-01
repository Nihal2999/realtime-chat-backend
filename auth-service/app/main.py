from fastapi import FastAPI
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
from app.db import engine, Base
from app.routes import router

security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Auth Service",
    description="Authentication Service for Real-Time Chat App by ***Nihal Vernekar***",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "Auth Service is running!"}