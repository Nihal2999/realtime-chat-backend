from aiokafka import AIOKafkaConsumer
from app.core.config import settings
import json
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

consumer = None

async def process_message(message: dict):
    event = message.get("event")
    if event == "new_message":
        sender = message.get("sender_username")
        room_id = message.get("room_id")
        content = message.get("content")
        print(f"New message notification: {sender} in room {room_id} said: {content}")
        logger.info(f"New message notification: {sender} in room {room_id} said: {content}")

async def consume():
    global consumer
    async for msg in consumer:
        try:
            data = json.loads(msg.value.decode("utf-8"))
            print(f"📨 Received Kafka event: {data}")
            await process_message(data)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

async def start_consumer():
    global consumer
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID,
        auto_offset_reset="earliest"
    )
    await consumer.start()
    asyncio.create_task(consume())
    print("Kafka consumer started!")

async def stop_consumer():
    global consumer
    if consumer:
        await consumer.stop()