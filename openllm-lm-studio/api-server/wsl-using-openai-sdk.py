# using-openai-sdk.py

import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_BASE_URL = os.getenv(
    "LM_STUDIO_BASE_URL"
)

MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    base_url=f"{LM_STUDIO_BASE_URL}/v1",
    api_key="lm-studio"
)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Explain what an LLM is in 3 sentences."
        }
    ]
)

print(
    response.choices[0].message.content
)
