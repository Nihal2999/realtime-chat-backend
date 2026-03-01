from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.consumer import start_consumer, stop_consumer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_consumer()
    yield
    await stop_consumer()

app = FastAPI(
    title="Notification Service",
    description="Kafka Consumer for Chat Notifications by ***Nihal Vernekar***",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "Notification Service is running!"}