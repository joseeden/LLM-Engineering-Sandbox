# chatbot.py

from openai import OpenAI
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_BASE_URL = os.getenv(
    "LM_STUDIO_BASE_URL"
)
MODEL_NAME = os.getenv("MODEL_NAME")


client = OpenAI(
    base_url=f"{LM_STUDIO_BASE_URL}/v1",
    api_key="something-doesnt-matter",
)


print("Chat with the local model (type 'quit' to exit)")

while True:
    user_input = input("> ")
    if user_input.lower() == "quit":
        break

    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                        "content": user_input
            }],
            stream=True,
            temperature=0.7,
        )

        print("AI: ", end="")
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
                sys.stdout.flush()
        print()

    except Exception as e:
        print(f"An error occurred: {e}")

print("Exiting chat.")
