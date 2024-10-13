#!/bin/bash

log_script="log_listener.py"
log_file_chat="home/logs/world2.chat"
log_file_format="home/logs/world2.formatlog"
log_file="home/logs/world2.log"
read_from_start="false"
files="$log_file_chat $log_file_format $log_file"

process_log_line() {
    local log_line="$1"
    python3 "$log_script" "$log_line" 2>> logs/pw_log_handler.log
}

if [ "$read_from_start" = "true" ]; then
    if [ -f "$files" ]; then
        while read -r log_line; do
            process_log_line "$log_line"
        done <  "$files"
    fi
else
    stdbuf -oL tail -f -n0 \
    "$log_file_chat" \
    "$log_file_format" \
    "$log_file" \
    | while IFS= read -r log_line; do
        echo "Processing Raw bash: $log_line"
        process_log_line "$log_line"
    done
fi