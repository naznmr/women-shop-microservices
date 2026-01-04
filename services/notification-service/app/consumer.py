import json
import asyncio
import aio_pika
from app.settings import settings
from app.db import SessionLocal, init_db
from app.models import Notification
from app.emailer import send_email

def store_notification(payload: dict, status: str, error: str | None, subject: str | None, message: str | None):
    db = SessionLocal()
    try:
        n = Notification(
            event_type=str(payload.get("type", "unknown")),
            order_id=payload.get("order_id"),
            user_email=payload.get("user_email"),
            channel="email",
            subject=subject,
            message=message,
            status=status,
            error=error,
            payload_json=json.dumps(payload, ensure_ascii=False),
        )
        db.add(n)
        db.commit()
    finally:
        db.close()

async def consume_forever():
    init_db()

    while True:
        try:
            print("🔌 Connecting to RabbitMQ:", settings.rabbitmq_url, flush=True)

            conn = await aio_pika.connect_robust(settings.rabbitmq_url)
            channel = await conn.channel()

            exchange = await channel.declare_exchange(
                settings.rabbitmq_exchange,
                aio_pika.ExchangeType.FANOUT,
                durable=True,
            )

            queue = await channel.declare_queue(
                settings.rabbitmq_queue,
                durable=True,
            )

            await queue.bind(exchange)

            print(f"✅ Connected. exchange={settings.rabbitmq_exchange} queue={settings.rabbitmq_queue}", flush=True)

            async with queue.iterator() as it:
                async for message in it:
                    async with message.process():
                        payload = json.loads(message.body.decode("utf-8"))
                        print("📩 Notification event received:", payload, flush=True)

                        # فقط برای سفارش موفق (مثلاً order_paid) ایمیل بفرست
                        event_type = payload.get("type")
                        user_email = payload.get("user_email")

                        subject = None
                        body = None

                        if event_type == "order_paid" and user_email:
                            subject = f"Order #{payload.get('order_id')} پرداخت شد"
                            body = f"سفارش شما با موفقیت ثبت/پرداخت شد.\nمبلغ: {payload.get('total_toman')} تومان"
                            try:
                                await asyncio.to_thread(send_email, user_email, subject, body)
                                store_notification(payload, status="sent", error=None, subject=subject, message=body)
                                print("✅ Email sent (MailHog).", flush=True)
                            except Exception as e:
                                store_notification(payload, status="failed", error=str(e), subject=subject, message=body)
                                print("❌ Email failed:", repr(e), flush=True)
                        else:
                            # سایر رویدادها را هم ذخیره می‌کنیم (برای ارائه/دیباگ)
                            store_notification(payload, status="stored", error=None, subject=None, message=None)

        except Exception as e:
            print("❌ Notification consumer error:", repr(e), flush=True)
            await asyncio.sleep(3)