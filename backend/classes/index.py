from pydantic import BaseModel
from typing import Any, List, Optional


class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str
    

class ApiResponse(BaseModel):
    status: int
    message: Optional[str]
    data: Optional[dict[str, Any]]

    
class Course(BaseModel):
    id: str
    title: str
    description: str
    credit_hours: int
    teacher: dict[str, str | int] 


class  User(BaseModel):
    id: str
    email: str
    role: str
    name: str
    hashed_pwd: str
    enrolled_courses: Optional[List[Course]]
    
class Teacher(BaseModel):
    id: str
    email: str
    name: str
    role: str
    
class CreateCourseRequest(BaseModel):
    title: str
    description: str
    credit_hours: int
    teacher: Teacher
    
    
class EnrollRequest(BaseModel):
    user: User
    course: Course
    
class DeleteCourseRequest(BaseModel):
    user: User
    course: Course