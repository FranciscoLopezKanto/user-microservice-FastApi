from bson import ObjectId
from .database import users_collection
from .models import User, user_helper

async def create_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def get_users() -> list:
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

async def get_user(user_id: str) -> dict:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_helper(user)

async def update_user(user_id: str, data: dict) -> bool:
    if len(data) < 1:
        return False
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    return result.modified_count > 0

async def delete_user(user_id: str) -> bool:
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0
