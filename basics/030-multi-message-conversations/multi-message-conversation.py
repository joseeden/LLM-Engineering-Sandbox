# multi-message-conversation.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

conversation_history = [
    {"role": "user", "content": "Help me plan a blog strategy"},
    {"role": "assistant", "content": "Sure, what audience are you targeting?"},
    {"role": "user", "content": "Beginners in tech"}
]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    messages=conversation_history + [
        {"role": "user", "content": "Now create a 1-week content plan"}
    ]
)

print(response.content[0].text)
