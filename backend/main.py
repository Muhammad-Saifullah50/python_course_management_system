import stat
from fastapi import FastAPI
from pydantic import Json
from backend.utils.users.index import create_user, get_all_users
from .classes.index import ApiResponse, LoginRequest, RegisterRequest, User
import bcrypt
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Course Management System API!"}

@app.post("/api/login")
async def login(data: LoginRequest) -> JSONResponse:
    users: list[User] | None = get_all_users()

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

    new_user = User(name=data.name, email=data.email, role=data.role, hashed_pwd=hashed_pwd)

    if new_user:
        try:
            created_user = create_user(new_user)
            return JSONResponse(status_code=201, content={"message": "User created successfully.", "data": {"user": created_user}})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Error creating user: {str(e)}", "data": None})

    return JSONResponse(status_code=500, content={"message": "Some error occurred.", "data": None})