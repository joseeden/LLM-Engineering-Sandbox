# chatbot-multi-turn.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

messages = [
    {
        "role": "system",
        "content": "You are a helpful math tutor that speaks concisely."
    }
]

# Multiple user inputs (simulating a real conversation)
user_msgs = [
    "Explain what pi is.",
    "Give a simple example of pi in real life.",
    "Summarize pi in two bullet points."
]

# Loop through each user question
for q in user_msgs:
    print("User:", q)

    # Add user message to conversation history
    messages.append({"role": "user", "content": q})

    # Send full conversation to the model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_completion_tokens=120
    )

    # Extract assistant reply
    reply = response.choices[0].message.content

    # Store assistant reply back into memory
    messages.append({"role": "assistant", "content": reply})

    print("Assistant:", reply, "\n")
