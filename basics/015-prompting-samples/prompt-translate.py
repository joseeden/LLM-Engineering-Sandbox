# prompt-translate.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    temperature=0,
    messages=[
        {"role": "user", "content": "Good morning -> Bonjour"},
        {"role": "assistant", "content": "Got it"},
        {"role": "user", "content": "Thank you -> Merci"},
        {"role": "assistant", "content": "Got it"},
        {"role": "user", "content": "Translate: Good night"}
    ]
)

print(response.content[0].text)
