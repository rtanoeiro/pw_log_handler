#!/bin/bash

pwlogger_pid=$(pidof -x log_listener.sh)

if [ -n "$pwlogger_pid" ]; then
    echo "Stopping pwlogger process (PID: $pwlogger_pid)"
    kill $pwlogger_pid
else
    echo "No pwlogger process found."
fi
