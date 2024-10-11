"""This script is run to perform all tests from log lines"""

import unittest
from scripts.log_listener import LogHandler


class TestLogs(unittest.TestCase):
    """
    Class to hold all tests from log lines
    """

    def setUp(self):
        self.login = "2024-10-06 20:42:05 pwtestes.com glinkd-1: notice : formatlog:rolelogin:userid=1072:roleid=1041:lineid=1:localsid=147"
        self.logout = "2024-10-06 21:40:07 pwtestes.com glinkd-1: notice : formatlog:rolelogout:userid=1072:roleid=1041:localsid=147:time=3481"
        self.exp_sp = (
            "2024-10-06 21:52:43 pwtestes.com gamed: info : 用户1024得到经验 27/6"
        )
        self.pickup_money = (
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
        self.create_faction = "2024-10-06 03:10:54 pwtestes.com gamedbd: notice : formatlog:faction:type=create:roleid=1024:factionid=1"
        self.upgrade_faction = "2024-10-06 03:11:10 pwtestes.com gamedbd: notice : formatlog:upgradefaction:factionid=1:master=1024:money=194154706:level=1"
        self.create_party = (
            "2024-09-27 15:46:15 pwtestes.com gamed: info : 用户1104建立了队伍(1104,0)"
        )
        self.join_party = "2024-09-27 15:46:15 pwtestes.com gamed: info : 用户1184成为队员(1104,1727463280)"
        self.leave_party = "2024-09-27 16:08:46 pwtestes.com gamed: info : 用户1104脱离队伍(1104,1727463280)"
        self.kill_person = "2024-10-06 20:43:36 pwtestes.com gamed: notice : formatlog:die:roleid=1041:type=258:attacker=1024"
        self.gshop_purchase = "2024-10-02 18:54:40 pwtestes.com gamed: notice : formatlog:gshop_trade:userid=1056:db_magic_number=1056:order_id=17:item_id=21508:expire=1730501681:item_count=1:cash_need=750000:cash_left=98649800:guid1=0:guid2=0"
        self.drop_item = "2024-09-22 13:31:20 pwtestes.com gamed: info : 用户1072丢弃包裹1个154"
        self.drop_equipament = "2024-10-06 22:14:40 pwtestes.com gamed: info : 用户1024丢弃装备6212"
        self.discard_money = "2024-10-10 17:27:46 pwtestes.com gamed: info : 用户1024丢弃金钱200000"
        self.sell_item = "2024-09-22 01:41:36 pwtestes.com gamed: info : 用户1029卖店1个154"
        self.receive_money = "2024-09-22 03:33:47 pwtestes.com gamed: info : 用户1088得到金钱26"
        self.pickup_item = "2024-09-22 03:37:29 pwtestes.com gamed: info : 用户1088拣起100个410"
        self.handler = LogHandler()

    def test_login_log(self):
        """
        Test if the login log line is correctly processed
        """
        results = self.handler.process_log_line(self.login)
        self.assertEqual(results, ("2024-10-06 20:42:05", "1072", "1041"))

    def test_logout_log(self):
        """
        Test if the logout log line is correctly processed
        """
        results = self.handler.process_log_line(self.logout)
        self.assertEqual(results, ("2024-10-06 21:40:07", "1072", "1041"))

    def test_exp_sp_log(self):
        """
        Test if the exp_sp log line is correctly processed
        """
        results = self.handler.process_log_line(self.exp_sp)
        self.assertEqual(results, ("2024-10-06 21:52:43", "1024", "27", "6"))

    def test_pickup_money_log(self):
        """
        Test if the pickup money log line is correctly processed
        """
        results = self.handler.process_log_line(self.pickup_money)
        self.assertEqual(results, ("2024-09-21 08:23:24", "1028", "9"))

    def test_receive_task(self):
        """
        Test if the receive task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_task)
        self.assertEqual(results, ("2024-09-23 08:29:26", "1088", "6436", "receive"))

    def test_task_give_up(self):
        """
        Test if the give up task log line is correctly processed
        """
        results = self.handler.process_log_line(self.give_up_task)
        self.assertEqual(results, ("2024-09-24 08:03:33", "1120", "33582", "give_up"))

    def test_receive_xp_task(self):
        """
        Test if the receive xp task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_xp_task)
        self.assertEqual(
            results,
            ("2024-09-24 08:01:17", "1088", "6437", "8100", "13500", "3000", "2"),
        )

    def test_receive_item_task(self):
        """
        Test if the receive item task log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_item_task)
        self.assertEqual(results, ("2024-09-24 08:01:17", "1088", "6437", "3366", "1"))

    def test_mine_item(self):
        """
        Test if the mine item log line is correctly processed
        """
        results = self.handler.process_log_line(self.mine_item)
        self.assertEqual(results, ("2024-09-21 08:23:02", "1028", "2", "1837"))

    def test_craft_item(self):
        """
        Test if the craft item log line is correctly processed
        """
        results = self.handler.process_log_line(self.craft_item)
        self.assertEqual(
            results,
            ("2024-09-24 18:28:03", "1104", "5", "11330", "1275"),
        )

    def test_create_faction(self):
        """
        Test if the create faction log line is correctly processed
        """
        results = self.handler.process_log_line(self.create_faction)
        self.assertEqual(results, ("2024-10-06 03:10:54", "1024", "1"))

    def test_upgrade_faction(self):
        """
        Test if the upgrade faction log line is correctly processed
        """
        results = self.handler.process_log_line(self.upgrade_faction)
        self.assertEqual(
            results, ("2024-10-06 03:11:10", "1", "1024", "194154706", "2")
        )

    def test_create_party(self):
        """
        Test if the create party log line is correctly processed
        """
        results = self.handler.process_log_line(self.create_party)
        self.assertEqual(results, ("2024-09-27 15:46:15", "1104", "1104"))

    def test_join_party(self):
        """
        Test if the join party log line is correctly processed
        """
        results = self.handler.process_log_line(self.join_party)
        self.assertEqual(results, ("2024-09-27 15:46:15", "1184", "1104"))

    def test_leave_party(self):
        """
        Test if the leave party log line is correctly processed
        """
        results = self.handler.process_log_line(self.leave_party)
        self.assertEqual(results, ("2024-09-27 16:08:46", "1104", "1104"))

    def test_kill_person(self):
        """
        Test if the kill person log line is correctly processed
        """
        results = self.handler.process_log_line(self.kill_person)
        self.assertEqual(results, ("2024-10-06 20:43:36", "1041", "1024"))

    def test_gshop_purchase(self):
        """
        Test if the gshop purchase log line is correctly processed
        """
        results = self.handler.process_log_line(self.gshop_purchase)
        self.assertEqual(
            results,
            ("2024-10-02 18:54:40", "1056", "17", "21508", "1", "750000", "98649800"),
        )

    def test_drop_item(self):
        """
        Test if the drop item log line is correctly processed
        """
        results = self.handler.process_log_line(self.drop_item)
        self.assertEqual(results, ("2024-09-22 13:31:20", "1072", "1", "154"))

    def test_drop_equipment(self):
        """
        Test if the drop equipment log line is correctly processed
        """
        results = self.handler.process_log_line(self.drop_equipament)
        self.assertEqual(results, ("2024-10-06 22:14:40", "1024", "6212"))

    def test_discard_money(self):
        """
        Test if the discard money log line is correctly processed
        """
        results = self.handler.process_log_line(self.discard_money)
        self.assertEqual(results, ("2024-10-10 17:27:46", "1024", "200000"))

    def test_sell_npc(self):
        """
        Test if the sell npc log line is correctly processed
        """
        results = self.handler.process_log_line(self.sell_item)
        self.assertEqual(results, ("2024-09-22 01:41:36", "1029", "1", "154"))

    def test_receive_money(self):
        """
        Test if the receive money log line is correctly processed
        """
        results = self.handler.process_log_line(self.receive_money)
        self.assertEqual(results, ("2024-09-22 03:33:47", "1088", "26"))

    def test_pickup_item(self):
        """
        Test if the pickup item log line is correctly processed
        """
        results = self.handler.process_log_line(self.pickup_item)
        self.assertEqual(results, ("2024-09-22 03:37:29", "1088", "100", "410"))