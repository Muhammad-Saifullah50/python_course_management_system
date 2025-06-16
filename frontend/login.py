import os
import streamlit as st
import requests as req
from dotenv import load_dotenv

def login():
    """
    Displays a login form using Streamlit, allowing users to enter their email and password to authenticate.
    The function renders input fields for email and password, and a login button. When the button is clicked,
    it sends a POST request to the backend API endpoint '/api/login' with the provided credentials.
    If authentication is successful, it updates the session state to reflect the authenticated user.
    Accepts:
        None (inputs are taken interactively from the user via the Streamlit UI).
    Returns:
        None (the function operates via side effects, updating Streamlit's session state and UI).
    """
    if not os.getenv('ENVIRONMENT'):
        load_dotenv('.env.local')
    
    API_URL = os.getenv('API_URL')
    
    def handle_login(email:str, password:str) -> None:
        response = req.post(
            f"{API_URL}/api/login",
            json={"email": email, "password": password}
        )
        
        result = response.json()
        
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state.authenticated = True
            
            st.session_state.user = result.get('data').get('user')
        else:
            st.error("Login failed. Please check your credentials.")

    st.header('Welcome back! Please log into your account')

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    st.button('Login', on_click=handle_login, args=(email, password), use_container_width=True)

if __name__ == "__main__":
    login()