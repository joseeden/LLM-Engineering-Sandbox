# multi-message-iterative-conversation.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

conversation_history = [
    {
        "role": "user",
        "content": "I want to start a blog about tech"
    },
    {
        "role": "assistant",
        "content": "Good idea. What is your target audience?"
    },
    {
        "role": "user",
        "content": "Beginners who want to learn programming"
    },
    {
        "role": "assistant",
        "content": "Got it. Do you want help with topics or structure?"
    },
    {
        "role": "user",
        "content": "Help me design a 2-week content plan"
    }
]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=conversation_history + [
        {
            "role": "user",
            "content": "Now create a simple 2-week blog schedule with daily topics"
        }
    ]
)

print(response.content[0].text)
