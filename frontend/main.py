import streamlit as st

def main():
    is_user_logged_in = st.user.is_logged_in

    if not is_user_logged_in:
        if st.button("Log in with Google"):
            st.login()
        st.stop()

    st.title("Python Course Management System")
    st.write(f'Welcome {st.user.name}')



    # Define the pages
    dashboard_page = st.Page('dashboard.py', title='Dashboard', icon='📊')
    create_course_page = st.Page('create_course.py', title='Create Course', icon='📚')
    courses_page = st.Page('courses.py', title='All Courses', icon='📚')

    pg = st.navigation([dashboard_page, create_course_page, courses_page, ])

    pg.run()


    st.button("Log out", on_click=st.logout, use_container_width=True)

if __name__ == "__main__":
    main()
    