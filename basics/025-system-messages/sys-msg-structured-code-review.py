# sys-msg-structured-code-review.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

system_message = """
Priority 1: Security
Priority 2: Performance
Priority 3: Style

If issues are found:
- List the issues
- Suggest fixes

If no issues are found:
- Reply with "Code looks good"
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    system=system_message,
    messages=[
        {
            "role": "user",
            "content": """
Review this code:

password = "admin123"
print(password)
"""
        }
    ]
)

print(response.content[0].text)
