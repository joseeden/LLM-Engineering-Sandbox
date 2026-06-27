# AI Content Processing: Multi-Step AI Workflow with OpenAI API

## Overview 

This example demonstrates how to build a simple multi-step AI workflow using the OpenAI API to process website content and generate social media posts.

Instead of sending a single prompt to a model, the application breaks the task into multiple steps:

1. **Website Fetching**

    The workflow starts by downloading the HTML content from the provided URL using the `requests` library.

2. **Content Extraction**

    A dedicated AI prompt extracts the main content from the HTML and removes unnecessary elements such as navigation menus, scripts, headers, and footers.

3. **Summarization**

    The extracted content is summarized into a concise set of key points.

4. **Social Media Post Generation**

    The summary is passed into a final prompt that generates a social media post.
    This step uses examples stored in `post-examples.json` to guide the writing style and output format.
    
The output of each step is passed to the next stage of the workflow:

<div class='img-center'>

![](../images/project-ai-content-processing-workflow.png)

</div>

This approach allows each step to focus on a specific task, which often produces more reliable results than handling everything in a single prompt.


## Project Structure

```text
├── .env
├── .env.example
├── main.py
├── post-examples.json
├── pyproject.toml
├── requirements.txt
├── uv.lock
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
    cd project-llm-engineering-sandbox/building-ai-workflows/05-multi-step-workflow
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
    OPENAI_API_KEY=your_api_key_here

    MODEL_NAME=your_model_name_here
    ```


## Install uv

1. Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. Verify installation:

    ```bash
    uv --version
    ```


## Install Dependencies

From the project directory, run:

```bash
uv sync
```

This will:

1. Create a virtual environment if needed
2. Install all project dependencies
3. Use the versions locked in `uv.lock`

## Few-Shot Prompting 

The example few-shot prompts are stored in `post-examples.json`. 

You can modify this file to add more examples or change existing ones. 

Each example should follow the structure:

```json
[
  {
    "post": [
      "Best Practices In Digital Evidence Collection"
    ]
  },
  {
    "post": [
      "How To Use LLMs For Data Analysis"
    ]
  }
]
```

For multiline examples, you can use multiple strings in the `post` array, and they will be joined together when sent to the model.


```json
[
  {
    "post": [
      "Cloud computing has changed the way organizations build and operate technology platforms.",
      "",
      "Some of the key benefits include:",
      "",
      "Faster deployment of services",
      ...
    ]
  }
]      
```

## Run the Application

```bash
uv run python main.py
```

Provide a website URL when prompted:

```text
Website URL: https://example.com/blog/article
```

Example:

```bash
Website URL: https://www.iotforall.com/intelligent-mobility-smarter-cities
```

The script will extract the core content from the provided URL, summarize it, and generate a social media post based on the summary and examples.

```text
Fetching website HTML...

---------
Extracting core content from the website...

---------
Summarizing the core content...

---------
Generating social media post based on the summary...

Generated social media post:
...
```

<div class='img-center'>

![](../images/1406206-multi-step-workflow-ai-content-processing.gif)

</div>


## Things to Keep in Mind

- The extraction quality depends on the structure of the target website.
- Large web pages may increase token usage and response time.
- The final post generation step uses few-shot prompting through examples stored in `post-examples.json`.
