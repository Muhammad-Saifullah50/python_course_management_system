import subprocess
import threading
import time
import os
import sys

class ServerManager:
    def __init__(self):
        self.flask_process = None
        self.streamlit_process = None
        self.running = True
    
    def start_flask(self):
        """Start Flask server in a separate thread"""
        try:
            print("🚀 Starting Flask backend...")
            self.flask_process = subprocess.Popen([sys.executable, "backend/server.py"])
            print("✅ Flask backend started on http://localhost:5000")
            self.flask_process.wait()
        except Exception as e:
            print(f"❌ Flask server error: {e}")
    
    def start_streamlit(self):
        """Start Streamlit server in a separate thread"""
        try:
            # Wait for Flask to start
            time.sleep(3)
            print("🚀 Starting Streamlit frontend...")
            self.streamlit_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "frontend/app.py"
            ])
            print("✅ Streamlit frontend started on http://localhost:8501")
            self.streamlit_process.wait()
        except Exception as e:
            print(f"❌ Streamlit server error: {e}")
    
    def run_servers(self):
        """Start both servers using threading"""
        # Check if required files exist
        if not os.path.exists("backend/server.py"):
            print("❌ Error: backend/server.py not found")
            return
        
        if not os.path.exists("frontend/app.py"):
            print("❌ Error: frontend/app.py not found")
            return
        
        # Start servers in separate threads
        flask_thread = threading.Thread(target=self.start_flask)
        streamlit_thread = threading.Thread(target=self.start_streamlit)
        
        flask_thread.daemon = True
        streamlit_thread.daemon = True
        
        flask_thread.start()
        streamlit_thread.start()
        
        print("\n🎉 Both servers are starting!")
        print("📱 Frontend: http://localhost:8501")
        print("🔧 Backend:  http://localhost:5000")
        print("\nPress Ctrl+C to stop both servers")
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⛔ Shutting down servers...")
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of both servers"""
        self.running = False
        
        if self.flask_process and self.flask_process.poll() is None:
            self.flask_process.terminate()
        
        if self.streamlit_process and self.streamlit_process.poll() is None:
            self.streamlit_process.terminate()
        
        print("🛑 All servers stopped")

if __name__ == "__main__":
    manager = ServerManager()
    manager.run_servers()