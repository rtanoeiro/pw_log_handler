Each log file is responsible for different logging capabilities. Below is a summary of each one:

1. World2Cash
    This contains cash purchases made in the Gold Store. But it doesn't contain who purchased it. So not useful.
1. World2.Chat
    This contains chat messages sent in the server. It's useful to read. All messages are written in Base64 format.
2. World2.formatlog
    This file seems to some of the things we'll need for monitoring. It contains TaskDelivery/Receive, Gold Spending, death logs, login/logout, play time, etc
3. World2.log
    This seems to contain most of the things we'll need. Though not formatted as the .formatlog file, but it should contain crafted, dropped itens, party creation/join, equipment/money drop, sp spent, and so on...

The idea of this project is to monitor the log file for anything interesting we want to check from players. For example, checking if the player is mining to many minerals in a short amount of time. Log kills into a database, check how money was spent by the player, which items it has crafted.

All data will be logged into a Database for easier querying and possibly usage in a Website.