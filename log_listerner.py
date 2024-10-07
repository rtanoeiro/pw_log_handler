import os

LOG_FILE = "world2.log"
LAST_READ_LINE = os.environ["LAST_READ_LINE"]
MAX_LINES = 1000

def read_log_lines(file_to_read) -> list:
    with open(file_to_read, "r", encoding='gb2312') as file:
        lines = file.readlines()[int(LAST_READ_LINE) : MAX_LINES]
        return lines


last_lines = read_log_lines(file_to_read=LOG_FILE)

with open("last_line.env", "w") as file:
    last_line_string = f"LAST_READ_LINE={str(MAX_LINES + int(LAST_READ_LINE))}"
    file.write(str(last_line_string))

for line in last_lines:
    print(line)
