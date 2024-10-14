#!/bin/bash
script_path="log_listener.sh"
pwlogger_pid=$(pidof -x $(basename -- "$script_path"))

if [ -n "$pwlogger_pid" ]; then
    echo "Logger is already running (PID: $pwlogger_pid)"
else
    echo "Starting pwlogger"
    cd $(dirname -- "$script_path")
    nohup "$script_path" > /dev/null 2> logs/start_error.log &
fi
