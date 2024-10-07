import os
from config import LOG_PATTERNS
import sys

class LogHandler:

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS

    def processLogLine(self, log_line):
        print(f"Processing log line: {log_line}")
        return None

if sys.argv == 1:
    log_handler = LogHandler()
    log_line = sys.argv[1]
    log_handler.processLogLine(log_line=log_line)
