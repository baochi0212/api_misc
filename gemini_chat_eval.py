import sys
import os
import asyncio
import aiohttp
import json
import jsonlines
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import random
from tqdm import tqdm
import requests
keys = [key.strip() for key in open("./all_valid_key_eval").readlines()]
idx = int(sys.argv[1])
input_file = sys.argv[2]
print("Chosen idx: ", idx)
jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
passed = len([i for i in jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl")])
#omit_indx = open(f"./omit/{input_file.split('.')[0]}_{idx}_omit.txt", "a")
print("Passed lines:", passed)
API_KEY = keys[idx]
fail_streak = 0
def condition(line):
    #If no condition
    return True
    if "1" in line or "0" in line and not ("1" in line and "0" in line):
        return True
    #If evaluate
    if ("ĐÚNG" in line['rewrite_response'] or "SAI" in line['rewrite_response']) and not ("ĐÚNG" in line['rewrite_response'] and "SAI" in line['rewrite_response']):
        return True
    if line['rewrite_response'].split()[-1] in ["ĐÚNG", "SAI"]:
        return True
    #If augmentation
    #if "<Câu hỏi" == line['rewrite_response'].split(">")[0] and "<Câu hỏi>" in line['rewrite_response'] and "<Câu trả lời>" in line['rewrite_response'] and "<Giải thích>" in line['rewrite_response'] and "<Đoạn văn>" not in line['rewrite_response']: 
        #return True
    return False
def process(content, temp):
    #global fail_streak
    if True:
        #API_KEY = "AIzaSyAqGJG0_NtCXzyB5hCcoSy-QTOYU1jpuMA"
        #API_KEY = "AIzaSyDo7DTaM8MCyuz-nYhmXtunjj6vK6US3MA"
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
                "temperature": temp,
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
                    content['rewrite_response'] = content['instruction']
                    content['status'] = f"Fail {API_KEY}"
                    return content
        else:
              #writer = jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
              #fail_streak += 1
              #print("failing streak ", fail_streak)
              #print(content['instruction'])
              #time.sleep(3)
              content['rewrite_response'] = content['instruction']
              content['status'] = f"Fail {API_KEY}" 
              return content
def get_completion(content):
    global fail_streak
    if True:
        #API_KEY = "AIzaSyAqGJG0_NtCXzyB5hCcoSy-QTOYU1jpuMA"
        #print(content['instruction'])
        time.sleep(random.randint(0, 2))
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
                "temperature": 0.01,
                "maxOutputTokens": 4096,
                "topP": 0.9,
                "topK": 50
            }
        }        
        #SET QUOTA here
#        if progress_log.done > 2000:
#            print("Quota")
#            return
        writer = jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
        try:
            with requests.post(url, headers=headers, data=json.dumps(data)) as resp:
                #printt("???", resp) 
#                writer = jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
                response_json = resp.json()
                try:
                    output = response_json['candidates'][0]['content']['parts'][0]['text']
                    content['rewrite_response'] = output
                    content['status'] = "success"
                    fail_streak = 0
                
                    
                    
                except:
                    #print(content['instruction'])
                    content['rewrite_response'] = content['instruction']
                    content['status'] = f"Fail {idx}"
#                    writer.write(content)
                    print(content['instruction'], response_json)
        except:
#              writer = jsonlines.open(f"./{input_file.split('.')[0]}_{idx}.jsonl", "a")
#              fail_streak += 1
#              print("failing streak ", fail_streak)
              #print(content['instruction'])
              #time.sleep(3)
              content['rewrite_response'] = content['instruction']
              content['status'] = f"Fail {idx}"
              writer.write(content)
        if content['status'] != 'success' or not condition(content):
             
            retry = 5
            temp = 0.01
            status = False
            while retry > 0:
                temp = temp*(6-retry)
                print(f"Retry for {retry} times, with temp {temp}", idx)
                retry -= 1
                time.sleep(0.5)
                line = process(content, temp)
                if line['status'] == 'success' and condition(line):
                    writer.write(line)
                    status = True
                    break
            if status == True:
                return
            fail_streak += 1
            print("failing streak ", fail_streak)
            writer.write(content)
        else:
            writer.write(content)
if __name__ == "__main__":
    instructions = [content for content in jsonlines.open(input_file)]
    batch_length = int(round(len(instructions)/(len(keys)-1)))
    #print("Length ", batch_length*i, batch_length*(i+1))
    batches = [instructions[batch_length*i:batch_length*(i+1)] for i in range(len(keys))]
    print("Diff", sum([len(batch) for batch in batches]), len(instructions))
    instructions = batches[idx]
    for i, content in enumerate(tqdm(instructions)):
        if fail_streak > 3:
            print("Enough fail")
            break 
        if i < passed:
            continue
        get_completion(content)        


