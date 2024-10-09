#!/bin/bash


pwlogger_pid=$(pidof -x log_listener.sh)

if [ -n "$pwlogify_pid" ]; then
    echo "Stopping pwlogger process (PID: $pwlogger_pid)"
    kill $pwlogify_pid
else
    echo "No pwlogger process found."
fi
