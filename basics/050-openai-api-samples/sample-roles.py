# sample-roles.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "You are a Python tutor who answers in one short sentence."
    },

    {
        "role": "user",
        "content": "What is a loop in Python?"
    },
    {
        "role": "assistant",
        "content": "A loop repeats a block of code multiple times."
    },

    {
        "role": "user",
        "content": "Explain functions in Python."
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(response.choices[0].message.content)
