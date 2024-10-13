#!/bin/bash

base_folder=$(pwd)
log_script="$(pwd)log_listener.py"
log_file_chat="/home/logs/world2.chat"
log_file_format="/home/logs/world2.formatlog"
log_file="/home/logs/world2.log"
read_from_start="false"

export PYTHONPATH="$base_folder"

echo "This script is running inside $base_folder"
echo ""
echo ""

process_log_line() {
    local log_line="$1"
    python3 "$log_script" "$log_line" 2>> logs/pw_log_handler.log
}

read_log_file() {
    local file="$1"
    if [ "$read_from_start" = "true" ]; then
        if [ -f "$file" ]; then
            while read -r line; do
                process_log_line "$line"
            done < "$file"
        fi
    else
        stdbuf -oL tail -f -n0 "$file" | while read -r line; do
            process_log_line "$line"
        done
    fi
}

# Read all log files in parallel
read_log_file "$log_file_chat" &
read_log_file "$log_file_format" &
# read_log_file "$log_file" &