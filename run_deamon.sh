#!/bin/bash
file=$1
n1=$2
n2=$3
for sub_file in `ls ${file}_*`; do
    echo $sub_file
    python debug_jsonl.py $sub_file && mv temp_fix.jsonl $sub_file
done 



for i in $(seq $n1 $n2); do
    python gemini_chat.py $i "${file}.jsonl" &

done

wait
sleep 180s 

