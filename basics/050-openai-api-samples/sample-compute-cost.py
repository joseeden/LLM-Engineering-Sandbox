# sample-compute-cost.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

max_completion_tokens = 500

prompt = """
Summarize the following customer support conversation:

Customer: I cannot log in.
Support: Please reset your password.
Customer: That fixed it.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_completion_tokens=max_completion_tokens
)

input_token_price = 0.15 / 1_000_000
output_token_price = 0.60 / 1_000_000

input_tokens = response.usage.prompt_tokens
output_tokens = max_completion_tokens

cost = (
    input_tokens * input_token_price
    + output_tokens * output_token_price
)

print(f"Input tokens: {input_tokens}")
print(f"Estimated cost: ${cost:.8f}")
