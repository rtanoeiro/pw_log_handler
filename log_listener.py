import os
from config import LOG_PATTERNS, REGEX_PATTERNS
import sys
import re
import datetime

class LogHandler:

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.regex_patterns = REGEX_PATTERNS
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
                    function(log_line=log_line, function=func_name)
                else:
                    print(f"Method {func_name} not found or is not callable")
                return
        print("Pattern doesn't match any method")

    def processExpSP(self, log_line: str, function: str):
        regex = self.regex_patterns[function]
        matches = self.regexMatch(regex, log_line)
        roleid = matches[0][0]
        exp = matches[0][1]
        sp = matches[0][2]
        print(f"Role ID: {roleid} received {exp} EXP and {sp} SP at {self.now}")

    def processPickupMoney(self, log_line: str, function: str):
        regex = self.regex_patterns[function]
        matches = self.regexMatch(regex, log_line)
        roleid = matches[0][0]
        money = matches[1][1]
        print(f"Role ID: {roleid} picked up {money} money at {self.now}")
        return self.now, roleid, money
    
    def processTask(self, log_line: str, function: str):
        regex = self.regex_patterns[function]
        matches = self.regexMatch(regex, log_line)
        roleid = matches[0][0]
        task = matches[0][1]
        print(f"Role ID: {roleid} completed the task {task} at {self.now}")
        return self.now, roleid, task

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        log_line = "2024-10-06 21:52:43 pwtestes.com gamed: info : 用户1024得到经验 27/6"
        #log_line = sys.argv[1]
        log_handler.processLogLine(log_line=log_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
