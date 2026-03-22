import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .parser import stream_new_lines
from .extractor import ErrorExtractor
from .ai import AIService
from .formatter import Formatte

class LogWatcher(FileSystemEventHandler)
    def __init__(self, file_path: Path, ai_service: AIService, extractor: ErrorExtractor):
        self.file_path = file_path
        self.ai_service = ai_service
        self.extractor = extractor
        self.last_position = file_path.stat().st_size
        self.buffer = []

    def on_modified(self, event):
        if event.src_path == str(self.file_path.resolve()):
            self.process_new_content()

    def process_new_content(self):
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(self.last_position)
            new_lines = f.readlines()
            self.last_position = f.tell()
            
            if not new_lines:
                return

            errors = self.extractor.extract_errors(new_lines)
            for error in errors:
                Formatter.print_header("New Error Detected in Watch Mode")
                analysis = self.ai_service.analyze_error(error['content'])
                Formatter.print_analysis(analysis)

def start_watching(file_path: Path, ai_service: AIService, extractor: ErrorExtractor):
    """
    Starts the file watcher loop.
    """
    event_handler = LogWatcher(file_path, ai_service, extractor)
    observer = Observer()
    observer.schedule(event_handler, path=str(file_path.parent), recursive=False)
    observer.start()
    
    Formatter.print_info(f"Watching {file_path}... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        Formatter.print_info("Stopped watching.")
    observer.join()
