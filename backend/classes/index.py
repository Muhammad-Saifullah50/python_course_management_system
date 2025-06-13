from pydantic import BaseModel
from typing import Any, Optional


class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str  # 'teacher' or 'student'

class ApiResponse(BaseModel):
    status: int
    message: Optional[str]
    data: Optional[dict[str, Any]]
    

class Course(BaseModel):
    pass


class  User(BaseModel):
    id: str
    email: str
    role: str
    name: str
    hashed_pwd: str