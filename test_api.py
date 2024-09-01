import requests
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
import requests
import random

#session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(10))

#API_KEY = "AIzaSyCEpyQ7hELkIQOVUQNG4e6qBLIkhyiJUpA"
API_KEY = sys.argv[1]
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" +  API_KEY
text = "Generate 5 high-quality and diverse questions and answers pairs requiring complex reasoning and only based on below context, just ask around questions around context, don't include redundant info like 'this file or this report or this document ...', ask directly. \n\nContext:  Arriving on your vacation, you are dismayed to\nlearn that the local weather service forecasts a\n50% chance of rain every day this week. What\n are the chances of 3 consecutive rainy days?\n\n##Question 1:\nWhat is the probability of having at least one rainy day this week?\n\n##Answer 1:\n1 - (0.5)^7 = 0.9922 (approximately 99.2%)\n\n##Question 2:\nWhat is the probability of having exactly 3 rainy days this week?\n\n##Answer 2:\n(0.5)^3 * (0.5)^4 = 0.03125 (approximately 3.1%)\n\n##Question 3:\nWhat is the probability of having a rainy day on the first day and a dry day on the second day?\n\n##Answer 3:\n(0.5) * (0.5) = 0.25 (25%)\n\n##Question 4:\nWhat is the probability of having a dry day on the first day and a rainy day on the second day?\n\n##Answer 4:\n(0.5) * (0.5) = 0.25 (25%)\n\n##Question 5:\nWhat is the probability of having a rainy day on the first day, a dry day on the second day, and a rainy day on the third day?\n\n##Answer 5:\n(0.5) * (0.5) * (0.5) = 0.125 (12.5%)\n\nContext: 41086.01500\n\n | Signature Tower I, LLC Signature Tower 2, LLC | (1)\n | Signature Tower 3, LLC | (1)\n | The Signature Condominiums, LLC | (1)\n | Tower B, LLC | (1)\n | Tower C, LLC | (1)\n | Vdara Condo Hotel, LLC | (1)\n | Vendido, LLC | (1)\n | VidiAd | (1)\n | Vintage Land Holdings, LLC | (1)\n##Question 1:\n"
headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [{
        "parts": [
            {"text": text}
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

response = requests.post(url, headers=headers, json=data)
#response_json = await resp.json()
print(response)
print("Rewrite\n", response.json()['candidates'][0]['content']['parts'][0]['text'])

