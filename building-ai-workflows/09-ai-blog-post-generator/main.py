import os
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent

POST_EXAMPLES_DIR = BASE_DIR / "posts-examples"
PROMPTS_DIR = BASE_DIR / "prompts"
POSTS_TO_PUBLISH_DIR = BASE_DIR / "posts-to-publish"

DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "developer_prompt.txt"
USER_PROMPT_FILE = PROMPTS_DIR / "user_prompt.txt"


def load_text_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    return file_path.read_text(encoding="utf-8")


def save_text_file(file_path: Path, content: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def load_post_examples() -> str:
    if not POST_EXAMPLES_DIR.exists():
        raise FileNotFoundError(
            f"The directory '{POST_EXAMPLES_DIR}' does not exist."
        )

    post_examples = []

    for file_path in sorted(POST_EXAMPLES_DIR.iterdir()):
        if file_path.suffix.lower() in [".md", ".mdx"]:
            content = load_text_file(file_path)

            post_examples.append(
                f"<post-example file='{file_path.name}'>\n"
                f"{content}\n"
                f"</post-example>"
            )

    if not post_examples:
        raise ValueError(
            "No .md or .mdx files found in the posts-examples directory."
        )

    return "\n\n".join(post_examples)


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

    return "untitled-blog-post"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def get_next_output_file(title: str) -> Path:
    date_prefix = datetime.now().strftime("%d%m%Y")
    slug = slugify(title)

    POSTS_TO_PUBLISH_DIR.mkdir(parents=True, exist_ok=True)

    counter = 1

    while True:
        file_name = f"{date_prefix}-{slug}-{counter:02d}.md"
        output_file = POSTS_TO_PUBLISH_DIR / file_name

        if not output_file.exists():
            return output_file

        counter += 1


def generate_blog_post(outline: str) -> str:
    print("Generating blog post...")

    developer_prompt = load_text_file(DEVELOPER_PROMPT_FILE)
    user_prompt_template = load_text_file(USER_PROMPT_FILE)
    post_examples = load_post_examples()

    user_prompt = user_prompt_template.format(
        outline=outline,
        post_examples=post_examples,
    )

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {
                "role": "developer",
                "content": developer_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return remove_markdown_code_fence(response.output_text)


def main():
    if len(sys.argv) != 2:
        print("Usage: uv run python main.py outlines/sample-outline.txt")
        sys.exit(1)

    outline_file = Path(sys.argv[1])

    print(f"Loading outline: {outline_file}")
    outline = load_text_file(outline_file)

    title = extract_title_from_outline(outline)
    blog_post = generate_blog_post(outline)

    output_file = get_next_output_file(title)

    print(f"Saving blog post: {output_file}")
    save_text_file(output_file, blog_post)

    print(f"Blog post saved to '{output_file}'.")


if __name__ == "__main__":
    main()
