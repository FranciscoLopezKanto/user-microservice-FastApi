from fastapi import APIRouter, HTTPException,status
from typing import List
from bson import ObjectId
from .models import User, UserCreate, UserUpdate
from .database import users_collection
from pymongo.errors import DuplicateKeyError
router = APIRouter()

# Helper para convertir el ObjectId de MongoDB a string y asegurar que se incluya _id en la respuesta
def user_helper(user) -> dict:
    # Asegura que el campo _id esté incluido como id en la respuesta
    return {
        "_id": str(user["_id"]),  # Convirtiendo ObjectId a string
        "id": str(user["_id"]),  # Incluyendo también el campo id
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
    }

# Ruta para obtener todos los usuarios
@router.get("/users/", response_model=List[User])
async def read_users():
    users_cursor = users_collection.find()  # Obtiene todos los usuarios
    users = await users_cursor.to_list(None)  # Convierte el cursor a lista
    return [user_helper(user) for user in users]

# Ruta para obtener un usuario por su ID
@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})  # Busca por ID
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user_dict = user.dict()  # Convierte el modelo Pydantic a diccionario
    try:
        result = await users_collection.insert_one(user_dict)  # Inserta el nuevo usuario
        user_dict["_id"] = str(result.inserted_id)  # Añadimos el id generado
        return user_dict
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
# Ruta para actualizar un usuario
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate):
    user_dict = user.dict(exclude_unset=True)  # Excluye campos no modificados
    updated_user = await users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},  # Busca al usuario por ID
        {"$set": user_dict},  # Actualiza los campos
        return_document=True  # Devuelve el documento actualizado
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(updated_user)

# Ruta para eliminar un usuario
@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})  # Elimina al usuario
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
