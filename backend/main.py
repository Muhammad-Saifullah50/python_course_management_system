from fastapi import FastAPI
from backend.utils.users.index import create_user, get_all_users
from .classes.index import ApiResponse, LoginRequest, RegisterRequest, User
import bcrypt


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Course Management System API!"}

@app.post("/api/login")
def login(data: LoginRequest) -> ApiResponse:
    pass

@app.post("/api/register")
def register(data: RegisterRequest) -> ApiResponse:
    
    users: list[User] | None = get_all_users()
    
    if users:    
        for user in users:
            if user['email'] == data.email:
                return ApiResponse(status=400, message="User already exists.", data=None)
            
    
    hashed_pwd = bcrypt.hashpw(data.password.encode() , bcrypt.gensalt()).decode('utf-8')
    
    new_user = User(data.name, data.email, data.role, hashed_pwd)
    
    if new_user:
        try:
            created_user = create_user(new_user)
            return ApiResponse(status=201, message="User created successfully.", data={"user": created_user})
        except Exception as e:
            return ApiResponse(status=500, message=f"Error creating user: {str(e)}", data=None)

    return ApiResponse(status=500, message="Some error occurred.", data=None)