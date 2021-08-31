from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 

class FileModified(FileSystemEventHandler):
    def dispatch(self, event):
        if event.src_path == pathToWatch and event.event_type == "modified":
                conf.loadConfig()

    