# thinking-mode-strategy-planning.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1500,
    thinking={
        "type": "enabled",
        "budget_tokens": 1024
    },
    messages=[
        {
            "role": "user",
            "content": "Create a launch strategy for a new fitness app entering multiple countries"
        }
    ]
)

print(response.content)
