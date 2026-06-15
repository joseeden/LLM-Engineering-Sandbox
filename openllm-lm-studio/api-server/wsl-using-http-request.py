# wsl-using-http-request.py

import json
import os

import requests

from dotenv import load_dotenv

load_dotenv()


LM_STUDIO_BASE_URL = os.getenv(
    "LM_STUDIO_BASE_URL"
)

MODEL_NAME = os.getenv("MODEL_NAME")

response = requests.post(
    f"{LM_STUDIO_BASE_URL}/v1/chat/completions",
    json={
        "model": MODEL_NAME,
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
