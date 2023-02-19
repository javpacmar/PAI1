import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.event_type == 'modified' and not event.src_path.endswith(".hash") and not event.src_path.endswith(".mac"):
            print(f"File {event.src_path} has been modified")

            # Change the hash file
            with open(f"{event.src_path}", "r") as f:
                data = f.read()
                hash = hashlib.sha1(data.encode()).hexdigest()
                with open(f"{event.src_path}.hash", "w") as f:
                    f.write(str(hash))


def run_server():
    print("Starting server...")
    path = './cloud/'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Server started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
