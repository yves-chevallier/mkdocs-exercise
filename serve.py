import os
import sys
import signal
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

class MyHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)
        self.last_restart_time = time.time()

    def on_any_event(self, event):
        if self.should_restart(event):
            print(f"Detected {event.event_type} event on {event.src_path}")
            self.restart_process()

    def should_restart(self, event):
        # Ignore __pycache__ files and directories
        if "__pycache__" in event.src_path:
            return False

        # Add a cooldown to prevent too frequent restarts
        current_time = time.time()
        if current_time - self.last_restart_time < 2:  # Cooldown period in seconds
            return False

        self.last_restart_time = current_time
        return True

    def restart_process(self):
        if self.process.poll() is None:  # Check if the process is still running
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()  # Ensure the process has terminated
        time.sleep(1)  # Optional: Add a short delay to ensure the port is freed
        self.process = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)

if __name__ == "__main__":
    path = "./mkdocs_exercises"
    command = "mkdocs serve -f docs/mkdocs.yml " # --verbose
    event_handler = MyHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process.poll() is None:
            os.killpg(os.getpgid(event_handler.process.pid), signal.SIGTERM)
            event_handler.process.wait()
    observer.join()
