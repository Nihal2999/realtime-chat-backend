from datetime import datetime

def message_entity(message: dict) -> dict:
    return {
        "id": str(message["_id"]),
        "room_id": message["room_id"],
        "sender_id": message["sender_id"],
        "sender_username": message["sender_username"],
        "content": message["content"],
        "created_at": message["created_at"]
    }

def room_entity(room: dict) -> dict:
    return {
        "id": str(room["_id"]),
        "name": room["name"],
        "members": room["members"],
        "created_at": room["created_at"]
    }

def message_list_entity(messages: list) -> list:
    return [message_entity(message) for message in messages]

def room_list_entity(rooms: list) -> list:
    return [room_entity(room) for room in rooms]