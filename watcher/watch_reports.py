# pylint: disable=C0413,E0401
"""
File to watch the report_ids.txt file for changes and process new lines
"""

import asyncio
import sys
from threading import Lock

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

sys.path.append('/hai-on-hackerone/cli/')
from actions import hai_actions
from hai import send_to_hai

FILE_TO_WATCH = "/hai-on-hackerone/webserver/data/report_ids.txt"
line_count_lock = Lock()

def get_line_count(filepath):
    """ 
    Get the line count of the file
    """
    with open(filepath, 'r', encoding='UTF-8') as f:
        return sum(1 for _ in f)

initial_line_count = get_line_count(FILE_TO_WATCH)

def process_new_lines(filepath, initial_count):
    """
    Process new lines in the file
    """
    with open(filepath, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    new_lines = lines[initial_count:]
    for line in new_lines:
        report_number = line.strip()
        asyncio.run(run_python_tool(report_number))
    return len(lines)

async def run_python_tool(report_number):
    """
    Run the python tool
    """
    verbose = True
    comment_hai_flag = False
    custom_field_hai_flag = True
    csv_output_flag = False
    (
        predictedValidity,
        predictedValidityCertaintyScore,
        predictedValidityReasoning,
        predictedComplexity,
        predictedComplexityCertaintyScore,
        predictedComplexityReasoning,
        predictedOwnershipCertaintyScore,
        predictedOwnershipReasoning,
        productArea,
        squadOwner
    ) = await send_to_hai(report_number, verbose)

    hai_actions(
        predictedValidity,
        predictedValidityCertaintyScore,
        predictedValidityReasoning,
        predictedComplexity,
        predictedComplexityCertaintyScore,
        predictedComplexityReasoning,
        predictedOwnershipCertaintyScore,
        predictedOwnershipReasoning,
        productArea,
        squadOwner,
        report_number,
        comment_hai_flag,
        custom_field_hai_flag,
        csv_output_flag,
        verbose
)

class FileChangeHandler(FileSystemEventHandler):
    """
    Handle file changes
    """
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def on_modified(self, event):
        if event.src_path == self.filepath:
            global initial_line_count
            with line_count_lock:
                initial_line_count = process_new_lines(self.filepath, initial_line_count)

def monitor_file(filepath):
    """
    Monitor the file for changes and process new lines
    """
    event_handler = FileChangeHandler(filepath)
    observer = Observer()
    observer.schedule(event_handler, path=filepath, recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

if __name__ == "__main__":
    monitor_file(FILE_TO_WATCH)
