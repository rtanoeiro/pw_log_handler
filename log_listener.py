import os
from config import LOG_PATTERNS
import sys
import re
import datetime

class LogHandler:

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.now = timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def processLogLine(self, log_line: str):
        print(f"Processing log line: {log_line}")
        self.getMethod(log_line)
        return None

    def regexMatch(self, regex_expression: str, log_line: str):
        matches = re.findall(regex_expression, log_line)
        return matches

    def getMethod(self, log_line: str):
        for pattern, func_name in self.log_patterns.items():
            if pattern in log_line:
                print(f"Pattern matched: {pattern}")
                function = getattr(self, func_name, None)
                if callable(function):
                    function(log_line)
                else:
                    print(f"Method {func_name} not found or is not callable")
                return
        print("Pattern doesn't match any method")

    def processExpSP(self, log_line: str):
        regex = r"(\d+)(?=经验)|(\d+)(?=灵气)|(\d+)(?=\s*$)"
        matches = self.regexMatch(regex, log_line)
        print("Processing EXP/SP gain...")
        print(f"Matches: {matches}")

    def processPickupMoney(self, log_line: str):
        regex = r"(\d+)(?=拣起金钱)|(\d+)(?=\s*$)"
        matches = self.regexMatch(regex, log_line)
        roleid = matches[0][0]
        money = matches[1][1]
        print(f"Role ID: {roleid} picked up {money} money at {timestamp}")
        return self.now, roleid, money

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_handler = LogHandler()
        log_line = sys.argv[1]
        log_handler.processLogLine(log_line=log_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
