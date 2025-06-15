from typing import Dict, List
from fastapi import FastAPI
from backend.utils.users.index import (
    create_course_in_db,
    create_user,
    enroll_user_in_course,
    get_all_courses,
    get_all_users,
)
from .classes.index import (
    Course,
    CreateCourseRequest,
    EnrollRequest,
    LoginRequest,
    RegisterRequest,
    User,
)
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
                is_pwd_correct = bcrypt.checkpw(
                    data.password.encode(), user.get("hashed_pwd").encode()
                )

                if is_pwd_correct:
                    return JSONResponse(
                        status_code=200,
                        content={
                            "message": "Login successful",
                            "data": {
                                "user": {
                                    "id": user.get("id"),
                                    "email": user.get("email"),
                                    "role": user.get("role"),
                                    "name": user.get("name"),
                                    'enrolled_courses': user.get('enrolled_courses')
                                }
                            },
                        },
                    )
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"message": "Login failed", "data": None},
                    )

        return JSONResponse(
            status_code=400, content={"message": "Invalid email", "data": None}
        )

    return JSONResponse(
        status_code=400, content={"message": "Invalid email or password.", "data": None}
    )


@app.post("/api/register")
async def register(data: RegisterRequest) -> JSONResponse:
    users: list[User] | None = get_all_users()

    if users:
        for user in users:
            if user.get("email") == data.email:
                return JSONResponse(
                    status_code=400,
                    content={"message": "User already exists.", "data": None},
                )

    hashed_pwd = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
    id = str(uuid.uuid1())
    new_user = User(
        id=id, name=data.name, email=data.email, role=data.role, hashed_pwd=hashed_pwd, enrolled_courses=[]
    )

    if new_user:
        try:
            create_user(new_user)
            return JSONResponse(
                status_code=201,
                content={"message": "User created successfully.", "data": None},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": f"Error creating user: {str(e)}", "data": None},
            )

    return JSONResponse(
        status_code=500, content={"message": "Some error occurred.", "data": None}
    )


@app.post("/api/courses/create")
async def create_course(data: CreateCourseRequest) -> JSONResponse:
    if (
        not data.title
        or not data.description
        or not data.credit_hours
        or not data.teacher
    ):
        return JSONResponse(
            status_code=400,
            content={"message": "All fields are required.", "data": None},
        )
    course = Course(
        id=str(uuid.uuid1()),
        title=data.title,
        description=data.description,
        credit_hours=data.credit_hours,
        teacher={
            "id": data.teacher.id,
            "email": data.teacher.email,
            "role": data.teacher.role,
            "name": data.teacher.name,
        },
    )

    try:
        created_course = create_course_in_db(course)
        return JSONResponse(
            status_code=201,
            content={
                "message": "Course created successfully.",
                "data": created_course.__dict__,
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Error creating course: {str(e)}", "data": None},
        )


@app.get("/api/courses")
async def get_courses() -> JSONResponse:
    try:
        courses = get_all_courses()

        return JSONResponse(
            status_code=200,
            content={"message": "Courses fetched successfully", "data": {'courses': courses}},
        )
    except Exception as e:
        courses = []
        print(f"Error  fetching  courses {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to fetch courses", "data": None},
        )



@app.post("/api/courses/enroll")
async def enroll_in_course(data: EnrollRequest) -> JSONResponse:
    try:
        course = data.course
        user = data.user
        
        result  = enroll_user_in_course(user, course)
        if result['status_code'] == 200:
            return JSONResponse(
                status_code=200,
                content={"message": "Enrolled in course successfully", "data": None},
            )
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to enroll", "data": None},
        )   
        
    except Exception as e:
        print(f"Error  enrolling in course: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Something went wrong", "data": None},
        )


