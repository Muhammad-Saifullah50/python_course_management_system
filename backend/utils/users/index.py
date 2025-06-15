import os
import json
from typing import Dict, List
import streamlit as st

from backend.classes.index import Course, User

def get_all_users():
    """
    Retrieves all user records from the users.json file.
    Reads the JSON file located at 'backend/db/users.json' and returns its contents as a list of users.
    If the file does not exist, raises a FileNotFoundError.
    If the file is empty or contains invalid JSON, returns an empty list.
    Returns:
        list: A list of user records loaded from the JSON file.
    Raises:
        FileNotFoundError: If the users.json file does not exist.
    """
    
    path = 'backend/db/users.json'
    if not os.path.exists(path):
        raise FileNotFoundError("The users.json file does not exist.")

    with open(path, 'r') as f:
        try:
            users: list[User] = json.load(f)
            return users
        except json.JSONDecodeError:
            users = []

def create_user(user: User):
    """
    Creates a new user entry and appends it to the users.json file.
    Args:
        user (User): An instance of the User class containing user information to be added.
    Raises:
        FileNotFoundError: If the users.json file does not exist.
    Returns:
        User: The user object that was added to the file.
    """
    
    
    path = 'backend/db/users.json'

    if not os.path.exists(path):
        raise FileNotFoundError("The users.json file does not exist.")

    with open(path, 'r+') as f:

        try:
            users: List[Dict[str, str | int]] = json.load(f)
        
        except Exception:
            users = []
            
        users.append(user.__dict__)

        f.seek(0)
        json.dump(users, f, indent=4)
        return user
    
def logout():
    """
    Logs out the current user by removing authentication and user information from the session state.
    This function checks for the presence of "authenticated" and "user" keys in the Streamlit session state,
    removes them if they exist, and displays a success message to the user.
    Args:
        None
    Returns:
        None
    """
    
    if "authenticated" in st.session_state:
        del st.session_state["authenticated"]
    if "user" in st.session_state:
        del st.session_state["user"]
    st.success("You have been logged out successfully.")

def create_course_in_db(course: Course):
    """
    Adds a new course to the courses.json database file.
    This function takes a Course object, converts it to a dictionary, and appends it to the list of courses
    stored in the 'backend/db/courses.json' file. If the file does not exist, a FileNotFoundError is raised.
    If the file is empty or contains invalid JSON, it initializes an empty list of courses.
    Args:
        course (Course): The Course object to be added to the database.
    Returns:
        Course: The same Course object that was added to the database.
    Raises:
        FileNotFoundError: If the 'courses.json' file does not exist.
    """
    
    path = 'backend/db/courses.json'

    if not os.path.exists(path):
        raise FileNotFoundError("The courses.json file does not exist.")

    with open(path, 'r+') as f:

        try:
            courses: List[Dict[str, str | int]] = json.load(f)

        except Exception:
            courses = []

        courses.append(course.__dict__)

        f.seek(0)
        json.dump(courses, f, indent=4)
        return course
    
def get_all_courses():
    """
    Retrieves all courses from the courses.json file.
    Reads the list of courses stored in the 'backend/db/courses.json' file. If the file does not exist,
    a FileNotFoundError is raised. If the file exists but contains invalid JSON, an empty list is returned.
    Returns:
        list[Course]: A list of Course objects loaded from the JSON file, or an empty list if the file is empty or invalid.
    Raises:
        FileNotFoundError: If the courses.json file does not exist.
    """
    
    path = 'backend/db/courses.json'
    if not os.path.exists(path):
        raise FileNotFoundError("The courses.json file does not exist.")

    with open(path, 'r') as f:
        try:
            courses: list[Course] = json.load(f)
            return courses
        except json.JSONDecodeError:
            courses = []
            
def replace_exisitng_user(updated_user:User) -> dict[str , str | int]:
    
    """
    Replaces an existing user in the users.json file with updated user information.
    Args:
        updated_user (User): An instance of the User class containing updated user data. The user is identified by its 'id' attribute.
    Returns:
        dict[str, str | int]: A dictionary containing the result of the operation:
            - On success: {'message': 'success', 'status_code': 200, 'data': <updated_user_data>}
            - On failure: {'message': 'failure', 'status_code': 500}
    Raises:
        FileNotFoundError: If the users.json file does not exist.
    Notes:
        - The function reads the users.json file, finds the user with the matching 'id', replaces their data, and writes the updated list back to the file.
        - If the file cannot be decoded as JSON, an error message is printed and a failure response is returned.
    """
    
    path = 'backend/db/users.json'
    if not os.path.exists(path):
        raise FileNotFoundError("The users.json file does not exist.")
    
    with open(path, 'r') as f:
        try:
            users: list[User] = json.load(f)
            for index,user in enumerate(users):
                if user['id'] == updated_user.id:
                    users[index] = updated_user.model_dump()
                    break
                
            with open(path, 'w') as f:
                json.dump(users, f, indent=4)
                
            return {'message': 'success', 'status_code': 200, 'data': updated_user.model_dump()}
        except json.JSONDecodeError as e:
            print('Erroro replacing user', e)
            return {'message': 'failure', 'status_code': 500}
           
def enroll_user_in_course(user: User, course: Course) -> dict[str, str| int]:
    """
    Enrolls a user in a given course and updates the user's enrolled courses.
    Args:
        user (User): The user object to enroll in the course. Must have an 'enrolled_courses' attribute.
        course (Course): The course object to enroll the user in.
    Returns:
        dict[str, str | int]: A dictionary containing the result of the enrollment operation.
            - On success: {'message': 'success', 'status_code': 200, 'data': ...}
            - On failure: {'message': 'failure', 'status_code': 500}
    Notes:
        - The function appends the course to the user's enrolled_courses list and updates the user record.
        - Assumes the existence of a 'replace_exisitng_user' function that updates the user in the data store.
    """
    
    if user.enrolled_courses is not None:
       user.enrolled_courses.append(course)
      
       result = replace_exisitng_user(user)
       if result['status_code'] == 200:
           return {'message': 'success', 'status_code': 200, 'data': result['data']}
    
       
       return {'message': 'failure', 'status_code': 500}
    return {'message': 'failure', 'status_code': 500}

def delete_course_enrollment_from_user(user: User, course: Course)-> dict[str, str| int]:
    """
    Removes a specified course from a user's list of enrolled courses.
    Args:
        user (User): The user object from which the course enrollment will be removed.
        course (Course): The course object to be removed from the user's enrolled courses.
    Returns:
        dict[str, str | int]: A dictionary containing the result of the operation:
    """    
    if user.enrolled_courses is not None:
       user.enrolled_courses.remove(course)
      
       result = replace_exisitng_user(user)
       if result['status_code'] == 200:
           return {'message': 'success', 'status_code': 200,'data': result['data']}
    
       
       return {'message': 'failure', 'status_code': 500}
    return {'message': 'failure', 'status_code': 500}