from functools import partial
import streamlit as st
import requests as req


def courses() -> None:
    """
    Displays a list of all available courses and allows the user to view course details and enroll in a course.
    This function fetches the list of courses from the backend API and presents them as buttons in the Streamlit interface.
    When a course is selected, a modal dialog shows detailed information about the course and provides an option to enroll.
    Handles user enrollment by sending a POST request to the backend API and updates the session state accordingly.
    Accepts:
        None. Relies on Streamlit's session state for user information.
    Returns:
        None. All UI rendering and state updates are handled within the function.
    """
    
    st.title("All Courses")
    
    user = st.session_state.get('user')

    credit_hours = 0
    total_credit_hours = sum([c.get('credit_hours') + credit_hours for c in user.get("enrolled_courses")])    
    
    st.subheader(f'Total credit hours of courses you have enrolled: ({total_credit_hours})')
    
    st.subheader(f'Max credit hours: (18)')
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
            if response.status_code == 200:
                st.success('Course enrolment successfull. Go to your dashboard for more info')
                st.session_state.user = response.json()['data']
                
            else:
                st.success('Failed to enroll in course')
                st.session_state.user = response.json()['data']
                
        if course:
            st.subheader(course['title'])
            st.text(f'Instructor: Sir {course['teacher']['name']}')
            st.text(f'Credit hours: {course['credit_hours']}')
            st.text(f'Description: {course['description']}')
            
            is_already_enrolled = course in st.session_state.user['enrolled_courses']
            
            st.button('Enroll in this course', type='primary', use_container_width=True, on_click=handle_register, disabled=is_already_enrolled)
    
    def select_and_show(course):
        st.session_state.selected_course = course
        show_modal()
        
        
    for course in courses:
        is_already_enrolled = course in st.session_state.user['enrolled_courses']
        st.button(
            f"{course['title']} ➕",
            on_click=partial(select_and_show, course),
            disabled=is_already_enrolled or total_credit_hours > 18
            )
        

if __name__ == "__main__":
    courses()
