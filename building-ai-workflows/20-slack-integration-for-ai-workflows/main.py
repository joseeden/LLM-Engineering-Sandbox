import argparse
import base64
import os
import re
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
IMAGE_MODEL_NAME = os.getenv("IMAGE_MODEL_NAME", "gpt-image-1")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent

OUTLINES_DIR = BASE_DIR / "outlines"
POST_EXAMPLES_DIR = BASE_DIR / "posts-examples"
LINKEDIN_EXAMPLES_DIR = BASE_DIR / "linkedin-post-examples"
PROMPTS_DIR = BASE_DIR / "prompts"

POSTS_TO_PUBLISH_DIR = BASE_DIR / "posts-to-publish"
THUMBNAILS_DIR = BASE_DIR / "thumbnails"
LINKEDIN_POSTS_DIR = BASE_DIR / "linkedin-posts"

ARTICLE_DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "article_developer_prompt.txt"
ARTICLE_USER_PROMPT_FILE = PROMPTS_DIR / "article_user_prompt.txt"
ARTICLE_IMPROVEMENT_PROMPT_FILE = PROMPTS_DIR / "article_improvement_prompt.txt"
EVALUATION_DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "evaluation_developer_prompt.txt"
EVALUATION_USER_PROMPT_FILE = PROMPTS_DIR / "evaluation_user_prompt.txt"
THUMBNAIL_PROMPT_FILE = PROMPTS_DIR / "thumbnail_prompt.txt"
LINKEDIN_DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "linkedin_developer_prompt.txt"
LINKEDIN_USER_PROMPT_FILE = PROMPTS_DIR / "linkedin_user_prompt.txt"


class Evaluation(BaseModel):
    needs_improvement: bool = Field(
        description="Whether the blog post needs improvement."
    )
    feedback: str = Field(
        description="Short feedback explaining how the blog post can be improved."
    )


def load_text_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    return file_path.read_text(encoding="utf-8")


def save_text_file(file_path: Path, content: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def save_binary_file(file_path: Path, content: bytes) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(content)


def load_markdown_examples(directory: Path, tag_name: str) -> str:
    if not directory.exists():
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    examples = []

    for file_path in sorted(directory.iterdir()):
        if file_path.suffix.lower() in [".md", ".mdx", ".txt"]:
            content = load_text_file(file_path)
            examples.append(
                f"<{tag_name} file='{file_path.name}'>\n"
                f"{content}\n"
                f"</{tag_name}>"
            )

    if not examples:
        raise ValueError(f"No example files found in '{directory}'.")

    return "\n\n".join(examples)


def remove_markdown_code_fence(text: str) -> str:
    cleaned_text = text.strip()

    if cleaned_text.startswith("```markdown"):
        lines = cleaned_text.splitlines()

        if len(lines) > 2 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()

    if cleaned_text.startswith("```"):
        lines = cleaned_text.splitlines()

        if len(lines) > 2 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()

    return cleaned_text


def extract_title_from_outline(outline: str) -> str:
    for line in outline.splitlines():
        if line.lower().startswith("title:"):
            return line.split(":", 1)[1].strip()

    return "untitled-post"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def get_next_file_path(directory: Path, title: str, extension: str) -> Path:
    date_prefix = datetime.now().strftime("%d%m%Y")
    slug = slugify(title)

    directory.mkdir(parents=True, exist_ok=True)

    counter = 1

    while True:
        file_name = f"{date_prefix}-{slug}-{counter:02d}{extension}"
        file_path = directory / file_name

        if not file_path.exists():
            return file_path

        counter += 1


def send_slack_notification(message: str) -> None:
    if not SLACK_WEBHOOK_URL:
        print("Skipping Slack notification. SLACK_WEBHOOK_URL is not set.")
        return

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=30,
    )

    response.raise_for_status()


def generate_blog_post(outline: str) -> str:
    print("Generating blog post...")

    developer_prompt = load_text_file(ARTICLE_DEVELOPER_PROMPT_FILE)
    user_prompt_template = load_text_file(ARTICLE_USER_PROMPT_FILE)
    post_examples = load_markdown_examples(POST_EXAMPLES_DIR, "post-example")

    user_prompt = user_prompt_template.format(
        outline=outline,
        post_examples=post_examples,
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return remove_markdown_code_fence(response.output_text)


def evaluate_blog_post(outline: str, article: str) -> Evaluation:
    print("Evaluating blog post...")

    developer_prompt = load_text_file(EVALUATION_DEVELOPER_PROMPT_FILE)
    user_prompt_template = load_text_file(EVALUATION_USER_PROMPT_FILE)

    user_prompt = user_prompt_template.format(
        outline=outline,
        article=article,
    )

    response = client.responses.parse(
        model=MODEL_NAME,
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": user_prompt},
        ],
        text_format=Evaluation,
    )

    return response.output_parsed


def improve_blog_post(outline: str, article: str, feedback: str) -> str:
    print("Improving blog post...")

    developer_prompt = load_text_file(ARTICLE_DEVELOPER_PROMPT_FILE)
    improvement_prompt_template = load_text_file(
        ARTICLE_IMPROVEMENT_PROMPT_FILE)
    post_examples = load_markdown_examples(POST_EXAMPLES_DIR, "post-example")

    improvement_prompt = improvement_prompt_template.format(
        outline=outline,
        article=article,
        feedback=feedback,
        post_examples=post_examples,
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": improvement_prompt},
        ],
    )

    return remove_markdown_code_fence(response.output_text)


def generate_thumbnail(article: str) -> bytes:
    print("Generating thumbnail...")

    thumbnail_prompt_template = load_text_file(THUMBNAIL_PROMPT_FILE)
    thumbnail_prompt = thumbnail_prompt_template.format(article=article)

    response = client.images.generate(
        model=IMAGE_MODEL_NAME,
        prompt=thumbnail_prompt,
        n=1,
        output_format="jpeg",
        size="1536x1024",
    )

    return base64.b64decode(response.data[0].b64_json)


def generate_linkedin_post(article: str) -> str:
    print("Generating LinkedIn post...")

    developer_prompt = load_text_file(LINKEDIN_DEVELOPER_PROMPT_FILE)
    user_prompt_template = load_text_file(LINKEDIN_USER_PROMPT_FILE)

    linkedin_examples = load_markdown_examples(
        LINKEDIN_EXAMPLES_DIR,
        "linkedin-post-example",
    )

    user_prompt = user_prompt_template.format(
        article=article,
        linkedin_examples=linkedin_examples,
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.output_text.strip()


def build_slack_message(
    title: str,
    article_file: Path,
    thumbnail_file: Path | None,
    linkedin_file: Path | None,
    evaluation: Evaluation,
) -> str:
    message = (
        "AI content workflow completed.\n\n"
        f"Title: {title}\n"
        f"Needs improvement: {evaluation.needs_improvement}\n"
        f"Feedback: {evaluation.feedback}\n\n"
        f"Article: {article_file.name}\n"
    )

    if thumbnail_file:
        message += f"Thumbnail: {thumbnail_file.name}\n"

    if linkedin_file:
        message += f"LinkedIn post: {linkedin_file.name}\n"

    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outline_file", help="Path to the outline text file.")
    parser.add_argument(
        "--skip-thumbnail",
        action="store_true",
        help="Skip thumbnail image generation.",
    )
    parser.add_argument(
        "--skip-linkedin",
        action="store_true",
        help="Skip LinkedIn post generation.",
    )
    parser.add_argument(
        "--skip-slack",
        action="store_true",
        help="Skip Slack notification.",
    )

    args = parser.parse_args()

    outline_file = Path(args.outline_file)

    print(f"Loading outline: {outline_file}")
    outline = load_text_file(outline_file)

    title = extract_title_from_outline(outline)

    blog_post = generate_blog_post(outline)

    evaluation = evaluate_blog_post(outline, blog_post)

    print("Evaluation result:")
    print(f"Needs improvement: {evaluation.needs_improvement}")
    print(f"Feedback: {evaluation.feedback}")

    if evaluation.needs_improvement:
        blog_post = improve_blog_post(
            outline=outline,
            article=blog_post,
            feedback=evaluation.feedback,
        )

    article_file = get_next_file_path(POSTS_TO_PUBLISH_DIR, title, ".md")

    print(f"Saving blog post: {article_file}")
    save_text_file(article_file, blog_post)

    thumbnail_file = None

    if not args.skip_thumbnail:
        thumbnail = generate_thumbnail(blog_post)
        thumbnail_file = get_next_file_path(THUMBNAILS_DIR, title, ".jpeg")

        print(f"Saving thumbnail: {thumbnail_file}")
        save_binary_file(thumbnail_file, thumbnail)

    linkedin_file = None

    if not args.skip_linkedin:
        linkedin_post = generate_linkedin_post(blog_post)
        linkedin_file = get_next_file_path(LINKEDIN_POSTS_DIR, title, ".txt")

        print(f"Saving LinkedIn post: {linkedin_file}")
        save_text_file(linkedin_file, linkedin_post)

    if not args.skip_slack:
        slack_message = build_slack_message(
            title=title,
            article_file=article_file,
            thumbnail_file=thumbnail_file,
            linkedin_file=linkedin_file,
            evaluation=evaluation,
        )

        print("Sending Slack notification...")
        send_slack_notification(slack_message)

    print("Workflow completed.")


if __name__ == "__main__":
    main()
