from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    room_id: str
    content: str

class MessageResponse(BaseModel):
    id: Optional[str] = None
    room_id: str
    sender_id: str
    sender_username: str
    content: str
    created_at: datetime

class RoomCreate(BaseModel):
    name: str
    members: list[str]

class RoomResponse(BaseModel):
    id: Optional[str] = None
    name: str
    members: list[str]
    created_at: datetime