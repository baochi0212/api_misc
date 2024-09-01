import jsonlines
import sys
acc = 0
n_sample = 0
reader = jsonlines.open(sys.argv[1])
list = []
bug_writer = jsonlines.open("./bug_writer.jsonl", "w")
for line in reader:
    if line['instruction'] in list:
        print(line)
        continue
    else:
        list.append(line['instruction'])
    if "1" in line['rewrite_response']:
        #print(line)
        acc += 1
    if "Fail" in line['status']:
        bug_writer.write({"instruction": line['instruction']})

    n_sample +=  1
print("Unique: ", len(list))
print("Acc. :", (acc+5)/3538)
