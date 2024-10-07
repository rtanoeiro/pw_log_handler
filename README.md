Each log file is responsible for different logging capabilities. Below is a summary of each one:

1. World2Cash
    This contains cash purchases made in the Gold Store. But it doesn't contain who purchased it. So not useful.
1. World2.Chat
    This contains chat messages sent in the server. It's useful to read. All messages are written in Base64 format.
2. World2.formatlog
    This file seems to some of the things we'll need for monitoring. It contains TaskDelivery/Receive, Gold Spending, death logs, login/logout, play time, etc
3. World2.log
    This seems to contain most of the things we'll need. Though not formatted as the .formatlog file, but it should contain crafted, dropped itens, party creation/join, equipment/money drop, sp spent, and so on...