"""This module contains configurations such as function names and regex patterns for the log handler"""

LOG_PATTERNS = {
    "GM:": "processGMActions",
    "chat :": "processChat",
    "formatlog:sendmail": "processSendMail",  # Waiting for log line
    "formatlog:rolelogin": "process_login",  # done
    "formatlog:rolelogout": "process_logout",  # done
    "formatlog:trade": "processTrade",  # Waiting for log line
    "formatlog:task": "process_task",  # done
    "formatlog:die": "process_kill_person",  # done
    "formatlog:faction": "process_create_faction",  # done
    "formatlog:upgradefaction": "process_upgrade_faction",  # done
    "formatlog:gshop_trade": "process_gshop_trade",  # done
    "建立了队伍": "process_create_party",  # done
    "成为队员": "process_join_party",  # done
    "脱离队伍": "process_leave_party",  # done
    "丢弃包裹": "process_drop_item",  # done
    "丢弃装备": "process_drop_equipment",  # done
    "拣起金钱": "process_pick_up_money",  # done
    "丢弃金钱": "process_discard_money",  # done
    "卖店": "process_sell_item", #done
    "得到金钱": "process_receive_money", # done
    "拣起": "processPickupItem",
    "升级到": "processLevelUp",
    "花掉金钱": "processSpendMoney",
    "消耗了sp": "processSpConsume",
    "技能": "processSkillLevelUp",
    "制造了": "process_craft_item",  # done
    "采集得到": "process_mine",  # done
    "孵化了宠物蛋": "processPetEggHatch",
    "还原了宠物蛋": "processPetEggRestore",
    "组队拣起用户": "pickupTeamMoney",
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
    "process_mine": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*? 用户(\d+)采集得到(\d+)个(\d+)",
    "process_create_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):factionid=(\d+)",
    "process_upgrade_faction": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?factionid=(\d+):master=(\d+):money=(\d+):level=(\d+)",
    "deleteFaction": "(Action type: %s) An attempt to delete the faction ID %d was detected!",
    "joinFaction": "(Type: %s) The Role ID %d joined the Faction ID %d",
    "promoteRoleInFaction": "(Type: %s) The Role ID %d was promoted by his superior (ID %d) in Faction ID %d. New position: %d",
    "deleteRoleFromFaction": "(Type: %s) Role with ID %d was deleted from Faction ID %d. Role: %d",
    "leaveFaction": "(Type: %s) The Role ID %d just left the Faction ID %d, his position was: %d",
    "pickupTeamMoney": "Role ID %d picked up money (%d) dropped by Role ID %d they both were in a Party.",
    "process_create_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)建立了队伍\((\d+),\d+\)",
    "process_join_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)成为队员\((\d+),\d+\)",
    "process_leave_party": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)脱离队伍\((\d+),\d+\)",
    "petEggHatch": "The Role ID %d hatched the pet egg ID %d.",
    "petEggRestore": "The Role ID %d restored a pet and received the pet egg ID %d.",
    "process_craft_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+).*?(\d+)",
    "process_kill_person": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):type=258:.*attacker=(\d+)",
    "spendMoney": "The Role ID %d spent %d money.",
    "spConsume": "The Role ID %d consumed %d sp.",
    "skillLevelUp": "The Role ID %d leveled up the skill ID %d to level %d.",
    "sendMail": "Timestamp: %d, The Role ID %d just sent a mail to role ID %d. Mail ID: %d. Mail size: %d. Money sent: %d. Item ID: %d. Item count: %d. Mail position: %d.",
    "process_logout": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):roleid=(\d+):.*time=(\d+)",
    "process_login": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):roleid=(\d+)",
    "process_drop_equipment": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃装备(\d+)",
    "process_drop_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃包裹(\d+)个(\d+)",
    "pickupItem": "The Role ID %d picked up %d unit(s) of item %d (discarded by role ID %d)",
    "purchaseFromAuction": "The Role ID %d purchased %d item(s) from gshop, spent %d unit(s) of cash, remaining balance: %d",
    "trade": "Role %d traded with role %d. Money exchanged: %d from role %d and %d from role %d. Role %d traded %s items. And Role %d traded %s items.",
    "process_pick_up_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)拣起金钱(\d+)",
    "process_discard_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)丢弃金钱(\d+)",
    "process_sell_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)卖店(\d+)个(\d+)",
    "process_receive_money": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*用户(\d+)得到金钱(\d+)",
    "process_task": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+)",
    "process_task_receive_item": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+).*Item id = (\d+), Count = (\d+)",
    "process_task_receive_reward": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*roleid=(\d+):taskid=(\d+).*gold\s*=\s*(\d+),\s*exp\s*=\s*(\d+),\s*sp\s*=\s*(\d+),\s*reputation\s*=\s*(\d+)",
    "levelUp": "The Role ID %d leveled up to level %d. Current money: %s. Playtime: %s.",
    "process_gshop_trade": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*userid=(\d+):.*order_id=(\d+):item_id=(\d+):.*item_count=(\d+):cash_need=(\d+):cash_left=(\d+)",
    "process_exp_sp": r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?用户(\d+)得到经验 (\d+)/(\d+)",
}
