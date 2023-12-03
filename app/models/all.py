from pydantic import BaseModel, field_validator, EmailStr, \
    conint, constr # all these types can identify constraints as conint (gt=10)
from typing import List, Annotated, Union
from datetime import datetime
from fastapi import Body


class CalculateModel(BaseModel):
    num1: int
    num2: int


# создаём модель данных, которая обычно расположена в файле models.py
class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Union[datetime, None] = None
    friends: List[int] = []
    age: int = None
    is_adult: bool = None


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float | None = None
    tags: list[str] = []

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value < -1:
            raise ValueError("Product is too cheap")
        return value


class UserModel(BaseModel):
    name: str
    mail: Annotated[EmailStr, Body()]
    email: Annotated[str, Body(regex=r"^\S+@\S+\.\S+$", deprecated=True)]
    age: Annotated[int | None, Body(gt=0)] = None
    is_subscribed: bool = False


# Pydantic модель ответов на ошибки
class ErrorResponse(BaseModel):
    error_code: int
    error_message: str
    error_details: str = None