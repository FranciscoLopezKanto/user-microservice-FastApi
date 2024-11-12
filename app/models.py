from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        alias_generator = str.lower  # Genera alias en minúsculas automáticamente
        json_encoders = {
            ObjectId: str  # Convierte ObjectId a str
        }

# Esquema para crear un usuario
class UserCreate(UserBase):
    pass

# Esquema para la respuesta de un usuario (incluye id)
class User(UserBase):
    id: str = Field(..., alias="_id")  # Alias _id para mapear correctamente el campo de MongoDB

    class Config:
        orm_mode = True
        alias_generator = str.lower  # Permite que los campos sean accesibles en minúsculas
        json_encoders = {
            ObjectId: str  # Convierte ObjectId a str
        }

# Esquema para actualizar un usuario (no incluye id, solo los campos editables)
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True
        alias_generator = str.lower
