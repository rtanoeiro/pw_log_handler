#!/bin/bash

log_script="log_listener.py"
log_file="world2.chat"

process_log_line() {
    local log_line="$1"
    python "${log_script}" "${log_line}" 2>>errors.log
}

stdbuf -oL tail -f -n0 $log_file | while read line; do
    process_log_line "$line"
done