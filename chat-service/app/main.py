from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.kafka import start_producer, stop_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_producer()
    yield
    await stop_producer()

app = FastAPI(
    title="Chat Service",
    description="Real-Time Chat Service with WebSockets",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "Chat Service is running!"}