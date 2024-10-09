"""This script is run to perform all tests from log lines"""

import unittest
from pw_logger.log_listener import LogHandler


class TestLogs(unittest.TestCase):
    """
    Class to hold all tests from log lines
    """

    def setUp(self):
        self.exp_sp_log = (
            "2024-10-06 21:52:43 pwtestes.com gamed: info : 用户1024得到经验 27/6"
        )
        self.pickup_money_log = (
            "2024-09-21 08:23:24 pwtestes.com gamed: info : 用户1028拣起金钱9"
        )
        self.receive_task = "2024-09-23 08:29:26 pwtestes.com gamed: notice : formatlog:task:roleid=1088:taskid=6436:type=1:msg=CheckDeliverTask"
        self.give_up_task = "2024-09-24 08:03:33 pwtestes.com gamed: notice : formatlog:task:roleid=1120:taskid=33582:type=1:msg=GiveUpTask"
        self.receive_xp_task = "2024-09-24 08:01:17 pwtestes.com gamed: notice : formatlog:task:roleid=1088:taskid=6437:type=1:msg=DeliverByAwardData: success = 1, gold = 8100, exp = 13500, sp = 3000, reputation = 2"
        self.receive_item_task = "2024-09-24 08:01:17 pwtestes.com gamed: notice : formatlog:task:roleid=1088:taskid=6437:type=1:msg=DeliverItem: Item id = 3366, Count = 1"
        self.mine_item = (
            "2024-09-21 08:23:02 pwtestes.com gamed: info : 用户1028采集得到2个1837"
        )
        self.craft_item = "2024-09-24 18:28:03 pwtestes.com gamed: info : 用户1104制造了5个11330, 配方1275, 消耗材料1823, 数量10; 材料1830, 数量15;"
        self.handler = LogHandler()

    def test_exp_sp_log(self):
        """
        Test if the exp_sp log line is correctly processed
        """
        results = self.handler.process_log_line(self.exp_sp_log)
        self.assertEqual(results, (self.handler.now, "1024", "27", "6"))

    def test_pickup_money_log(self):
        """
        Test if the pickup money log line is correctly processed
        """
        results = self.handler.process_log_line(self.pickup_money_log)
        self.assertEqual(results, (self.handler.now, "1028", "9"))

    def test_receive_task(self):
        """
        Test if the receive task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_task)
        self.assertEqual(results, (self.handler.now, "1088", "6436", "receive"))

    def test_task_give_up(self):
        """
        Test if the give up task log line is correctly processed
        """
        results = self.handler.process_log_line(self.give_up_task)
        self.assertEqual(results, (self.handler.now, "1120", "33582", "give_up"))

    def test_receive_xp_task(self):
        """
        Test if the receive xp task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_xp_task)
        self.assertEqual(
            results, (self.handler.now, "1088", "6437", "8100", "13500", "3000", "2")
        )

    def test_receive_item_task(self):
        """
        Test if the receive item task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_item_task)
        self.assertEqual(results, (self.handler.now, "1088", "6437", "3366", "1"))

    def test_mine_item(self):
        """
        Test if the mine item log line is correctly processed
        """
        results = self.handler.process_log_line(self.mine_item)
        self.assertEqual(results, (self.handler.now, "1028", "2", "1837"))

    def test_craft_item(self):
        """
        Test if the craft item log line is correctly processed
        """
        results = self.handler.process_log_line(self.craft_item)
        self.assertEqual(
            results,
            (
                self.handler.now,
                "1104",
                "5",
                "11330",
                "1275",
                "1823",
                "10",
                "1830",
                "15",
            ),
        )
