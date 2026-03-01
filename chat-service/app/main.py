from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Chat Service",
    description="Real-Time Chat Service with WebSockets by ***Nihal Vernekar***",
    version="1.0.0"
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "Chat Service is running!"}