import jsonlines
import sys

acc = 0 
not_acc = 0
refuse = 0 
total = 0
for line in jsonlines.open(sys.argv[1]):
    result = line['rewrite_response'] 
    if "1" in result:
        acc += 1
    elif "2" in result:
        not_acc += 1
    elif "3" in result:
        refuse += 1 
        print(line['Response'], line['Answer'])
    total += 1 

print("Acc. :", acc/total*100, not_acc/total*100, refuse/total*100)
