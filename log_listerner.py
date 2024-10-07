# Messages are in base64 format

from collections import deque
import os

LOG_FILE = "world2.log"
LAST_READ_LINE = os.environ["LAST_READ_LINE"]
LINES_PER_STREAM = 10

def read_log_lines(file_to_read) -> list:
    with open(file_to_read, "r", encoding='gb2312') as file:
        lines = file.readlines()
        return lines


last_lines = read_log_lines(file_to_read=LOG_FILE)

for line in last_lines:
    print(line)
