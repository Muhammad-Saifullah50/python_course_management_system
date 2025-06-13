import streamlit as st
import requests as req


def main():
    is_logged_in = (
        st.session_state.authenticated if "authenticated" in st.session_state else False
    )

    
    st.title("Python Course Management System")

    # Define the pages
    dashboard_page = st.Page("dashboard.py", title="Dashboard", icon="📊")
    create_course_page = st.Page("create_course.py", title="Create Course", icon="📚")
    courses_page = st.Page("courses.py", title="All Courses", icon="📚")
    register_page = st.Page("register.py", title="Register", icon="📝")
    login_page = st.Page("login.py", title="Login", icon="🔑")

    if is_logged_in:
        pages = [dashboard_page, create_course_page, courses_page]

    else:
        pages = [login_page, register_page]

    pg = st.navigation(pages)

    pg.run()


if __name__ == "__main__":
    main()

# have to access the currently logged in user here 
# have to protect the create course page from here to allow only teachers