# prompt-customer-support.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    temperature=0,
    messages=[
        {"role": "user", "content": "Customer: My order is late."},
        {"role": "assistant", "content": "We’re sorry for the delay. We are checking your order status and will update you soon."},

        {"role": "user", "content": "Customer: I received the wrong item."},
        {"role": "assistant", "content": "We apologize for the mistake. We will arrange a replacement immediately."},

        {"role": "user", "content": "Customer: My payment was charged twice."}
    ]
)

print(response.content[0].text)
