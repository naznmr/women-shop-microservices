import os
import requests

USER = os.getenv("USER_BASE", "http://localhost:8001")
PRODUCT = os.getenv("PRODUCT_BASE", "http://localhost:8002")
ORDER = os.getenv("ORDER_BASE", "http://localhost:8003")

def test_e2e_checkout_flow():
    # register (اگر تکراری شد 409 طبیعی است)
    r = requests.post(f"{USER}/auth/register", json={
        "email":"itest@example.com",
        "full_name":"Integration Test",
        "password":"12345678",
        "phone":"000"
    })
    assert r.status_code in (200, 409)

    # login
    r = requests.post(f"{USER}/auth/login", json={"email":"itest@example.com","password":"12345678"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # get products
    r = requests.get(f"{PRODUCT}/products?limit=10")
    assert r.status_code == 200
    products = r.json()
    assert len(products) > 0
    p0 = products[0]

    # create order (اگر پرداخت fail شد چندبار تلاش می‌کنیم)
    last = None
    for _ in range(10):
        last = requests.post(f"{ORDER}/orders", json={
            "items":[{"product_id": p0["id"], "qty": 1}],
            "card_last4":"2222"
        }, headers=headers)

        if last.status_code == 200:
            break
        if last.status_code == 402:
            continue
        assert False, f"Unexpected status: {last.status_code} body={last.text}"

    assert last.status_code == 200
    data = last.json()
    assert data["total_toman"] > 0