#!/bin/bash

log_script="scripts/log_listener.py"
log_file_chat="logs/world2.chat"
log_file_format="logs/world2.formatlog"
log_file="logs/world2.log"
read_from_start="true"

base_folder=$(pwd)
export PYTHONPATH="$base_folder"

process_log_line() {
    local log_line="$1"
    if [ -f "$log_script" ]; then
        python "$log_script" "$log_line" 2>>run.log
    else
        echo "Error: $log_script not found." >&2
        exit 1
    fi
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
read_log_file "$log_file" &