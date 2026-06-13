import os
import json
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_FILE = BASE_DIR / "post-examples.json"


prompt_input = """
You are an expert social media manager.
Your expertise is in creating viral, highly engaging, and shareable content for various social media platforms.

Your task is to create a social media post that is concise, engaging, and tailored to the user's input.

Important guidelines to follow:

- Avoid using hashtags or emojis.
- Do not use asyndetons. Use complete sentences or conjunctions to connect ideas.
- Do not use em dash (—) that can be interpreted as an AI-generated content marker.
- Use bullet points or numbered lists to organize information when appropriate.

Keep the post structured and coherent, and use line breaks or empty lines to separate different sections of the post.

Here are some example posts:

{examples_str}

Please use the tone, language style, and formatting from the examples above as a reference when creating the social media post.
DO NOT copy the content from the examples.

Here is the user's input: {topic}
"""


def load_examples() -> str:
    with open(EXAMPLES_FILE, "r", encoding="utf-8") as f:
        examples = json.load(f)

    posts = []

    for index, item in enumerate(examples, start=1):
        post_text = "\n".join(item["post"])
        posts.append(f"<example-{index}>\n{post_text}\n</example-{index}>")

    return "\n\n".join(posts)


def generate_post(topic: str) -> str:
    examples_str = load_examples()

    prompt = prompt_input.format(
        examples_str=examples_str,
        topic=topic,
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text


def main():
    user_input = input("What do you want to post about? ")
    socmed_post = generate_post(user_input)

    print("\nGenerated social media post:\n")
    print(socmed_post)


if __name__ == "__main__":
    main()
