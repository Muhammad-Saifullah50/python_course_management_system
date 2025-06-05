import streamlit as st

def main():
    st.title("Python Course Management System")   
    
    dashboard_page = st.Page('dashboard.py', title='Dashboard', icon='📊')
    create_course_page = st.Page('create_course.py', title='Create Course', icon='📚')
    courses_page = st.Page('courses.py', title='All Courses', icon='📚')
    
    pg = st.navigation([dashboard_page, create_course_page, courses_page],)

    pg.run()

if __name__ == "__main__":
    main()