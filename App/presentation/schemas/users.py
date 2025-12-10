from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    status: str
    message: str
    
class UserModel(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    is_active: bool
    created_at: datetime
class GetUserByEmail(BaseModel):
    email: EmailStr

class GetUserByEmailResponse(BaseModel):
    status: str
    message: str
    user: UserModel

class GetUserByid(BaseModel):
    id: str