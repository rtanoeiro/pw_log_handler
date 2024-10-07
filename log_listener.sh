$log_script = "log_listerner.py"
$log_file = "world2.log"

process_log_line() {
    local log_line=$1
    python "${logify_script}" "${log_line}" 1>/dev/null 2>> "${script_dir}/../logs/errors.txt"
}


stdbuf -oL tail -f -n0 world2.chat | while read line; do
    echo "$line"
    python3 "$log_script" "$line" 1>run.log 2>run.err
done