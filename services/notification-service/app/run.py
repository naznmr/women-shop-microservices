import asyncio
import threading
import uvicorn
from app.main import app
from app.consumer import consume_forever

def start_consumer():
    asyncio.run(consume_forever())

def main():
    t = threading.Thread(target=start_consumer, daemon=True)
    t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
