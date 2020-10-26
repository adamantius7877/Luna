#! /bin/bash
command=""
for i in "$*"
do 
    command="${command}${i}"
done
echo "python3 luna.py --command \"$command\""
