import jsonlines
import json
import argparse
from tqdm.auto import tqdm
import requests
def process(content):
    #global fail_streak
    if True:
        #API_KEY = "AIzaSyAqGJG0_NtCXzyB5hCcoSy-QTOYU1jpuMA"
        API_KEY = "AIzaSyDo7DTaM8MCyuz-nYhmXtunjj6vK6US3MA"
        #print(content['instruction'])
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

        headers = {
            "Content-Type": "application/json"
        }

#        data = {
#            "contents": [{
#              "parts":[{
#                "text": content}]}]}
        
        data = {
            "contents": [{
                "parts": [
                    {"text": content['instruction']}
                ]
            }],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                }
            ],
            "generationConfig": {
                "stopSequences": [
                    "Title"
                ],
                "temperature": 0.0001,
                "maxOutputTokens": 4096,
                "topP": 0.9,
                "topK": 50
            }
        }
        #SET QUOTA here
#        if progress_log.done > 2000:
#            print("Quota")
#            return
        if True:
            with requests.post(url, headers=headers, data=json.dumps(data)) as resp:
                #printt("???", resp)
                response_json = resp.json()
                try:
                    output = response_json['candidates'][0]['content']['parts'][0]['text']
                    content['rewrite_response'] = output
                    content['status'] = "success"
                    #fail_streak = 0
                    return content
                    #writer.write(content)

                except:
                    #fail_streak += 1
                    
                    #print(content['instruction'])
                    #time.sleep(3)
                    content['response'] = content['instruction']
                    content['status'] = "Fail"
                    return content
        else:
              #writer = jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
              #fail_streak += 1
              #print("failing streak ", fail_streak)
              #print(content['instruction'])
              #time.sleep(3)
              content['response'] = content['instruction']
              content['status'] = "Fail"
              return content
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, help='input jsonlines file')
parser.add_argument('-o', '--output', required=True, help='output jsonlines file')
parser.add_argument('-v', '--valid', required=True, help='output jsonlines file')   
parser.add_argument('-t', '--type', required=True, help='output jsonlines file')
args = parser.parse_args()
fail_count = 0 
fail = 0
type = args.type
with jsonlines.open(args.input) as reader, jsonlines.open(args.output, 'w') as writer, jsonlines.open(args.valid, 'w') as valid_writer:
    for line in tqdm(reader):
        ##condition for evaluatio
        if type == 'qgen':
            if line['status'] == 'success' and line['rewrite_response'].split()[-1].strip() in ["ĐÚNG", "SAI"]:
                valid_writer.write(line)
            elif line['status'] == 'success' and  ("ĐÚNG" in line['rewrite_response'] or "SAI" in line['rewrite_response']) and not ("ĐÚNG" in line['rewrite_response'] and "SAI" in line['rewrite_response']):
                valid_writer.write(line)
            
        elif type == 'llava':
            if line['status'] == 'success' and ("1" in line['rewrite_response'] or "0" in line['rewrite_response']):
                valid_writer.write(line)
                    ##condititon for augmentation        
        #if line['status'] == 'success' and "<Đoạn văn>" not in line and "<Câu hỏi" == line['rewrite_response'].split(">")[0]:
            #valid_writer.write(line)
        #no condition
        elif line['status'] == 'success':
            valid_writer.write(line)
        else:
            if line['status'] != 'success':
                fail += 1 
                print(line['status'])
                continue
#            retry = 3
#            status = False
#            while retry > 0:
#                retry -= 1
#                line = process(line)
#                if line['status'] == 'success' and line['rewrite_response'] in ["0", "1"]:
#                    valid_writer.write(line)
#                    status = True
#                    break
#            if status == True:
#                continue 
#            writer.write(line)
            fail_count += 1
            if fail_count == 1:
               print(line['rewrite_response'], line['status'])

print("Fail count: ", fail_count, fail)   
              
