import streamlit as st
import requests as req

def register():
    def handle_register(name:str ,email:str, password:str, role: str) -> None:
        response = req.post(
            "http://localhost:8000/api/register",
            json={"name": name, "email": email, "password": password, "role": role.lower()}
        )
        
        if response.status_code == 200:
            st.success("Registration successful!")
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