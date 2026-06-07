# sample-text-generation.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

prompt = """
Write a product description for SonicPro headphones.

Features:
- Active noise cancellation
- 40-hour battery life
- Foldable design

Tone:
Professional and engaging

Audience:
Travelers and remote workers
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_completion_tokens=400,
    temperature=0.5
)

print(response.choices[0].message.content)
