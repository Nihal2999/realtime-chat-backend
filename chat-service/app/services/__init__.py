from datetime import datetime
from bson import ObjectId
from app.db import get_db
from app.models import message_entity, room_entity, message_list_entity, room_list_entity

async def create_room(name: str, members: list[str]) -> dict:
    db = get_db()
    room = {
        "name": name,
        "members": members,
        "created_at": datetime.utcnow()
    }
    result = await db.rooms.insert_one(room)
    room["_id"] = result.inserted_id
    return room_entity(room)

async def get_room(room_id: str) -> dict:
    db = get_db()
    room = await db.rooms.find_one({"_id": ObjectId(room_id)})
    if room:
        return room_entity(room)
    return None

async def get_all_rooms() -> list:
    db = get_db()
    rooms = await db.rooms.find().to_list(100)
    return room_list_entity(rooms)

async def save_message(room_id: str, sender_id: str, sender_username: str, content: str) -> dict:
    db = get_db()
    message = {
        "room_id": room_id,
        "sender_id": sender_id,
        "sender_username": sender_username,
        "content": content,
        "created_at": datetime.utcnow()
    }
    result = await db.messages.insert_one(message)
    message["_id"] = result.inserted_id
    return message_entity(message)

async def get_room_messages(room_id: str) -> list:
    db = get_db()
    messages = await db.messages.find({"room_id": room_id}).sort("created_at", 1).to_list(100)
    return message_list_entity(messages)