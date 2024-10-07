stdbuf -oL tail -f -n0 world2.chat | while read line; do
    echo "$line"
done