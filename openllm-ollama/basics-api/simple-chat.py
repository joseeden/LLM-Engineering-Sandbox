# simple-chat.py
from openai import OpenAI
import sys
import os

from dotenv import load_dotenv
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="something-doesnt-matter",
    timeout=300,
)

print("Chat with the local model (type 'quit' to exit)")

messages = []

while True:
    user_input = input("> ").strip()

    if not user_input:
        continue

    if user_input.lower() == "quit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
        temperature=0.7,
    )

    assistant_response = ""

    print("AI: ", end="")

    for chunk in stream:
        if chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            assistant_response += text
            print(text, end="")
            sys.stdout.flush()

    print()

    messages.append({
        "role": "assistant",
        "content": assistant_response
    })

print("Exiting chat.")
