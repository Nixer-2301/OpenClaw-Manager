import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtCore import QObject, pyqtSignal


class ConfigFileHandler(QObject, FileSystemEventHandler):
    config_changed = pyqtSignal(str)

    def __init__(self, config_path):
        QObject.__init__(self)
        FileSystemEventHandler.__init__(self)
        self.config_path = Path(config_path)

    def on_modified(self, event):
        if not event.is_directory:
            event_path = Path(event.src_path)
            if event_path == self.config_path:
                self.config_changed.emit(str(event_path))

    def on_created(self, event):
        if not event.is_directory:
            event_path = Path(event.src_path)
            if event_path.parent == self.config_path.parent:
                self.config_changed.emit(str(event_path))


class SkillsFileHandler(QObject, FileSystemEventHandler):
    skills_changed = pyqtSignal()

    def __init__(self, skills_dirs):
        QObject.__init__(self)
        FileSystemEventHandler.__init__(self)
        self.skills_dirs = [Path(d) for d in skills_dirs]

    def on_created(self, event):
        self._check_skills_dir(event)

    def on_deleted(self, event):
        self._check_skills_dir(event)

    def on_modified(self, event):
        if not event.is_directory:
            self._check_skills_dir(event)

    def _check_skills_dir(self, event):
        event_path = Path(event.src_path)
        for skills_dir in self.skills_dirs:
            if skills_dir in event_path.parents or event_path == skills_dir:
                self.skills_changed.emit()
                break


class FileWatcher(QObject):
    config_changed = pyqtSignal(str)
    skills_changed = pyqtSignal()

    def __init__(self, config_path, skills_dirs):
        super().__init__()
        self.observer = Observer()
        self.config_handler = ConfigFileHandler(config_path)
        self.config_handler.config_changed.connect(self.config_changed.emit)

        self.skills_handler = SkillsFileHandler(skills_dirs)
        self.skills_handler.skills_changed.connect(self.skills_changed.emit)

        self._setup_watchers(config_path, skills_dirs)

    def _setup_watchers(self, config_path, skills_dirs):
        config_dir = Path(config_path).parent
        if config_dir.exists():
            self.observer.schedule(self.config_handler, str(config_dir), recursive=False)

        for skills_dir in skills_dirs:
            skills_path = Path(skills_dir)
            if skills_path.exists():
                self.observer.schedule(self.skills_handler, str(skills_path), recursive=True)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def is_running(self):
        return self.observer.is_alive()
