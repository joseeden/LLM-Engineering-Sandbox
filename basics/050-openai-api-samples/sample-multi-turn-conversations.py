# sample-multi-turn-conversations.py

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful IT support assistant. "
            "Provide concise and practical troubleshooting advice."
        )
    },

    {
        "role": "user",
        "content": "I can't connect to the company VPN."
    },
    {
        "role": "assistant",
        "content": (
            "Check that your internet connection is working and "
            "verify that your VPN username and password are correct."
        )
    },

    {
        "role": "user",
        "content": "My internet is working and the password is correct."
    },
    {
        "role": "assistant",
        "content": (
            "Try disconnecting and reconnecting the VPN client. "
            "If the issue continues, restart your computer."
        )
    },

    {
        "role": "user",
        "content": "I restarted my computer and now I get error code 809."
    },
    {
        "role": "assistant",
        "content": (
            "Error 809 usually indicates that the VPN connection is being "
            "blocked by a firewall or network device."
        )
    },

    {
        "role": "user",
        "content": (
            "I'm connected from a hotel Wi-Fi network. "
            "What should I check next?"
        )
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.3
)

print(response.choices[0].message.content)
