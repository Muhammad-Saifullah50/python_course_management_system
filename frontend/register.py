from dotenv import load_dotenv
import streamlit as st
import requests as req
import os

def register():
    """
    Displays a user registration form using Streamlit and handles user registration.
    The function renders a registration form that collects the user's name, email, password, and role (Student or Teacher).
    Upon submission, it sends a POST request to the backend API to create a new user account.
    Accepts:
        None. All inputs are collected via Streamlit widgets.
    Returns:
        None. The function displays success or error messages in the Streamlit app based on the registration outcome.
    """
    if not os.getenv('ENVIRONMENT'):
        load_dotenv('.env.local')
    
    API_URL = os.getenv('API_URL')
    def handle_register(name:str ,email:str, password:str, role: str) -> None:
        
        response = req.post(
            f"{API_URL}/api/register",
            json={"name": name, "email": email, "password": password, "role": role.lower()}
        )
        
        if response.status_code == 201:
            st.success("Registration successful! Please log in from sidebar to continue.")
        else:
            st.error("Registration failed. Please check your credentials.")

    st.header('Hello and welcome! Please register to create an account')

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", options=["Student", "Teacher"])

    st.button('Register', on_click=handle_register, args=(name, email, password, role), use_container_width=True)

if __name__ == "__main__":
    register()