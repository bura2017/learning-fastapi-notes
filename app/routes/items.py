from fastapi import APIRouter, Query, status
from app.models.all import Item
from typing import Annotated
from app.exceptions import CustomException, HTTPException


app = APIRouter()

@app.post("/", status_code=201)
async def create_item(item: Item) -> Item:
    if item.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if item.price == 0:
        raise CustomException("There is nothing for free")
    return item


@app.get("/")
async def read_items(q: Annotated[str, Query(min_length=3, max_length=50, pattern="query$")] = ...)\
        -> list[Item]:
    print(q)
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
