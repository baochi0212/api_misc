prefix=$1
type=$2
rm -rf temp_fix_rerun.jsonl "${prefix}_valid.jsonl" "${prefix}_final.jsonl"

#main
ls | grep "${prefix}_" | wc -l 
cat `ls | grep "${prefix}_"` >> "${prefix}_final.jsonl"
wc -l "${prefix}_final.jsonl" 
python regen_fail_request.py -i "${prefix}_final.jsonl" -o temp_fix_rerun.jsonl -v "${prefix}_valid.jsonl" -t $type
