import json
import aio_pika
from app.settings import settings

async def publish_order_event(event: dict) -> None:
    conn = await aio_pika.connect_robust(settings.rabbitmq_url)
    async with conn:
        channel = await conn.channel()
        exchange = await channel.declare_exchange(settings.rabbitmq_exchange, aio_pika.ExchangeType.FANOUT, durable=True)
        msg = aio_pika.Message(body=json.dumps(event, ensure_ascii=False).encode("utf-8"))
        await exchange.publish(msg, routing_key="")
