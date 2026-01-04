from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_payment_success_or_fail():
    # این تست صرفاً بررسی می‌کند endpoint پاسخ معتبر می‌دهد
    r = client.post("/payments/process", json={"order_id":"1","amount_toman":10000,"card_last4":"2222"})
    assert r.status_code == 200
    data = r.json()
    assert data["order_id"] == "1"
    assert data["amount_toman"] == 10000
    assert data["status"] in ["success","failed"]
