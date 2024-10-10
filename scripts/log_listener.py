"""This is the main script for the processing of the log file"""

import re
import sys
from typing import Any

from scripts.config import LOG_PATTERNS, REGEX_PATTERNS


class LogHandler:
    """
    This class handle the processing of the log file.
    It's called in log_listener.sh script for each new log line that is written to the log files.
    The line is then routed into it's corresponding method based on the log_patterns dictionary.
    """

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.regex_patterns = REGEX_PATTERNS

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

        return None

    def process_login(self, log_line: str, function: str):
        """
        Function called when the player logs in
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            userid = matches.group(2)
            roleid = matches.group(3)
        print(f"User ID {userid} with Role {roleid} logged in at {date_time}")
        return date_time, userid, roleid

    def process_logout(self, log_line: str, function: str):
        """
        Function called when the player logs out
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            userid = matches.group(2)
            roleid = matches.group(3)
        print(f"User ID {userid} with Role {roleid} logged out at {date_time}")
        return date_time, userid, roleid

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
            return self.process_task_receive_item(log_line, function="process_task_receive_item")
        elif "DeliverByAwardData" in log_line:
            return self.process_task_receive_reward(log_line, function="process_task_receive_reward")

    def process_task_receive_item(self, log_line: str, function: str):
        """
        Function called when the player gives up on a task
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
            itemid = matches.group(4)
            item_count = matches.group(5)
        print(
            f"Role ID {roleid} received {item_count} units of item ID {itemid} from task ID {taskid} at {date_time}"
        )
        return date_time, roleid, taskid, itemid, item_count

    def process_task_receive_reward(self, log_line: str, function: str):
        """
        Function called when the player receives an item via task
        Arguments:
            log_line -- Log line to be processed
            roleid -- Role that received item
            taskid -- Task that gave item
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            taskid = matches.group(3)
            gold = matches.group(4)
            exp = matches.group(5)
            sp = matches.group(6)
            reputation = matches.group(7)
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

    def process_kill_person(self, log_line: str, function: str):
        """
        Function called when the player kills another player
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            killer = matches.group(2)
            victim = matches.group(3)
        print(f"Role ID {killer} killed Role ID {victim} at {date_time}")

        return date_time, killer, victim

    def process_gshop_trade(self, log_line: str, function:str):
        """
        Function called when the player trades in the gshop
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            itemid = matches.group(3)
            item_count = matches.group(4)
            price = matches.group(5)
            cash_needed = matches.group(6)
            cash_left = matches.group(7)
        print(f"Role ID {roleid} traded {item_count} unit(s) of item ID {itemid} for {price} at {date_time}, cash used: {cash_needed}, cash left: {cash_left}")

        return date_time, roleid, itemid, item_count, price, cash_needed, cash_left

    def process_drop_item(self, log_line: str, function: str):
        """
        Function called when the player drops an item
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
        print(f"Role ID {roleid} dropped {item_count} item ID {itemid} at {date_time}")

        return date_time, roleid, item_count, itemid

    def process_drop_equipment(self, log_line: str, function:str):
        """
        Function called when the player drops an equipment
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            itemid = matches.group(3)
        print(f"Role ID {roleid} dropped equipment ID {itemid} at {date_time}")

        return date_time, roleid, itemid


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        current_line = sys.argv[1]
        log_handler.process_log_line(log_line=current_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
