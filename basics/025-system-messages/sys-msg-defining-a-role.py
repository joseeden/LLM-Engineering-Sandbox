# sys-msg-defining-a-role.py
#
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = """
You are a technical writer.

Write in active voice.
Keep responses under 100 words.
Provide actionable advice.
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": "How can I improve API documentation?"
        }
    ]
)

print(response.content[0].text)
