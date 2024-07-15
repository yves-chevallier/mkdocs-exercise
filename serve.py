""" Helper script to automatically restart the mkdocs server when a file changes. """
import os
import signal
import subprocess
import time
import toml
import click
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def get_module_directory(toml_file_path='pyproject.toml'):
    with open(toml_file_path, 'r', encoding='utf-8') as file:
        toml_data = toml.load(file)
    try:
        packages = toml_data.get('tool', {}).get(
            'poetry', {}).get('packages', {})
        for package in packages:
            if module_directory := package.get('include'):
                return Path(module_directory)
    except KeyError as e:
        print(f"Error accessing TOML data: {e}")
        return None


class MyHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = self._create_process()

    def on_any_event(self, event):
        """Handle all file system events. """
        if self.should_restart(event):
            click.secho(f"File {event.src_path} modified, restart server", fg='green')
            print(f"Detected {event.event_type} event on {event.src_path}")
            self.restart_process()

    def should_restart(self, event):
        """Check if the event is a file change event. """
        if "__pycache__" in event.src_path:
            return False
        return event.event_type in ['modified', 'created', 'deleted']

    def _create_process(self):
        """Create a new process. """
        return subprocess.Popen(self.command, shell=True, preexec_fn=os.setsid)

    def restart_process(self):
        """Restart the process by killing the process group and starting a new one."""
        if self.process.poll() is None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
        self.process = self._create_process()

@click.command()
@click.option('--toml', default='pyproject.toml', help='Path to the TOML file.')
@click.option('--verbose', is_flag=True, help='Enable verbose output.')
def serve(toml, verbose):
    """Start the mkdocs server and restart it when a file changes. """
    command = "mkdocs serve -f docs/mkdocs.yml "
    module_dir = get_module_directory(toml).absolute()
    print(module_dir)
    if verbose:
        command += "--verbose"
    event_handler = MyHandler(command)
    observer = Observer()
    observer.schedule(event_handler, module_dir, recursive=True)
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


if __name__ == "__main__":
    serve()  # pylint: disable=no-value-for-parameter
