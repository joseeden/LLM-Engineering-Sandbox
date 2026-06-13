import os
import json
import requests

from pathlib import Path
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")


client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_FILE = BASE_DIR / "post-examples.json"


prompt_extract = """"
You are an expert web content extractor. Your task is to extract the core content from a given HTML page.
The core content should be the main text, excluding navigation, footers, and other non-essential elements like scripts etc.

Please extract the core content and return it as plain text.

Here is the user's input: {html}
"""

prompt_summarize = """
You are an expert summarizer. 

Your task is to summarize the provided content into a concise and clear summary.

Please provide a brief summary of the main points in the content. Prefer bullet points and avoid unncessary explanations.

Here is the content to summarize:
<content>
{content}
</content>
"""

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


def get_website_html(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return ""


def extract_core_website_content(html: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt_extract.format(html=html)
    )

    return response.output_text


def summarize_content(content: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt_summarize.format(content=content)
    )

    return response.output_text


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
    website_url = input("Website URL: ")
    print("Fetching website HTML...")
    try:
        html_content = get_website_html(website_url)
    except Exception as e:
        print(f"An error occurred while fetching the website: {e}")
        return

    if not html_content:
        print("Failed to fetch the website content. Exiting.")
        return

    print("---------")
    print("Extracting core content from the website...")
    core_content = extract_core_website_content(html_content)
    print("Extracted core content:")
    print(core_content)

    print("---------")
    print("Summarizing the core content...")
    summary = summarize_content(core_content)
    print("Generated summary:")
    print(summary)

    print("---------")
    print("Generating X post based on the summary...")
    x_post = generate_post(summary)
    print("Generated X post:")
    print(x_post)


if __name__ == "__main__":
    main()
