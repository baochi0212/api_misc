import os
import requests
from multiprocessing import Pool
import random
import json
import jsonlines
from copy import deepcopy
import argparse
import time


PROMPT = """"""

KEY = [
    "AIzaSyCgpFTXOu9BaJS7RGgBmPvaq64RtI0QFLw"
]

GENERATION_COONFIG = {
    "temperature": 0.0,
    "candidateCount": 1,
    "maxOutputTokens": 2048
}

SAFE = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def api_call(input):
    key = random.choice(KEY)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}"

    headers = {
        "Content-Type": "application/json"
    }

    content = {
        "contents": [{"parts": [{"text": PROMPT.format(input['chunks']),
        "generationConfig": GENERATION_COONFIG,
        "safetySettings": SAFE
    }
    
    while True:
        response = requests.post(url, headers=headers, data=json.dumps(content))
        if response.status_code == 200:
            print(f"Pid {os.getpid()} | {response.json()}")
            break
        else:
            print("Fuck, Error encountered!!!. Waiting...")
            time.sleep(8)

    output = deepcopy(input)
    output["preference"] = response.json()

    return output

def get_win_rate(results):
    target_score = 0
    pred_score = 0
    for line in results:
        if line["target"] != line["pred"]:
            try:
                if line["preference"]["candidates"][0]["content"]["parts"][0]["text"].find("1") != -1:
                    target_score += 1
                elif line["preference"]["candidates"][0]["content"]["parts"][0]["text"].find("2") != -1:
                    pred_score += 1
            except:
                pass

    return 100*pred_score/(pred_score + target_score) 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_filename", type=str, default="./pred.jsonl", help="Prediction filename formatted in jsonl")
    parser.add_argument("--target_filename", type=str, default=None, help="Prediction filename for cross evaluation if specified")
    parser.add_argument("--response_filename", type=str, default="./response.jsonl", help="Response filename formatted in jsonl")
    parser.add_argument("--num_processes", type=int, default=16, help="Number of processes")
    args = parser.parse_args()

    inputs = []
    with jsonlines.open(args.pred_filename, mode="r") as fr:
        for line in fr:
            inputs.append(line)

    if args.target_filename:
        with jsonlines.open(args.target_filename, mode="r") as fr:
            for i, line in enumerate(fr):
                inputs[i]["target"] = line["pred"]

    with Pool(processes=args.num_processes) as pool:
        results = pool.map(api_call, inputs)

    with jsonlines.open(args.response_filename, mode="w") as fw:
        for result in results:
            fw.write(result)

    print(f"Win rate: {get_win_rate(results)}")

if __name__ == "__main__":
    main()
