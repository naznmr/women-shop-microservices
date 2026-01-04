import time
import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.settings import settings

class UpstreamError(Exception):
    pass

class CircuitOpenError(Exception):
    pass

class AsyncCircuitBreaker:
    """Circuit breaker ساده برای async.
    - fail_max: بعد از چند شکست مدار باز می‌شود
    - reset_timeout: بعد از چند ثانیه اجازه‌ی یک درخواست آزمایشی می‌دهد
    """
    def __init__(self, fail_max: int = 5, reset_timeout: int = 20):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self._fail_count = 0
        self._opened_at: float | None = None
        self._lock = asyncio.Lock()

    async def before_call(self):
        async with self._lock:
            if self._opened_at is None:
                return
            if (time.time() - self._opened_at) >= self.reset_timeout:
                # half-open: اجازه یک تلاش
                return
            raise CircuitOpenError("Circuit is open")

    async def on_success(self):
        async with self._lock:
            self._fail_count = 0
            self._opened_at = None

    async def on_failure(self):
        async with self._lock:
            self._fail_count += 1
            if self._fail_count >= self.fail_max:
                self._opened_at = time.time()

payment_breaker = AsyncCircuitBreaker(fail_max=5, reset_timeout=20)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=3),
    retry=retry_if_exception_type((httpx.RequestError, UpstreamError)),
)
async def get_product(product_id: str) -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{settings.product_service_url}/products/{product_id}")
    if r.status_code != 200:
        raise UpstreamError(f"Product lookup failed: {r.status_code}")
    return r.json()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=3),
    retry=retry_if_exception_type((httpx.RequestError, UpstreamError)),
)
async def process_payment(order_id: int, amount_toman: int, card_last4: str) -> dict:
    await payment_breaker.before_call()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(f"{settings.payment_service_url}/payments/process", json={
                "order_id": str(order_id),
                "amount_toman": amount_toman,
                "card_last4": card_last4,
            })
        if r.status_code != 200:
            raise UpstreamError(f"Payment failed: {r.status_code}")
        data = r.json()
        await payment_breaker.on_success()
        return data
    except Exception:
        await payment_breaker.on_failure()
        raise
