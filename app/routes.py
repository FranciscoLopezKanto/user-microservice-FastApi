from fastapi import APIRouter, HTTPException
from .models import User
from .database import users_collection
from bson import ObjectId

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: User):
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)
    user_dict['id'] = str(result.inserted_id)
    return user_dict

@router.get("/users/", response_model=list[User])
async def read_users():
    users = []
    for user in users_collection.find():
        user['id'] = str(user['_id'])
        users.append(user)
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['id'] = str(user['_id'])
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict(exclude_unset=True)})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {**user.dict(), "id": user_id}

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
