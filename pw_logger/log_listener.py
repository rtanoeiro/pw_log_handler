"""This is the main script for the processing of the log file"""

import datetime
import re
import sys
from typing import Any

from pw_logger.config import LOG_PATTERNS, REGEX_PATTERNS, TASK_PATTERNS


class LogHandler:
    """
    This class handle the processing of the log file.
    It's called in log_listener.sh script for each new log line that is written to the log files.
    The line is then routed into it's corresponding method based on the log_patterns dictionary.
    """

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.regex_patterns = REGEX_PATTERNS
        self.task_patterns = TASK_PATTERNS
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_log_line(self, log_line: str) -> tuple[Any] | None:
        """
        This function gets the correct method to process the log line.

        Arguments:
            log_line -- Log Line received by the log_listener.sh script
        """
        results = self.get_method(log_line)
        return results

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

    def get_method(self, log_line: str) -> tuple[Any] | None:
        """
        This function gets the correct method based in the log_patterns dictionary.
        Each key in the dictionary contains the function name.

        If the pattern is found in the log line, the function is called.

        Arguments:
            log_line -- Log Line to be processed
        """
        for pattern, func_name in self.log_patterns.items():
            if pattern in log_line:
                method = getattr(self, func_name, None)
                if method:
                    return method(log_line, func_name)  # pylint: disable=not-callable

        print("Pattern doesn't match any method")
        return None

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
        print(f"Role ID {roleid} received {exp} EXP and {sp} SP at {self.now}")

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
        money = matches[0][1]
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
        roleid = matches[0][0]
        taskid = matches[0][1]
        if "GiveUpTask" in log_line:
            print(f"Role ID {roleid} gave up task ID {taskid} at {self.now}")
            return self.now, roleid, taskid, "give_up"
        elif "CheckDeliverTask" in log_line:
            print(f"Role ID {roleid} received task ID {taskid} at {self.now}")
            return self.now, roleid, taskid, "receive"
        elif "DeliverItem" in log_line:
            return self.process_task_give_item(log_line, roleid, taskid)
        elif "DeliverByAwardData" in log_line:
            return self.process_task_receive_reward(log_line, roleid, taskid)

    def process_task_give_item(self, log_line: str, roleid: str, taskid: str):
        """
        Function called when the player gives up on a task
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.task_patterns["DeliverItem"]
        matches = self.regex_match(regex, log_line)
        print(f"Matches: {matches}")
        itemid = matches[0][0]
        item_count = matches[0][1]
        print(
            f"Role ID {roleid} received {item_count} units of item ID {itemid} from task ID {taskid}"
        )
        return self.now, roleid, taskid, itemid, item_count

    def process_task_receive_reward(self, log_line: str, roleid: str, taskid: str):
        """
        Function called when the player receives an item via task
        Arguments:
            log_line -- Log line to be processed
            roleid -- Role that received item
            taskid -- Task that gave item
        """
        regex = self.task_patterns["DeliverByAwardData"]
        matches = self.regex_match(regex, log_line)
        print(f"Matches: {matches}")
        gold = matches[0][0]
        exp = matches[0][1]
        sp = matches[0][2]
        reputation = matches[0][3]
        print(
            f"Role ID {roleid} completed the task ID {taskid} and received as reward: gold = {gold}, exp = {exp}, sp = {sp}, reputation = {reputation}"
        )
        return self.now, roleid, taskid, gold, exp, sp, reputation

    def process_mine(self, log_line: str, function: str):
        """
        Function called when the player mines
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = self.regex_match(regex, log_line)
        roleid = matches[0][0]
        item_count = matches[0][1]
        itemid = matches[0][2]
        print(
            f"Role ID {roleid} mined and obtained {item_count} unit(s) of item ID {itemid}"
        )
        return self.now, roleid, item_count, itemid

    def process_craft_item(self, log_line: str, function: str):
        """
        Function called when the player crafts an item
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = self.regex_match(regex, log_line)
        print(f"matches: {matches}")
        roleid = matches[0][0]
        item_count = matches[0][1]
        itemid = matches[0][2]
        recipe = matches[0][3]
        resource1 = matches[0][4]
        resource1_count = matches[0][5]
        resource2 = matches[0][6]
        resource2_count = matches[0][7]
        print(
            f"Role ID {roleid} crafted {item_count} unit(s) of item ID {itemid} at {self.now}"
        )
        return (
            self.now,
            roleid,
            item_count,
            itemid,
            recipe,
            resource1,
            resource1_count,
            resource2,
            resource2_count,
        )


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        current_line = sys.argv[1]
        log_handler.process_log_line(log_line=current_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
