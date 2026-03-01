from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.services import (
    create_room,
    get_room,
    get_all_rooms,
    save_message,
    get_room_messages
)
from app.schemas import RoomCreate
import redis.asyncio as aioredis
from app.core.config import settings
from app.kafka import produce_message
import json

router = APIRouter(tags=["Chat"])
security = HTTPBearer()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(json.dumps(message, default=str))

manager = ConnectionManager()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.post("/rooms")
async def create_chat_room(room_data: RoomCreate, user=Depends(get_current_user)):
    room = await create_room(room_data.name, room_data.members)
    return room

@router.get("/rooms")
async def list_rooms(user=Depends(get_current_user)):
    rooms = await get_all_rooms()
    return rooms

@router.get("/rooms/{room_id}/messages")
async def get_messages(room_id: str, user=Depends(get_current_user)):
    messages = await get_room_messages(room_id)
    return messages

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    room_id: str,
    websocket: WebSocket,
    token: str = Query(...)
):
    payload = decode_access_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    sender_id = payload.get("sub")
    sender_username = payload.get("email")

    room = await get_room(room_id)
    if not room:
        await websocket.close(code=1008)
        return

    await manager.connect(room_id, websocket)

    redis = aioredis.from_url(settings.REDIS_URL)
    await redis.set(f"online:{sender_id}", "true", ex=3600)

    try:
        while True:
            data = await websocket.receive_text()
            message = await save_message(room_id, sender_id, sender_username, data)

            # Produce Kafka event
            await produce_message({
                "event": "new_message",
                "room_id": room_id,
                "sender_id": sender_id,
                "sender_username": sender_username,
                "content": data,
                "message_id": message["id"]
            })

            await manager.broadcast(room_id, message)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await redis.delete(f"online:{sender_id}")
        await redis.aclose()