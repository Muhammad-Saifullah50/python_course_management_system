from functools import partial
from typing import Counter
import streamlit as st
import requests as req


def courses():
    st.title("All Courses")
        

    try:
        response = req.get("http://localhost:8000/api/courses")
        result = response.json()
        courses = result["data"]["courses"]
    except Exception as e:
        st.error(f"Failed to load all courses {e}")
        
    if 'selected_course' not in st.session_state:
        st.session_state.selected_course = None
        
    @st.dialog('Course Details', width='large')  
    def show_modal():
        course = st.session_state.selected_course
        
        def handle_register():
            user = st.session_state.user
            course = st.session_state.selected_course
            response = req.post('http://localhost:8000/api/courses/enroll',
                                json={
                                    'user': user,
                                    'course': course
                                    })
            if response.status_code == 201:
                st.success('Course enrolment successfull. Go to your dashboard for more info')
                st.session_state.user = response.json()['data']['user']
        if course:
            st.subheader(course['title'])
            st.text(f'Instructor: Sir {course['teacher']['name']}')
            st.text(f'Credit hours: {course['credit_hours']}')
            st.text(f'Description: {course['description']}')
            
            st.button('Enroll in this course', type='primary', use_container_width=True, on_click=handle_register)
    
    def select_and_show(course):
        st.session_state.selected_course = course
        show_modal()
        
    for course in courses:
        st.button(f"{course['title']} ➕", on_click=partial(select_and_show, course))
        

if __name__ == "__main__":
    courses()
 # have to find a way to close the modal