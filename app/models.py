from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  
    username: str
    email: EmailStr
    full_name: str = None

    class Config:
        json_encoders = {
            ObjectId: str
        }
