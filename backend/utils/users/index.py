import os
import json
from typing import Dict, List
import streamlit as st

from backend.classes.index import Course, User

def get_all_users():
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
    if "authenticated" in st.session_state:
        del st.session_state["authenticated"]
    if "user" in st.session_state:
        del st.session_state["user"]
    st.success("You have been logged out successfully.")

def create_course_in_db(course: Course):
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
    path = 'backend/db/courses.json'
    if not os.path.exists(path):
        raise FileNotFoundError("The courses.json file does not exist.")

    with open(path, 'r') as f:
        try:
            courses: list[Course] = json.load(f)
            return courses
        except json.JSONDecodeError:
            courses = []