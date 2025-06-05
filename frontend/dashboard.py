import streamlit as st

def dashboard():
    
    role:str = 'student'
    
    if role == 'teacher':
        st.title("Teacher Dashboard")
        
    if role == 'student':
        st.title("Student Dashboard")
  
    
if __name__ == "__main__":
    dashboard()