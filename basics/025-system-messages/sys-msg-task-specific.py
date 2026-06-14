# sys-msg-task-specific.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = """
You are a debugging assistant.

Identify bugs.
Suggest fixes.
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": "Why does x = 1/0 fail in Python?"
        }
    ]
)

print(response.content[0].text)
