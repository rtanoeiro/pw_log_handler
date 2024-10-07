import os
from config import LOG_PATTERNS
import sys

class LogHandler:

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS

    def processLogLine(self, log_line):
        print(f"Processing log line: {log_line}")
        self.getMethod(log_line)
        return None
    
    def getMethod(self, log_line):
        for pattern in self.log_patterns.keys():
            if pattern in log_line:
                print(f"Pattern matched: {pattern}")
                return self.log_patterns[pattern]
        return print("Pattern doesn't match any method")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_handler = LogHandler()
        log_line = sys.argv[1]
        log_handler.processLogLine(log_line=log_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
