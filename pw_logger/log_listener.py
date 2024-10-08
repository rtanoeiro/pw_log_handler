"""This is the main script for the processing of the log file"""

import datetime
import re
import sys

from pw_logger.config import LOG_PATTERNS, REGEX_PATTERNS


class LogHandler:
    """
    This class handle the processing of the log file.
    It's called in log_listener.sh script for each new log line that is written to the log files.
    The line is then routed into it's corresponding method based on the log_patterns dictionary.
    """

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.regex_patterns = REGEX_PATTERNS
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_log_line(self, log_line: str):
        """
        This function gets the correct method to process the log line.

        Arguments:
            log_line -- Log Line received by the log_listener.sh script
        """
        self.get_method(log_line)
        return None

    def regex_match(self, regex_expression: str, log_line: str):
        """
        Finds all matches from a regex.

        Arguments:
            regex_expression -- Regex Expression
            log_line -- Log Line that contains the information to be extracted

        Returns:
            matches: All matches
        """
        matches = re.findall(regex_expression, log_line)
        return matches

    def get_method(self, log_line: str):
        """
        This function gets the correct method based in the log_patterns dictionary.
        Each key in the dictionary contains the function name.

        If the pattern is found in the log line, the function is called.

        Arguments:
            log_line -- Log Line to be processed
        """
        for pattern, func_name in self.log_patterns.items():
            if pattern in log_line:
                function = getattr(self, func_name, None)
                if callable(function):
                    function(log_line=log_line, function=func_name)
                else:
                    print(f"Method {func_name} not found or is not callable")
                return None
        print("Pattern doesn't match any method")

    def process_exp_sp(self, log_line: str, function: str):
        """
        Function called when exp_sp pattern is found in the log line
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = self.regex_match(regex, log_line)
        roleid = matches[0][0]
        exp = matches[0][1]
        sp = matches[0][2]
        print(f"Role ID: {roleid} received {exp} EXP and {sp} SP at {self.now}")

        return self.now, roleid, exp, sp

    def process_pick_up_money(self, log_line: str, function: str):
        """
        Function called when the player picks up money is found in the log line
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = self.regex_match(regex, log_line)
        roleid = matches[0][0]
        money = matches[1][1]
        print(f"Role ID: {roleid} picked up {money} money at {self.now}")
        return self.now, roleid, money

    def process_task(self, log_line: str, function: str):
        """
        Function called when the player interacts with tasks
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = self.regex_match(regex, log_line)
        return None


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        current_line = sys.argv[1]
        log_handler.process_log_line(log_line=current_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
