#!/bin/bash
# usage: save_p3.sh <label> -- copy newest list_folder tool result to phase3/list/<label>-pNN.json; print count/more/cursor
D=/home/user/panda/foxyprinting-rebrand/exports/dropbox-mask-sort/phase3/list; mkdir -p $D
f=$(ls -t /root/.claude/projects/-home-user-panda/*/tool-results/mcp-Dropbox-list_folder-*.txt | head -1)
n=$(ls $D/$1-p*.json 2>/dev/null | wc -l); n=$((n+1)); out=$(printf "%s/%s-p%02d.json" $D $1 $n)
cp "$f" "$out"; jq -r '"\(.entries|length) more=\(.has_more)\n\(.cursor)"' "$out"
