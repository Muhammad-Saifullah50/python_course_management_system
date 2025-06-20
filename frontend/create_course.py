import streamlit as st
import requests as req
import os
from dotenv import load_dotenv

def create_course():
    """
    Displays a Streamlit form for creating a new course and handles its submission.
    This function renders a user interface for entering course details such as course name,
    credit hours, and description. Upon submission, it sends a POST request to the backend API
    to create a new course associated with the currently logged-in user (teacher).
    Accepts:
        None. All inputs are collected via Streamlit widgets.
    Returns:
        None. Displays success or error messages in the Streamlit app based on the API response.
    """
    
    if not os.getenv('ENVIRONMENT'):
        load_dotenv('.env.local')
    
    API_URL = os.getenv('API_URL')
    
    st.header("Create New Course")

    def handle_submit(course_name: str, credit_hours: int, description: str) -> None:
        user = st.session_state.get("user")
        
        if user:
            response = req.post(
                f"{API_URL}/api/courses/create",
                json={
                    "title": course_name,
                    "credit_hours": credit_hours,
                    "description": description,
                    "teacher": {
                        "id": user.get("id"),
                        "email": user.get("email"),
                        "role": user.get("role"),
                        "name": user.get("name"),
                    },
                },
            )
        else:
            st.error("User not found.")
            return

        if response.status_code == 201:
            st.success("Course created successfully!")
        else:
            st.error("Course creation failed. Please try again.")

    course_name = st.text_input("Course Name")
    credit_hours = st.selectbox(label="Credit hours", options=[1, 2, 3, 4, 5])
    description = st.text_area("Description")

    st.button(
        "Create Course",
        on_click=handle_submit,
        args=(course_name, credit_hours, description),
        use_container_width=True,
    )


if __name__ == "__main__":
    create_course()
