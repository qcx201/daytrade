#!/bin/bash
session=$1


# https://unix.stackexchange.com/a/481042
screen -ls $session | grep -E '\s+[0-9]+\.' | awk -F ' ' '{print $1}' | while read s; do screen -XS $s quit; done
echo "Killed sessions with name \"$session\""
