# AI Blog Post Generator

## Overview 

This project generates blog posts from outlines using AI.

Instead of writing a blog post from scratch, the workflow uses an outline and a collection of example posts to generate a new article that follows a similar writing style.

The goal is to automate the creation of first drafts while maintaining a consistent tone and structure.

## Workflow

The workflow processes content in multiple steps.

1. Load a blog post outline
2. Load example blog posts
3. Send the outline and examples to an LLM
4. Generate a new blog post
5. Save the generated post as a Markdown file

Each step has a single responsibility, which makes the workflow easier to understand and maintain.

### 1. Outline Processing

The workflow starts by loading a text file that contains the outline for the new article.

The outline provides the topic, structure, and key points that should be covered in the generated post.

### 2. Style Reference Loading

The workflow loads example blog posts from the `posts-examples/` directory.

These examples are used as style references.

The model learns from:

- Writing tone
- Article structure
- Paragraph style
- Use of headings
- Use of bullet points

The workflow uses the examples for style only and does not reuse their content.

### 3. AI-Powered Content Generation

The outline and example posts are sent to an LLM.

The model generates a complete blog post that:

- Covers the outline topic
- Follows the writing style of the examples
- Returns Markdown content ready for publishing

### 4. File Output

The generated blog post is saved to a Markdown file.

The resulting file can be reviewed, edited, or published directly.


## Project Structure

```text
ai-blog-post-generator/
│
├── outlines
│   └── sample-outline.txt
│
├── posts-examples
│   ├── cybersecurity-basics.mdx
│   ├── iot-edge-monitoring.md
│   └── running-consistency.mdx
│
├── posts-to-publish
│   ├── 15062026-why-running-local-ai-models-is-useful-for-developers-01.md
│   └── 15062026-why-running-local-ai-models-is-useful-for-developers-02.md
│
├── prompts
│   ├── developer_prompt.txt
│   └── user_prompt.txt
│
├── pyproject.toml
├── uv.lock
├── main.py
└── README.md
```

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [An OpenAI account](https://platform.openai.com/login)
- [OpenAI API credentials](https://platform.openai.com/account/api-keys)

## Setup

1. Clone the repository

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox
    cd project-llm-engineering-sandbox/building-ai-workflows/09-ai-blog-post-generator
    ```

2. Copy the environment file

    Create a `.env` file from the provided example:

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables

    Open `.env` and update the values.

    **NOTE:** NEVER commit your real API keys to source control.

    ```env
    OPENAI_API_KEY=your_openai_key_here
    OPENAI_BASE_URL="https://api.openai.com/v1"

    MODEL_NAME=your_model_name_here
    ```

    **Note:** The OpenAI SDK automatically appends the correct endpoint paths based on the method being called, so the base URL should just be this.

4. Install UV 

    Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Verify installation:

    ```bash
    uv --version
    ```

5. Install SQLite CLI (Optional, for database validation)

    Linux / macOS

    ```bash
    sudo apt update -y
    sudo apt install -y sqlite3
    ```

6. Install Dependencies

    From the project directory, run:

    ```bash
    uv sync
    ```

    This will:

    1. Create a virtual environment if needed
    2. Install all project dependencies
    3. Use the versions locked in `uv.lock`


### Prompts

The workflow stores prompts in the `prompts/` directory.

```text
prompts/
├── developer_prompt.txt
└── user_prompt.txt
```

The prompts could be written directly in `main.py`, but they are stored separately to keep the application code cleaner and make prompt updates easier to manage.

1. `developer_prompt.txt`

    Defines the writing behavior of the model. This prompt contains instructions about:

    - Writing style
    - Tone
    - Audience
    - Formatting expectations

2. `user_prompt.txt`

    Defines the content generation task. The application injects:

    - The article outline
    - The example blog posts

    before sending the prompt to the model.

### Example Posts

The workflow uses blog posts stored in:

```text
posts-examples/
├── cybersecurity-basics.mdx
├── iot-edge-monitoring.md
└── running-consistency.mdx
```

The model uses these examples to learn:

- Writing style
- Sentence structure
- Article organization
- Tone

The content itself is not copied into the generated article.

Using multiple examples generally produces more consistent results than relying on instructions alone.

### Outlines

The workflow uses outline files stored in:

```text
outlines/
└── sample-outline.txt
```

The outline acts as the source material for the generated article.

## Run the Application

Generate a blog post from an outline:

```bash
uv run python main.py outlines/sample-outline.txt
```

Output:

```bash
Loading outline: outlines/sample-outline.txt
Generating blog post...
Saving blog post: posts-to-publish/15062026-why-running-local-ai-models-is-useful-for-developers-01.md
Blog post saved to 'posts-to-publish/15062026-why-running-local-ai-models-is-useful-for-developers-01.md'.
```

The generated blog post will be saved to:

```text
posts-to-publish/
```


## Validation

After running the application, verify that the blog post was generated successfully.

1. Check that a new file exists in:

    ```text
    posts-to-publish/
    ```

2. Open the generated file and confirm that:

    - The topic matches the outline
    - The structure follows the outline
    - The writing style is similar to the example posts
    - The output is valid Markdown

3. Compare the generated article against the example posts.

    The generated content should:

    - Follow a similar tone
    - Use similar formatting patterns
    - Maintain a consistent writing style

    without copying the original content.

## Use Case

Creating blog content can be time-consuming, especially when maintaining a consistent writing style across multiple articles.

This workflow combines outlines, few-shot prompting, and AI-generated content to automate the creation of blog posts.

The result is a simple content generation pipeline that can be extended to support documentation, technical blogs, learning notes, knowledge bases, and other Markdown-based publishing workflows.
