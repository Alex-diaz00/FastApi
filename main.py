from validation import validate_price
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
app = FastAPI()

class Order(BaseModel):
    id: int
    item: str
    quantity: int
    price: float
    status: str


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.post("/solution")
def process_orders(orders: list[Order], criterion: str):

    if len(orders) == 0:
        return {"message": "The orders list should not be empty"}
    if not validate_price(orders):
        return {"message": "The price should be positive"}
    total = 0
    for o in orders:
        if o.status == criterion:
            total += o.price*o.quantity
    return total


client = TestClient(app)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


data = [
{
    "id": 1,
    "item": "Laptop",
    "quantity": 1,
    "price": 999.99,
    "status": "completed"
  },
{
    "id": 2,
    "item": "Smartphone",
    "quantity": 2,
    "price": 499.95,
    "status": "pending"
  },
{
    "id": 3,
    "item": "Headphones",
    "quantity": 3,
    "price": 99.90,
    "status": "completed"
  },
{
    "id": 4,
    "item": "Mouse",
    "quantity": 4,
    "price": 24.99,
    "status": "canceled"
  }
]

def test_orders():
    response = client.post(
        "/solution?criterion=completed",
        json=data
    )
    assert response.status_code == 200
    assert response.json() == 1299.69


def test_negative_order():
    response = client.post(
        "/solution?criterion=completed",
        json=[{
    "id": 4,
    "item": "Mouse",
    "quantity": 4,
    "price": -20,
    "status": "canceled"
  }]
    )
    assert response.status_code == 200
    assert response.json() == {"message": "The price should be positive"}


def test_empty_order_list():
    response = client.post(
        "/solution?criterion=completed",
        json=[]
    )
    assert response.status_code == 200
    assert response.json() == {"message": "The orders list should not be empty"}
