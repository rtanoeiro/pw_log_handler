"""This is the main script for the processing of the log file"""

import datetime
import re
import sys
from typing import Any

from scripts.config import LOG_PATTERNS, REGEX_PATTERNS, TASK_PATTERNS


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

    def process_log_line(self, log_line: str) -> tuple[Any] | None:
        """
        This function gets the correct method to process the log line.

        Arguments:
            log_line -- Log Line received by the log_listener.sh script
        """
        results = self.get_method(log_line)
        return results

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
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            exp = matches.group(3)
            sp = matches.group(4)
        print(f"Role ID {roleid} received {exp} EXP and {sp} SP at {date_time}")

        return date_time, roleid, exp, sp

    def process_pick_up_money(self, log_line: str, function: str):
        """
        Function called when the player picks up money is found in the log line
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            money = matches.group(3)
        print(f"Role ID: {roleid} picked up {money} money at {date_time}")
        return date_time, roleid, money

    def process_task(self, log_line: str, function: str):
        """
        Function called when the player interacts with tasks
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            taskid = matches.group(3)
        if "GiveUpTask" in log_line:
            print(f"Role ID {roleid} gave up task ID {taskid} at {date_time}")
            return date_time, roleid, taskid, "give_up"
        elif "CheckDeliverTask" in log_line:
            print(f"Role ID {roleid} received task ID {taskid} at {date_time}")
            return date_time, roleid, taskid, "receive"
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
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            itemid = matches.group(2)
            item_count = matches.group(3)
        print(
            f"Role ID {roleid} received {item_count} units of item ID {itemid} from task ID {taskid}"
        )
        return date_time, roleid, taskid, itemid, item_count

    def process_task_receive_reward(self, log_line: str, roleid: str, taskid: str):
        """
        Function called when the player receives an item via task
        Arguments:
            log_line -- Log line to be processed
            roleid -- Role that received item
            taskid -- Task that gave item
        """
        regex = self.task_patterns["DeliverByAwardData"]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            gold = matches.group(2)
            exp = matches.group(3)
            sp = matches.group(4)
            reputation = matches.group(5)
        print(
            f"Role ID {roleid} completed the task ID {taskid} and received as reward: gold = {gold}, exp = {exp}, sp = {sp}, reputation = {reputation}"
        )
        return date_time, roleid, taskid, gold, exp, sp, reputation

    def process_mine(self, log_line: str, function: str):
        """
        Function called when the player mines
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            item_count = matches.group(3)
            itemid = matches.group(4)
        print(
            f"Role ID {roleid} mined and obtained {item_count} unit(s) of item ID {itemid}"
        )
        return date_time, roleid, item_count, itemid

    def process_craft_item(self, log_line: str, function: str):
        """
        Function called when the player crafts an item
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            item_count = matches.group(3)
            itemid = matches.group(4)
            recipe = matches.group(5)
        print(
            f"Role ID {roleid} crafted {item_count} unit(s) of item ID {itemid} at {date_time}"
        )
        return date_time, roleid, item_count, itemid, recipe

    def process_create_faction(self, log_line: str, function: str):
        """
        Function called when the player creates a faction
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            factionid = matches.group(3)
        print(f"Role ID {roleid} created faction ID {factionid} at {date_time}")
        return date_time, roleid, factionid

    def process_upgrade_faction(self, log_line: str, function: str):
        """
        Function called when the player upgrades a faction
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            factionid = matches.group(2)
            roleid = matches.group(3)
            money = matches.group(4)
            level = str(int(matches.group(5)) + 1)
        print(
            f"Faction ID {factionid} was upgraded by the master role {roleid}. Money: {money}, Level: {level}"
        )
        return date_time, factionid, roleid, money, level

    def process_create_party(self, log_line: str, function: str):
        """
        Function called when the player creates a party
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            partyid = matches.group(3)
        print(f"Role ID {roleid} created party ID {partyid} at {date_time}")

        return date_time, roleid, partyid

    def process_join_party(self, log_line: str, function: str):
        """
        Function called when the player joins a party
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            partyid = matches.group(3)
        print(f"Role ID {roleid} joined party ID {partyid} at {date_time}")

        return date_time, roleid, partyid

    def process_leave_party(self, log_line: str, function: str):
        """
        Function called when the player leaves a party
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            partyid = matches.group(3)
        print(f"Role ID {roleid} left party ID {partyid} at {date_time}")

        return date_time, roleid, partyid


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        current_line = sys.argv[1]
        log_handler.process_log_line(log_line=current_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
