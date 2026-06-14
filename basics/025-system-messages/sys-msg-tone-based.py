# sys-msg-tone-based.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = "Use an enthusiastic tone."

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": "Tell me about cloud computing."
        }
    ]
)

print(response.content[0].text)
