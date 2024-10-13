"""This is the main script for the processing of the log file"""

import re
import sys
from typing import Any, Union

from config import LOG_PATTERNS, REGEX_PATTERNS


class LogHandler:
    """
    This class handle the processing of the log file.
    It's called in log_listener.sh script for each new log line that is written to the log files.
    The line is then routed into it's corresponding method based on the log_patterns dictionary.
    """

    def __init__(self) -> None:
        self.log_patterns = LOG_PATTERNS
        self.regex_patterns = REGEX_PATTERNS

    def process_log_line(self, log_line: str) -> Union[tuple[Any], None]:
        """
        This function gets the correct method to process the log line.

        Arguments:
            log_line -- Log Line received by the log_listener.sh script
        """
        results = self.get_method(log_line)
        if results:
            self.write_to_file(results, "logs/log.txt")

        return results

    def get_method(self, log_line: str) -> Union[tuple[Any], None]:
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

    def write_to_file(self, results: tuple[Any], file_name: str):
        """
        This function is responsible for writing the results into a log file.
        """        

        with open(file_name, "a") as file:
            file.write(f"{log_line}\n")

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
        # TODO: Find a better method to give correct func name
        elif "DeliverItem" in log_line:
            return self.process_task_receive_item(
                log_line, function="process_task_receive_item"
            )
        elif "DeliverByAwardData" in log_line:
            return self.process_task_receive_reward(
                log_line, function="process_task_receive_reward"
            )

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

    def process_faction(self, log_line: str, function: str):
        """
        Function called when the player interacts with factions
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """

        if "type=create" in log_line:
            return self.process_create_faction(
                log_line, function="process_create_faction"
            )
        elif "type=join" in log_line:
            return self.process_join_faction(log_line, function="process_join_faction")
        elif "type=promote" in log_line:
            return self.process_promote_in_faction(
                log_line, function="process_promote_in_faction"
            )
        elif "type=leave" in log_line:
            return self.process_leave_faction(
                log_line, function="process_leave_faction"
            )
        if "type=delete" in log_line:
            return self.process_delete_faction(
                log_line, function="process_delete_faction"
            )

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

    def process_join_faction(self, log_line: str, function: str):
        """
        Function called when the player joins a faction
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        print(f"Regex: {regex}")
        if matches:
            print(f"MATCHES: {matches} \n\n\n\n")
            date_time = matches.group(1)
            roleid = matches.group(2)
            factionid = matches.group(3)
            print(f"Role ID {roleid} joined faction ID {factionid} at {date_time}")
            return date_time, roleid, factionid

    def process_promote_in_faction(self, log_line: str, function: str):
        """
        Function called when the player promotes a role in a faction
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            superior = matches.group(2)
            roleid = matches.group(3)
            factionid = matches.group(4)
            role = matches.group(5)
            new_role = self.get_role_name(role)
            print(
                f"Role ID {superior} promoted Role ID {roleid} to role {role} in faction ID {factionid} at {date_time}"
            )
            return date_time, superior, roleid, factionid, role, new_role

    def get_role_name(self, role: str) -> str:
        """
        Function to get the role name based on the role id
        Arguments:
            role -- Role ID
        """

        if role == "2":
            return "Marechal"
        elif role == "3":
            return "General"
        elif role == "4":
            return "Major"
        elif role == "5":
            return "Capitão"
        elif role == "6":
            return "Membro"
        return "Unknown"

    def process_leave_faction(self, log_line: str, function: str):
        """
        Function called when the player deletes a role from a faction
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
            print(f"Role ID {roleid} left faction ID {factionid} at {date_time}")
            return date_time, roleid, factionid

    def process_delete_faction(self, log_line: str, function: str):
        """
        Function called when the player deletes a faction
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            factionid = matches.group(2)
            print(f"Faction ID {factionid} was deleted at {date_time}")
            return date_time, factionid

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

    def process_gshop_trade(self, log_line: str, function: str):
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
            print(
                f"Role ID {roleid} traded {item_count} unit(s) of item ID {itemid} for {price} at {date_time}, cash used: {cash_needed}, cash left: {cash_left}"
            )

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
            print(
                f"Role ID {roleid} dropped {item_count} item ID {itemid} at {date_time}"
            )

            return date_time, roleid, item_count, itemid

    def process_drop_equipment(self, log_line: str, function: str):
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

    def process_discard_money(self, log_line: str, function: str):
        """
        Function called when the player discards money
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
            print(f"Role ID {roleid} discarded {money} money at {date_time}")

            return date_time, roleid, money

    def process_sell_item(self, log_line: str, function: str):
        """
        Function called when the player sells an item. Unfortunately, the log line
        does not contain the item price.
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
                f"Role ID {roleid} sold {item_count} unit(s) of item ID {itemid} at {date_time}"
            )

            return date_time, roleid, item_count, itemid

    def process_receive_money(self, log_line: str, function: str):
        """
        Function called when the player receives money
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
            print(f"Role ID {roleid} received {money} money at {date_time}")

            return date_time, roleid, money

    def process_pick_item(self, log_line: str, function: str):
        """
        Function called when the player picks up an item
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
                f"Role ID {roleid} picked up {item_count} item ID {itemid} at {date_time}"
            )

            return date_time, roleid, item_count, itemid

    def process_level_up(self, log_line: str, function: str):
        """
        Function called when the player levels up
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            level = matches.group(3)
            _ = matches.group(4)
            playtime = matches.group(5)
            print(
                f"Role ID {roleid} leveled up to {level} at {date_time} after playing for {playtime} minutes"
            )

            return date_time, roleid, level, playtime

    def process_spend_money(self, log_line: str, function: str):
        """
        Function called when the player spends money
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
            print(f"Role ID {roleid} spent {money} money at {date_time}")

            return date_time, roleid, money

    def process_spend_sp(self, log_line: str, function: str):
        """
        Function called when the player spends sp
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            sp = matches.group(3)
            print(f"Role ID {roleid} spent {sp} SP at {date_time}")

            return date_time, roleid, sp

    def process_upgrade_skill(self, log_line: str, function: str):
        """
        Function called when the player upgrades a skill
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            skillid = matches.group(3)
            level = matches.group(4)
            print(
                f"Role ID {roleid} upgraded skill ID {skillid} to level {level} at {date_time}"
            )

            return date_time, roleid, skillid, level

    def process_egg_hatch(self, log_line: str, function: str):
        """
        Function called when the player hatches an egg
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            roleid = matches.group(2)
            eggid = matches.group(3)
            print(f"Role ID {roleid} hatched egg ID {eggid} at {date_time}")

            return date_time, roleid, eggid

    def process_trade(self, log_line: str, function: str):
        """
        Function called when the player trades with another player
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """

        if "tradeaddgoods" in log_line:
            return self.process_trade_add_itens(
                log_line, function="process_trade_add_itens"
            )
        elif "traderemovegoods" in log_line:
            return self.process_trade_remove_itens(
                log_line, function="process_trade_remove_itens"
            )
        elif "tradesubmit" in log_line:
            return self.process_trade_submit(log_line, function="process_trade_submit")
        elif "TradeSave" in log_line:
            return self.process_trade_save(log_line, function="process_trade_save")

    def process_trade_add_itens(self, log_line: str, function: str):
        """
        Function called when the player adds items to the trade window
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
            money = matches.group(5)
            trade_id = matches.group(6)
            print(
                f"Role ID {roleid} added {item_count} unit(s) of item ID {itemid} to trade ID {trade_id} at {date_time}"
            )

            return date_time, roleid, itemid, item_count, money, trade_id

    def process_trade_remove_itens(self, log_line: str, function: str):
        """
        Function called when the player removes items from the trade window
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
            money = matches.group(5)
            trade_id = matches.group(6)
            print(
                f"Role ID {roleid} removed {item_count} unit(s) of item ID {itemid} from trade ID {trade_id} at {date_time}"
            )

            return date_time, roleid, itemid, item_count, money, trade_id

    def process_trade_submit(self, log_line: str, function: str):
        """
        Function called when the player submits the trade
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """

        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            role_id = matches.group(2)
            roleid_a = matches.group(3)
            roleid_b = matches.group(4)
            trade_id = matches.group(5)
            print(
                f"Role ID {roleid_a} submitted the trade with Role ID {roleid_b} at {date_time}"
            )

            return date_time, role_id, roleid_a, roleid_b, trade_id

    def process_trade_save(self, log_line: str, function: str):
        """
        Function called when the player saves the trade
        Arguments:
            log_line -- Log Line
            function -- Log Line called, it's used to get the regex pattern
        """
        regex = self.regex_patterns[function]
        matches = re.search(regex, log_line)
        if matches:
            date_time = matches.group(1)
            trade_id = matches.group(2)
            roleid_a = matches.group(3)
            roleid_b = matches.group(4)
            print(
                f"Trade ID {trade_id} was saved by Role ID {roleid_a} and Role ID {roleid_b} at {date_time}"
            )

            return date_time, trade_id, roleid_a, roleid_b


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        log_handler = LogHandler()
        current_line = sys.argv[1]
        log_handler.process_log_line(log_line=current_line)
    else:
        print("Nothing done, no log line provided.")
        sys.exit(0)
