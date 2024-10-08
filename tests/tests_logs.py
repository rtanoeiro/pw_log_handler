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
        self.test_pickup_money_log = (
            "2024-09-21 08:23:24 pwtestes.com gamed: info : 用户1028拣起金钱9"
        )
        self.receive_task = "2024-09-23 08:29:26 pwtestes.com gamed: notice : formatlog:task:roleid=1088:taskid=6436:type=1:msg=CheckDeliverTask"
        self.handler = LogHandler()

    def test_exp_sp_log(self):
        """
        Test if the exp_sp log line is correctly processed
        """
        self.assertEqual(
            self.handler.process_log_line(self.exp_sp_log),
            (self.handler.now, "1024", "27", "6"),
        )
