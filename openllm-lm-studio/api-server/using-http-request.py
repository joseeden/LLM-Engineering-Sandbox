# using-http-request.py

import json
import os

import requests

from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_BASE_URL = "http://localhost:1234"

response = requests.post(
    f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
    json={
        "model": os.getenv("MODEL_NAME"),
        "messages": [
            {
                "role": "user",
                "content": "Explain what an LLM is in 3 sentences."
            }
        ]
    },
    timeout=180
)

response.raise_for_status()

print(
    response.json()["choices"][0]["message"]["content"]
)
