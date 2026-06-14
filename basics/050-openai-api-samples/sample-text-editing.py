# sample-text-editing.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

bio_text = """
Alex Smith is a software engineer.
He works as a backend developer.
"""

prompt = f"""
Update the biography.

Change:
- Alex Smith to Jordan Lee
- software engineer to data analyst
- backend developer to business analyst

Biography:
{bio_text}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
