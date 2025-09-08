import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src import semantic_indexer

class SpreadsheetEventHandler(FileSystemEventHandler):
    """Handles events for spreadsheet files."""
    def on_modified(self, event):
        
        if not event.is_directory and event.src_path.endswith('.xlsx'):
            print(f"--- Detected change in: {event.src_path} ---")
            
            semantic_indexer.delete_index_for_file(event.src_path)
            
            print(f"--- Triggering re-indexing for: {event.src_path} ---")
            semantic_indexer.create_index_from_spreadsheet(event.src_path)
            
            print(f"--- Re-indexing complete. Ready for new searches. ---")

if __name__ == "__main__":
    path = "./data"
    event_handler = SpreadsheetEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print(f" Starting file watcher on directory: '{path}'")
    print("Watching for changes in .xlsx files... (Press Ctrl+C to stop)")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()