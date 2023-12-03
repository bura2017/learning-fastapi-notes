from fastapi.testclient import TestClient
from app.main import app
import pytest
from httpx import AsyncClient

client = TestClient(app)
async_client = AsyncClient()


def test_custom_exc():
    data = {
        "name": "custom_exc",
        "price": 0
    }
    response = client.post("/items/", json=data)
    assert response.status_code == 418
    assert response.json() == {
        "error": "There is nothing for free"
    }


@pytest.mark.asyncio
async def test_async_test():
    response = await async_client.get("http://127.0.0.1:8000/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0
