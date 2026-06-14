# sys-msg-constraint-based.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = "Respond with exactly 3 bullet points."

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=100,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": "Benefits of backups"
        }
    ]
)

print(response.content[0].text)
