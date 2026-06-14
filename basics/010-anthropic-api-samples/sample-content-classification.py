# sample-content-classification.py
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

messages = [
    "My app crashes when I try to upload a photo",
    "I forgot my password and cannot log in",
    "The app feels very slow after the update"
]

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": f"""
                Classify each message into one of these categories:
                - Bug report
                - Account issue
                - Performance issue

                Messages:
                {messages}

                Return the result as a simple numbered list.
                """
        }
    ]
)

print(response.content[0].text)
