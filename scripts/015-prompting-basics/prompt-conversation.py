# prompt-conversation.py
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
            "content": "Q: Differentiate f(x) = x^2"
        },
        {
            "role": "assistant",
            "content": "A: f'(x) = 2x"
        },
        {
            "role": "user",
            "content": "Q: Differentiate f(x) = 3x^3 + 2x"
        }
    ]
)

print(response.content[0].text)
