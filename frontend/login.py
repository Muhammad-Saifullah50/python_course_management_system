import streamlit as st
import requests as req


def login():
    
    def handle_login(email:str, password:str) -> None:
        response = req.post(
            "http://localhost:8000/api/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state.authenticated = True
        else:
            st.error("Login failed. Please check your credentials.")

    st.header('Welcome back! Please log into your account')

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    st.button('Login', on_click=handle_login, args=(email, password), use_container_width=True)

if __name__ == "__main__":
    login()