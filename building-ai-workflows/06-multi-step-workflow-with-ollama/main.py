import os
import json
import requests

from pathlib import Path
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME_4B = os.getenv("MODEL_NAME_4B")
MODEL_NAME_1B = os.getenv("MODEL_NAME_1B")
MODEL_NAME_12B = os.getenv("MODEL_NAME_12B")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_FILE = BASE_DIR / "post-examples.json"


prompt_extract = """
You are an expert web content extractor.

Your task is to extract only the main article content from the provided HTML.

Remove:
- Navigation
- Menus
- Footer content
- Ads
- Scripts
- Style-related content
- Cookie banners
- Related posts
- Author bio sections unless they are part of the article

Return only the article title and the main article body as plain text.

Do not explain the HTML.
Do not describe the page structure.
Do not mention tags, classes, scripts, or CSS.

Here is the HTML:

<html>
{html}
</html>
"""

prompt_summarize = """
You are an expert summarizer.

Summarize the provided article content into a concise and clear summary.

Use short bullet points.
Avoid unnecessary explanations.

Here is the article content:

<content>
{content}
</content>
"""

prompt_input = """
You are an expert social media manager.

Your task is to create a concise and engaging social media post based on the user's input.

Important guidelines:

- Avoid hashtags or emojis.
- Do not use asyndetons.
- Use complete sentences or conjunctions.
- Do not use em dash.
- Use bullet points only when appropriate.

Here are some example posts:

{examples_str}

Use the tone, language style, and formatting from the examples as reference.
Do not copy content from the examples.

Here is the user's input:

{topic}
"""


def get_ai_response(prompt: str, model: str, ctx: int = 4000) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": ctx
                }
            },
            # timeout=300
        )

        response.raise_for_status()
        data = response.json()

        if "response" not in data:
            print("Unexpected response format:", data)
            return ""

        return data["response"].strip()

    except requests.RequestException as e:
        print(f"Ollama request failed: {e}")
        return ""


def get_website_html(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        return response.text

    except requests.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return ""


def reduce_html_noise(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup([
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "form",
        "button",
        "nav",
        "footer",
        "header"
    ]):
        tag.decompose()

    text = str(soup)

    max_chars = 50000

    if len(text) > max_chars:
        text = text[:max_chars]

    return text


def extract_core_website_content(html: str) -> str:
    cleaned_html = reduce_html_noise(html)

    response = get_ai_response(
        model=MODEL_NAME_4B,
        prompt=prompt_extract.format(html=cleaned_html),
        ctx=20000
    )

    return response


def summarize_content(content: str) -> str:
    response = get_ai_response(
        model=MODEL_NAME_4B,
        prompt=prompt_summarize.format(content=content),
        ctx=8000
    )

    return response


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

    response = get_ai_response(
        model=MODEL_NAME_12B,
        prompt=prompt,
        ctx=8000
    )

    return response


def main():
    website_url = input("Website URL: ")

    print("Fetching website HTML...")
    html_content = get_website_html(website_url)

    if not html_content:
        print("Failed to fetch the website content. Exiting.")
        return

    print("---------")
    print("Extracting core content from the website using LLM...")
    core_content = extract_core_website_content(html_content)

    if not core_content:
        print("Failed to extract core content. Exiting.")
        return

    print("Extracted core content:")
    print(core_content)

    print("---------")
    print("Summarizing the core content...")
    summary = summarize_content(core_content)

    if not summary:
        print("Failed to summarize content. Exiting.")
        return

    print("Generated summary:")
    print(summary)

    print("---------")
    print("Generating X post based on the summary...")
    x_post = generate_post(summary)

    if not x_post:
        print("Failed to generate X post. Exiting.")
        return

    print("Generated X post:")
    print(x_post)


if __name__ == "__main__":
    main()
