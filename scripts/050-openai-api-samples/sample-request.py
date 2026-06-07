import os
from dotenv import load_dotenv
from openai import OpenAI

# Load env vars from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "user", "content": "Explain what an API is in simple terms"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(response.choices[0].message.content)
