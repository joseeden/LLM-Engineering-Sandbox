# sys-msg-role-based.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = "You are a customer support agent."

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": "My order has not arrived."
        }
    ]
)

print(response.content[0].text)
