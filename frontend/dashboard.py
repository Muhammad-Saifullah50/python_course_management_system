import streamlit as st
import pandas as pd
import requests as req

from backend.classes.index import Course, User
def dashboard():
    """
    Displays the dashboard interface for the currently logged-in user based on their role.
    The function checks the user's role from the Streamlit session state and renders either a teacher or student dashboard.
    For teachers, it displays a welcome message and dashboard title.
    For students, it displays a welcome message, dashboard title, a table of enrolled courses, and provides the ability to drop courses via a button.
    Handles course drop requests by sending a DELETE request to the backend API and updates the session state accordingly.
    Accepts:
        None. Relies on `st.session_state.user` for user information.
    Returns:
        None. Renders UI components using Streamlit.
    """
    
            
    user = st.session_state.user
    role = user.get("role")

    if role == "teacher":
        st.header(f"Welcome, {user['name']}")
        st.title("Teacher Dashboard")

    if role == "student":
        st.header(f"Welcome, {user['name']}")
        st.title("Student Dashboard")
        
        def handle_drop(course:Course, user:User):
            
            response = req.delete('http://localhost:8000/api/courses', json={'course': course, 'user': user})
            
            if response.status_code == 200:
                st.success('Course dropped successfully')
                st.session_state.user = response.json()['data']
            else:
                st.error('Failed to drop course. please try again')

        if user.get("enrolled_courses"):
            data = [
                {
                    "Course ID": c.get("id"),
                    "Course Title": c.get("title"),
                    "Credit Hours": c.get("credit_hours"),
                    "Teacher": c.get("teacher").get("name"),
                }
                for c in user.get("enrolled_courses")
            ]
            
            df= pd.DataFrame(data)
            st.subheader('Enrolled Courses')
            st.dataframe(df, hide_index=True)
            
        if user['enrolled_courses'] != []:    
            st.subheader('Drop Courses')
        else:
            st.write('No courses to display. Please enroll in courses to study.')
        
        for course in user['enrolled_courses']:
            st.button(
                course['title'],
                icon='🗑️',
                on_click=lambda c=course: handle_drop(c, user),
                key=f'drop_{course['id']}'
        
            )
if __name__ == "__main__":
    dashboard()
# for styudent: dispolay the enriolled courses
# for teacher: display vcreated courses
