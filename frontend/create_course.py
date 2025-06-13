import streamlit as st
import requests as req

def create_course():
    st.header('Create New Course')    
    
    def handle_submit(course_name:str, credit_hours:int, description:str) -> None:
        response = req.post(
                "http://localhost:8000/api/courses/create",
                json={"course_name": course_name, "credit_hours": credit_hours, "description": description}
        )
        # have to pass the currently logged in user as well or at least its id
        
        if response.status_code == 200:
            st.success("Course created successfully!")
        else:
            st.error("Course creatio failed failed. Pleasr try again.")

    course_name = st.text_input("Course Name")
    credit_hours = st.selectbox(label='Credit hours', options=[1,2,3,4,5])
    description = st.text_area('Description')
    
    st.button('Create Course', on_click=handle_submit, args=(course_name, credit_hours, description), use_container_width=True)
    
if __name__ == "__main__":
    create_course()