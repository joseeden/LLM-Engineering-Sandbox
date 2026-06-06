# prompt-classify-sentiment.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    temperature=0,
    messages=[
        {"role": "user", "content": "Task: classify sentiment -> I love this product"},
        {"role": "assistant", "content": "Positive"},

        {"role": "user", "content": "Task: classify sentiment -> This is terrible"},
        {"role": "assistant", "content": "Negative"},

        {"role": "user", "content": "Task: classify sentiment -> It is okay"},
        {"role": "assistant", "content": "Neutral"},

        {"role": "user", "content": "Task: classify sentiment -> The product works well"}
    ]
)

print(response.content[0].text)
