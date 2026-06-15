# using-openai-sdk.py

import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_BASE_URL = "http://localhost:1234"

client = OpenAI(
    base_url=f"{LM_STUDIO_BASE_URL}/v1",
    api_key="lm-studio"
)

response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=[
        {
            "role": "user",
            "content": "Explain what an LLM is in 3 sentences."
        }
    ]
)

print(response.choices[0].message.content)
