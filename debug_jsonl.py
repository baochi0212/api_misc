import jsonlines
from tqdm import tqdm
import json
import sys
writer = jsonlines.open("temp_fix.jsonl", "w")
count = 0
for line in tqdm(open(sys.argv[1]).readlines()):
    try:
        line = json.loads(line)
        writer.write(line)
    except:
        count += 1

print("Bug", count)
