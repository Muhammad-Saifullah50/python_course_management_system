# 🚀 Python Course Management System

Welcome to the **Python Course Management System** – your all-in-one solution for managing courses, students, and enrollments with ease! Whether you're an educator, administrator, or developer, this project streamlines the process of handling course data and student information.

---

## ✨ Features

- **Course Management:** Add, update, delete, and view courses.
- **Enrollment:** Students can enroll in courses with just a few clicks.
- **Modern UI:** Access a user-friendly frontend and simple backend.

---

## 🛠️ Getting Started

Follow these simple steps to set up and run the project:

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd python_course_management_system
   ```

2. **Install the [uv](https://docs.astral.sh/uv/) Package Manager**

3. **Install Dependencies**
   ```bash
   uv sync
   ```
4. **Create a `.env.local` File**

   Create a file named `.env.local` in the project root and add the following content:
   ```env
   ENVIRONMENT='local'
   API_URL='http://localhost:8000'
   ```
5. **Launch the Application**
   ```bash
   uv run launch.py
   ```

6. **Access the System**
   - Frontend: [http://localhost:8501](http://localhost:8501)
   - Backend: [http://localhost:8000](http://localhost:8000)

7. **Add More Packages**
   ```bash
   uv add <package_name>
   ```

   