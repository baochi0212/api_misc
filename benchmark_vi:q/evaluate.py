import jsonlines
import sys
import re
def round_to_nearest_0_5(num):
  """Rounds a float to the nearest 0.0 or 0.5.

  Args:
    num: The float to round.

  Returns:
    The rounded float.
  """

  distance_to_0_5 = abs(round(num) - num + 0.5)
  distance_to_0_0 = abs(num - round(num))
  #print("???", distance_to_0_5, distance_to_0_0)
  if distance_to_0_5 < distance_to_0_0:
    return round(num) + 0.5
  else:
    return round(num)

#print("???", round_to_nearest_0_5(4.3))
dict = {}
sentences = {}
pattern = r"\d/5"  # \d matches any digit

for line in jsonlines.open(sys.argv[1]):
    try:
        response = line['rewrite_response']
        #matches = re.findall(pattern, response)
        #score = float(matches[-1].split("/")[0])
        score = response.split("/5")[-2].split()[-1]
        if "*" in score:
            score = score.replace("*", "")
        score = float(score)
        if score < 1:
            score += 1
        elif score > 5:
            score = score/2
        category = line['category']
        if category in dict:
            dict[category].append(round_to_nearest_0_5(score))
        else:
            dict[category] =  [round_to_nearest_0_5(score)]
    except:
        print(line['rewrite_response'])
        #print(float(line['rewrite_response'].split("/5")[-2].split()[-1]))


for key in dict:
    print("Domain: ", key, sum(dict[key])/(5*(len(dict[key]))))
        
#print(dict['conv'])
print(dict)
