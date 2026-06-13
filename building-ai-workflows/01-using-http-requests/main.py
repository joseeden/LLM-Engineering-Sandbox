import requests
import os

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

prompt_input = """"
You are a expert social media manager. 
Your expertise is in creating viral, highly engaging, and shareable content for various social media platforms.

Your task is to create a social media post that is concise, engaging, and tailored to the user's input.

Important guidelines to follow: 

- Avoid using hashtags, emojis, or any platform-specific formatting. 
- Do not use asyndetons, use complete sentences or conjunctions to connect ideas.
- Do not use em dash (—) that can be interpreted as an AI-generated content marker.

Keep the post structured and coherent, and use line breaks or empty lines to separate different ideas or sections of the post.

Here is the user's input: {topic}
"""


def generate_post(topic: str) -> str:
    prompt = prompt_input.format(topic=topic)

    payload = {
        "model": MODEL_NAME,
        "input": prompt,
    }

    response = requests.post(
        OPENAI_BASE_URL,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        },
    )

    response.raise_for_status()
    data = response.json()

    return next(
        (
            part.get("text", "").strip()
            for item in data.get("output", [])
            if item.get("type") == "message"
            for part in item.get("content", [])
            if part.get("type") == "output_text"
        ),
        ""
    )


def main():
    user_input = input("What do you want to post about? ")
    socmed_post = generate_post(user_input)
    print("Generated social media post:")
    print(socmed_post)


if __name__ == "__main__":
    main()
