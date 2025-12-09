from pydantic import BaseModel
from datetime import datetime

class CreateUserRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    status: str
    message: str
