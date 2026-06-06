# prompt-one-shot.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": "Translate to French: How are you?"
        },
        {
            "role": "assistant",
            "content": "Comment ça va ?"
        },
        {
            "role": "user",
            "content": "Translate to French: How was your flight yesterday?"
        }
    ]
)

print(response.content[0].text)
