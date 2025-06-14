from typing import Dict, List
from fastapi import FastAPI
from backend.utils.users.index import create_user, get_all_users
from .classes.index import  CreateCourseRequest, LoginRequest, RegisterRequest, User
import bcrypt
from fastapi.responses import JSONResponse
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Course Management System API!"}

@app.post("/api/login")
async def login(data: LoginRequest) -> JSONResponse:
    users: List[Dict[str, str | int]] | None = get_all_users()

    if users:
        for user in users:
            if user.get("email") == data.email:
                is_pwd_correct = bcrypt.checkpw(data.password.encode(), user.get("hashed_pwd").encode())

                if is_pwd_correct:
                    return JSONResponse(
                        status_code=200,
                        content={
                            'message': 'Login successful',
                            'data': {
                                'user': {
                                    'email': user.get("email"),
                                    'role': user.get("role"),
                                    'name': user.get("name")
                                }
                            }
                        }
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            'message': 'Login failed',
                            'data': None
                        }
                    )

        return JSONResponse(status_code=400, content={"message": "Invalid email", "data": None})

    return JSONResponse(status_code=400, content={"message": "Invalid email or password.", "data": None})


@app.post("/api/register")
async def register(data: RegisterRequest) -> JSONResponse:

    users: list[User] | None = get_all_users()
    
    if users:    
        for user in users:
            if user.get("email") == data.email:
                return JSONResponse(status_code=400, content={"message": "User already exists.", "data": None})

    hashed_pwd = bcrypt.hashpw(data.password.encode() , bcrypt.gensalt()).decode()
    id = str(uuid.uuid1())
    new_user = User(id=id, name=data.name, email=data.email, role=data.role, hashed_pwd=hashed_pwd)

    if new_user:
        try:
            create_user(new_user)
            return JSONResponse(status_code=201, content={"message": "User created successfully.", "data": None})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Error creating user: {str(e)}", "data": None})

    return JSONResponse(status_code=500, content={"message": "Some error occurred.", "data": None})


@app.post('/api/courses/create')
async def create_course(data: CreateCourseRequest) -> JSONResponse:
    pass