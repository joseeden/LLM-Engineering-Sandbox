# sys-msg-vague-vs-improved.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

vague_system = "Be concise."

improved_system = """
Respond in 2 to 3 sentences.
Include relevant context.
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=200,
    system=improved_system,
    messages=[
        {
            "role": "user",
            "content": "What is Kubernetes?"
        }
    ]
)

print(response.content[0].text)
