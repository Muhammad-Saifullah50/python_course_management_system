import subprocess
import threading
import time
import os
import sys
from pathlib import Path

class ServerManager:
    def __init__(self):
        self.fastapi_process = None
        self.streamlit_process = None
        self.running = True

    def start_fastapi(self):
        """Start FastAPI server"""
        try:
            print("🚀 Starting FastAPI backend...")

            backend_dir = Path("backend").resolve()
            print(f"📁 Watching directory: {backend_dir}")

            # More explicit reload configuration
            self.fastapi_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "backend.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload",
                "--reload-dir", "backend",  # Explicit reload directory
                "--reload-delay", "0.25"    # Faster reload
            ])
            print("✅ FastAPI backend started on http://localhost:8000")
        except Exception as e:
            print(f"❌ FastAPI server error: {e}")

    def start_streamlit(self):
        """Start Streamlit server"""
        try:
            time.sleep(3)  # Wait for backend to start
            print("🚀 Starting Streamlit frontend...")

            env = os.environ.copy()
            # Force polling file watcher
            env["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "poll"
            env["STREAMLIT_SERVER_HEADLESS"] = "true"
            env["STREAMLIT_SERVER_RUN_ON_SAVE"] = "true"

            self.streamlit_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run",
                "frontend/main.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.fileWatcherType", "poll",
                "--server.runOnSave", "true",
                "--server.allowRunOnSave", "true"
            ], env=env)

            print("✅ Streamlit frontend started on http://localhost:8501")
        except Exception as e:
            print(f"❌ Streamlit server error: {e}")

    def check_file_structure(self):
        """Check if the required files and structure exist"""
        issues = []

        if not os.path.exists("backend"):
            issues.append("❌ 'backend' directory not found")
        elif not os.path.exists("backend/main.py"):
            issues.append("❌ 'backend/main.py' not found")
        elif not os.path.exists("backend/__init__.py"):
            issues.append("⚠️  'backend/__init__.py' missing (recommended for proper Python package)")

        if not os.path.exists("frontend"):
            issues.append("❌ 'frontend' directory not found")
        elif not os.path.exists("frontend/main.py"):
            issues.append("❌ 'frontend/main.py' not found")

        return issues

    def run_servers(self):
        """Start both servers using threading"""
        issues = self.check_file_structure()
        if issues:
            print("🔍 File structure issues detected:")
            for issue in issues:
                print(f"  {issue}")
            if any("❌" in issue for issue in issues):
                print("\n❌ Cannot start servers due to missing critical files.")
                return

        print("🔧 Starting development servers with auto-reload...")
        print("💡 Tips for better reload experience:")
        print("   - Save files with Ctrl+S (don't just auto-save)")
        print("   - Check terminal for reload messages")
        print("   - If still not working, try restarting the manager")
        print("   - Make sure no syntax errors in your code\n")

        fastapi_thread = threading.Thread(target=self.start_fastapi)
        streamlit_thread = threading.Thread(target=self.start_streamlit)

        fastapi_thread.daemon = True
        streamlit_thread.daemon = True

        fastapi_thread.start()
        streamlit_thread.start()

        print("\n🎉 Both servers are starting!")
        print("📱 Frontend: http://localhost:8501")
        print("🔧 Backend:  http://localhost:8000")
        print("📖 API Docs: http://localhost:8000/docs")
        print("\n🔄 Auto-reload is enabled for both servers")
        print("Press Ctrl+C to stop both servers")

        try:
            while self.running:
                # Check if processes are still running
                if self.fastapi_process and self.fastapi_process.poll() is not None:
                    print("⚠️ FastAPI process exited unexpectedly.")
                    print("   Check for errors in your backend code.")
                    
                if self.streamlit_process and self.streamlit_process.poll() is not None:
                    print("⚠️ Streamlit process exited unexpectedly.")
                    print("   Check for errors in your frontend code.")
                    
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Shutting down servers...")
            self.shutdown()

    def shutdown(self):
        """Clean shutdown of both servers"""
        self.running = False

        if self.fastapi_process and self.fastapi_process.poll() is None:
            print("🛑 Stopping FastAPI server...")
            self.fastapi_process.terminate()
            try:
                self.fastapi_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.fastapi_process.kill()

        if self.streamlit_process and self.streamlit_process.poll() is None:
            print("🛑 Stopping Streamlit server...")
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()

        print("🛑 All servers stopped")


if __name__ == "__main__":
    manager = ServerManager()
    manager.run_servers()