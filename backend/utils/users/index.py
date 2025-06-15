import os
import json
from turtle import update
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
            
def replace_exisitng_user(updated_user:User) -> dict[str , str | int]:
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
    
    if user.enrolled_courses is not None:
       user.enrolled_courses.append(course)
      
       result = replace_exisitng_user(user)
       if result['status_code'] == 200:
           return {'message': 'success', 'status_code': 200, 'data': result['data']}
    
       
       return {'message': 'failure', 'status_code': 500}
    return {'message': 'failure', 'status_code': 500}

def delete_course_enrollment_from_user(user: User, course: Course)-> dict[str, str| int]:
    
    if user.enrolled_courses is not None:
       user.enrolled_courses.remove(course)
      
       result = replace_exisitng_user(user)
       if result['status_code'] == 200:
           return {'message': 'success', 'status_code': 200,'data': result['data']}
    
       
       return {'message': 'failure', 'status_code': 500}
    return {'message': 'failure', 'status_code': 500}