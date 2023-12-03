from fastapi.responses import FileResponse
from app.models.all import CalculateModel, User
from typing import List


from fastapi import APIRouter
router = APIRouter()



@router.post("/calculate/{base_num}")
async def calculate(base_num: int, model: CalculateModel):
    return {"result": base_num+model.num1+model.num2}


users_db = [{
        "id": 1,
        "name": "John Doe"
    }

]
# @router.get("/users", response_model=List)
# async def get_users():
#     r = []
#     for user in users_db:
#         r.append(User(**user))
#     return r
#
#
# @router.get("/users/{user_id}")
# async def get_user(user_id: int):
#     for user in users_db:
#         if user['id'] == user_id:
#             return User(**user)
#     return {"error": "User not Found"}
#
#
# @router.post("/users", response_model=User)
# async def get_user(user: User):
#     if user.age is not None:
#         user.is_adult = True if user.age >= 18 else False
#         return user
#     else:
#         return
