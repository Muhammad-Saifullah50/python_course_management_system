import subprocess
import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class ProcessManager:
    def __init__(self, name, start_command, watch_dir):
        self.name = name
        self.start_command = start_command
        self.watch_dir = Path(watch_dir).resolve()
        self.process = None
        self.observer = None

    def start(self):
        self.stop()  # kill any existing
        print(f"🚀 Starting {self.name}...")
        self.process = subprocess.Popen(self.start_command)
        print(f"✅ {self.name} started.")

    def stop(self):
        if self.process and self.process.poll() is None:
            print(f"🛑 Stopping {self.name}...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print(f"✅ {self.name} stopped.")

    def restart(self):
        print(f"🔄 Reloading {self.name} due to changes...")
        self.start()

    def watch(self):
        class ReloadHandler(FileSystemEventHandler):
            def __init__(self, manager):
                self.manager = manager

            def on_any_event(self, event):
                if event.src_path.endswith(".py"):
                    self.manager.restart()

        print(f"👀 Watching {self.name} at {self.watch_dir}")
        event_handler = ReloadHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_dir), recursive=True)
        self.observer.start()

    def shutdown(self):
        self.stop()
        if self.observer:
            self.observer.stop()
            self.observer.join()


def main():
    backend = ProcessManager(
        "FastAPI backend",
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000"
        ],
        "backend"
    )

    # Streamlit doesn't need external reloading
    streamlit_env = os.environ.copy()
    streamlit_env["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "auto"
    streamlit_env["STREAMLIT_SERVER_HEADLESS"] = "true"
    streamlit_env["STREAMLIT_SERVER_RUN_ON_SAVE"] = "true"

    print("🚀 Starting Streamlit frontend...")
    streamlit_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "frontend/main.py",
            "--server.port",
            "8501"
        ],
        env=streamlit_env
    )
    print("✅ Streamlit frontend started.")

    backend.start()
    backend.watch()

    print("\n🎉 Servers running with live reload!")
    print("🔁 FastAPI will restart on file changes.")
    print("♻️ Streamlit handles its own hot reloads.")
    print("🛑 Press Ctrl+C to quit.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⛔ Shutting down...")
        backend.shutdown()
        if streamlit_process.poll() is None:
            print("🛑 Stopping Streamlit frontend...")
            streamlit_process.terminate()
            try:
                streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                streamlit_process.kill()
        print("✅ All done!")



if __name__ == "__main__":
    main()
