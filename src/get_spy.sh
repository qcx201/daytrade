#!/bin/bash

for i in {1..10}
do

    session=spy$i

    # kill screen if exists
    screen -ls $session | grep -E '\s+[0-9]+\.' | awk -F ' ' '{print $1}' | while read s; do screen -XS $s quit; done

    # start screen and detach
    screen -dmS $session
    echo "Started session <$session>"
    
    cmd="
    python3 -u get_spy.py -i $i 2>&1 | tee ../log/spy_$i.log

    screen -XS $session quit
    "

    # run script
    screen -S $session -X stuff $"$cmd\n"
    echo "Running in session <$session>"
    echo "> $cmd"

done