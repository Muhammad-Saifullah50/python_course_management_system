from typing import Dict, List
from fastapi import FastAPI
from backend.utils.users.index import (
    create_course_in_db,
    create_user,
    delete_course_enrollment_from_user,
    enroll_user_in_course,
    get_all_courses,
    get_all_users,
)
from .classes.index import (
    Course,
    CreateCourseRequest,
    DeleteCourseRequest,
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
    """
    Handles the root endpoint of the Course Management System API.
    Returns:
        dict: A welcome message indicating that the API is accessible.
    """
    
    return {"message": "Welcome to the Course Management System API!"}


@app.post("/api/login")
async def login(data: LoginRequest) -> JSONResponse:
    """
    Handles user login by verifying email and password credentials.
    Args:
        data (LoginRequest): An object containing the user's email and password.
    Returns:
        JSONResponse: 
            - On successful authentication, returns a JSON response with status code 200, a success message, and user data.
            - On failure (invalid email or incorrect password), returns a JSON response with status code 400 and an error message.
    """
    
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
                                    'enrolled_courses': user.get('enrolled_courses'),
                                    "hashed_pwd": user.get('hashed_pwd')
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
    """
    Registers a new user in the system.
    This function checks if a user with the provided email already exists. If not, it hashes the user's password,
    creates a new user object, and saves it to the database. Handles and returns appropriate responses for
    success, duplicate user, and server errors.
    Args:
        data (RegisterRequest): The registration data containing user's name, email, password, and role.
    Returns:
        JSONResponse: A JSON response indicating the result of the registration attempt:
            - 201 if the user is created successfully,
            - 400 if a user with the given email already exists,
            - 500 for any server or creation errors.
    """
    
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
    """
    Creates a new course based on the provided data.
    Args:
        data (CreateCourseRequest): An object containing the course details, including
            title (str): The title of the course.
            description (str): The description of the course.
            credit_hours (int): The number of credit hours for the course.
            teacher (Teacher): An object containing teacher details (id, email, role, name).
    Returns:
        JSONResponse: A JSON response with status code 201 and the created course data if successful.
        Returns status code 400 if any required field is missing.
        Returns status code 500 if an error occurs during course creation.
    """
   
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
    """
    Fetches all available courses and returns them in a JSON response.
    This asynchronous function attempts to retrieve all courses from the data source.
    If successful, it returns a JSON response with a success message and the list of courses.
    If an error occurs during retrieval, it returns a JSON response with an error message and no data.
    Returns:
        JSONResponse: A response object containing a status code, a message, and the courses data (or None on failure).
    """
    
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

@app.delete('/api/courses')
async def delete_course_enrollment(data: DeleteCourseRequest) -> JSONResponse:
    """
    Deletes a course enrollment for a user.
    This asynchronous function attempts to remove a course enrollment for a specified user based on the provided data.
    It calls the `delete_course_enrollment_from_user` function to perform the deletion and returns an appropriate JSON response.
    Args:
        data (DeleteCourseRequest): An object containing the user and course information required to process the deletion.
    Returns:
        JSONResponse: A response object with status code 200 and a success message if the course was dropped successfully,
                      or status code 500 with an error message if the operation failed or an exception occurred.
    """
    
    try:
        course = data.course
        user = data.user
        
        result = delete_course_enrollment_from_user(user, course)
                
        if result['status_code'] == 200:
            return JSONResponse(
                status_code=200,
                content={"message": "Dropped course successfully", "data":  result['data']},
            )
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to drop course", "data": None},
        )   
        
    except Exception as e:
        print(f"Error  dropping course: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": "Something went wrong", "data": None},
        )

@app.post("/api/courses/enroll")
async def enroll_in_course(data: EnrollRequest) -> JSONResponse:
    """
    Enrolls a user in a specified course.
    Args:
        data (EnrollRequest): An object containing the user and course information required for enrollment.
    Returns:
        JSONResponse: A JSON response indicating the result of the enrollment operation.
            - On success (status_code 200): Returns a message and the enrollment data.
            - On failure (status_code 500): Returns an error message and None as data.
    Raises:
        Exception: Handles any unexpected errors during the enrollment process and returns a generic error response.
    """
    
    
    try:
        course = data.course
        user = data.user
        
        result  = enroll_user_in_course(user, course)
        if result['status_code'] == 200:
            return JSONResponse(
                status_code=200,
                content={"message": "Enrolled in course successfully", "data": result['data']},
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


