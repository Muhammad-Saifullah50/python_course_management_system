import streamlit as st
from backend.utils.users.index import logout


def main():
    is_logged_in = (
        st.session_state.authenticated if "authenticated" in st.session_state else False
    )

    user = st.session_state.get("user") if is_logged_in and "user" in st.session_state else None
    
    role: str | None = user.get("role") if user else None

    st.title("Python Course Management System")

    # Define the pages
    dashboard_page = st.Page("dashboard.py", title="Dashboard", icon="📊")
    create_course_page = st.Page("create_course.py", title="Create Course", icon="📚")
    courses_page = st.Page("courses.py", title="All Courses", icon="📚")
    register_page = st.Page("register.py", title="Register", icon="📝")
    login_page = st.Page("login.py", title="Login", icon="🔑")

    if is_logged_in and role == "teacher":
        pages = [dashboard_page, create_course_page, courses_page]

    elif is_logged_in and role == "student":
        pages = [dashboard_page, courses_page]
    else:
        pages = [login_page, register_page]

    pg = st.navigation(pages)

    pg.run()

    if is_logged_in:
        st.button(
            "Logout",
            use_container_width=True,
            on_click=logout,
        )


if __name__ == "__main__":
    main()
