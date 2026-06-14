# sample-system-guardrails.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {
        "role": "system",
        "content": (
            "You are a finance education assistant. "
            "You must NOT provide real financial or investment advice. "
            "If asked, respond by saying you cannot give financial advice."
        )
    },
    {
        "role": "user",
        "content": "Should I invest all my savings into tech stocks?"
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.2
)

print(response.choices[0].message.content)
