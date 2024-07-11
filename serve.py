""" Helper script to automatically restart the mkdocs server when a file changes. """
import os
import signal
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)

    def on_any_event(self, event):
        if self.should_restart(event):
            print(f"Detected {event.event_type} event on {event.src_path}")
            self.restart_process()

    def should_restart(self, event):
        if "__pycache__" in event.src_path:
            return False
        return True

    def restart_process(self):
        if self.process.poll() is None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
        time.sleep(1)
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
