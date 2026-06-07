# sample-text-summarization.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

chat_transcript = """
Customer: My order has not arrived.
Support: Let me check the shipment status.
Customer: Thank you.
Support: The package was delayed and will arrive tomorrow.
"""

prompt = f"""
Summarize the following customer support conversation in 2 sentences.

Conversation:
{chat_transcript}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
