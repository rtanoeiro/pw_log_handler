"""This module contains configurations such as function names and regex patterns for the log handler"""

LOG_PATTERNS = {
    "GM:": "processGMActions",
    "chat :": "processChat",
    "formatlog:sendmail": "processSendMail",
    # Missing added auction itens and purchase from auction
    "formatlog:rolelogin": "process_login",  # done
    "formatlog:rolelogout": "process_logout",  # done
    "formatlog:trade": "process_trade",  # done
    "formatlog:task": "process_task",  # done
    "formatlog:die": "process_kill_person",  # done
    "formatlog:faction": "process_faction",  # done
    "formatlog:upgradefaction": "process_upgrade_faction",  # done
    "formatlog:gshop_trade": "process_gshop_trade",  # done
    "建立了队伍": "process_create_party",  # done
    "成为队员": "process_join_party",  # done
    "脱离队伍": "process_leave_party",  # done
    "丢弃包裹": "process_drop_item",  # done
    "丢弃装备": "process_drop_equipment",  # done
    "拣起金钱": "process_pick_up_money",  # done
    "丢弃金钱": "process_discard_money",  # done
    "卖店": "process_sell_item",  # done
    "得到金钱": "process_receive_money",  # done
    "拣起": "process_pick_item",  # done
    "升级到": "process_level_up",  # done
    "花掉金钱": "process_spend_money",  # done
    "消耗了sp": "process_spend_sp",  # done
    "技能": "process_upgrade_skill",  # done
    "制造了": "process_craft_item",  # done
    "采集得到": "process_mine",  # done
    "孵化了宠物蛋": "process_egg_hatch",  # done
    "还原了宠物蛋": "processPetEggRestore",  # waiting for log line
    "组队拣起用户": "pickupTeamMoney",  # Waiting for log line
    "得到经验": "process_exp_sp",  # done
}

REGEX_PATTERNS = {
    "startActivity": "GM %d started the activity %d.",
    "stopActivity": "GM %d stopped the activity %d.",
    "toggleInvincibility": "GM %d toggled invincibility state. Current state : %d.",
    "toggleInvisibility": "GM %d toggled invisibility state. Current state : %d.",
    "dropMonsterSpawner": "GM %d dropped monster spawner with ID : %d.",
    "playerDisconnect": "Player %d was disconnected. Disconnect type : %d.",
    "activateTrigger": "GM %d activated the trigger %d.",
    "cancelTrigger": "GM %d canceled the trigger %d.",
    "createMonster": "GM %d created %d monster(s) of type %d and ID %d,",
    "attemptMoveToPlayer": "GM %d attempted to move to player %d.",
    "moveToPlayer": "GM %d moved to player %d at position (%f, %f, %f).",
    "movePlayer": "GM %d moved player %d to position (%f, %f, %f).",
    "command": "The GM with Role ID %d executed internal command %d.",
    # Missing kicking from faction?
    "process_mine": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*? 用户(\d+)采集得到(\d+)个(\d+)",
    "process_create_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):factionid=(\d+)",
    "process_upgrade_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?factionid=(\d+):master=(\d+):money=(\d+):level=(\d+)",
    "process_join_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s.*roleid=(?P<roleid>\d+):factionid=(?P<factionid>\d+)",
    "process_promote_in_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?type=promote:superior=(\d+):roleid=(\d+):factionid=(\d+):role=(\d+)",
    "process_leave_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?type=leave:roleid=(\d+):factionid=(\d+):role=\d+",
    "process_delete_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?type=delete:factionid=(\d+)",
    "process_create_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)建立了队伍\((\d+),\d+\)",
    "process_join_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)成为队员\((\d+),\d+\)",
    "process_leave_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)脱离队伍\((\d+),\d+\)",
    "process_egg_hatch": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)孵化了宠物蛋(\d+)",
    "petEggRestore": "The Role ID %d restored a pet and received the pet egg ID %d.",
    "process_craft_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)",
    "process_kill_person": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):type=258:.*attacker=(\d+)",
    "process_spend_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)花掉金钱(\d+)",
    "process_spend_sp": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)消耗了sp (\d+)",
    "process_upgrade_skill": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)技能(\d+)达到(\d+)级",
    "sendMail": "Timestamp: %d, The Role ID %d just sent a mail to role ID %d. Mail ID: %d. Mail size: %d. Money sent: %d. Item ID: %d. Item count: %d. Mail position: %d.",
    "process_logout": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):roleid=(\d+):.*time=(\d+)",
    "process_login": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):roleid=(\d+)",
    "process_drop_equipment": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃装备(\d+)",
    "process_drop_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃包裹(\d+)个(\d+)",
    "process_pick_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)拣起(\d+)个(\d+)",
    "purchaseFromAuction": "The Role ID %d purchased %d item(s) from gshop, spent %d unit(s) of cash, remaining balance: %d",
    "process_trade_add_itens": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+),goods is \(id=(\d+),pos=\d+,count=(\d+)\),money=(\d+),tid=(\d+)",
    "process_trade_remove_itens": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) .*? roleid=(\d+),item \(id=(\d+),pos=\d+,count=(\d+)\),money=(\d+),tid=(\d+)",
    "process_trade_submit": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*rid=(\d+),A:(\d+),B:(\d+),.*tid=(\d+)",
    "process_trade_save": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*tid=(\d+),\(Trader:(\d+),(\d+)\)",
    # Missing trading cancel?
    "pickupTeamMoney": "Role ID %d picked up money (%d) dropped by Role ID %d they both were in a Party.",
    "process_pick_up_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)拣起金钱(\d+)",
    "process_discard_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃金钱(\d+)",
    "process_sell_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)卖店(\d+)个(\d+)",
    "process_receive_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)得到金钱(\d+)",
    "process_task": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+)",
    "process_task_receive_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+).*Item id = (\d+), Count = (\d+)",
    "process_task_receive_reward": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+).*gold\s*=\s*(\d+),\s*exp\s*=\s*(\d+),\s*sp\s*=\s*(\d+),\s*reputation\s*=\s*(\d+)",
    "process_level_up": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)升级到(\d+)级金钱(\d+),游戏时间(\d+:\d{2}:\d{2})",
    "process_gshop_trade": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):.*order_id=(\d+):item_id=(\d+):.*item_count=(\d+):cash_need=(\d+):cash_left=(\d+)",
    "process_exp_sp": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)得到经验 (\d+)/(\d+)",
}
