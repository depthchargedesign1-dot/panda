#!/bin/bash
# usage: save.sh <prefix>  -- copies newest tool-result list_folder file into raw/<prefix>-pNN.json, prints count/more/cursor
D=/home/user/panda/foxyprinting-rebrand/exports/dropbox-mask-sort/raw; mkdir -p $D
f=$(ls -t /root/.claude/projects/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/tool-results/mcp-Dropbox-list_folder-*.txt | head -1)
n=$(ls $D/$1-p*.json 2>/dev/null | wc -l); n=$((n+1)); out=$(printf "%s/%s-p%02d.json" $D $1 $n)
cp "$f" "$out"; jq -r '"\(.entries|length) more=\(.has_more)\n\(.cursor)"' "$out"; echo "$out"
