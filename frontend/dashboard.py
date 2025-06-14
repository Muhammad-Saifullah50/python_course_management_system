import streamlit as st

def dashboard():
    user = st.session_state.user
    
    role = user.get('role')

    if role == 'teacher':
        st.title("Teacher Dashboard")
        
    if role == 'student':
        st.title("Student Dashboard")
  
    
if __name__ == "__main__":
    dashboard()