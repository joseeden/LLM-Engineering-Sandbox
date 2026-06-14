# Multi-Step AI Workflow with Ollama

This example demonstrates how to build a simple multi-step AI workflow using Ollama to process website content and generate social media posts.

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
    

## Workflow Overview 

The output of each step is passed to the next stage of the workflow:

```text
Website URL
    │
    ▼
Fetch HTML
    │
    ▼
Extract Core Content
    │
    ▼
Summarize Content
    │
    ▼
Generate Social Media Post
    │
    ▼
Final Output
``` 

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
- [Ollama](https://ollama.com/) 


## Setup

1. Clone the repository

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox
    cd project-llm-engineering-sandbox/building-ai-workflows/06-multi-step-workflow-with-ollama
    ```

2. Install UV 

    Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

4. Verify installation:

    ```bash
    uv --version
    ```

5. Install Dependencies

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

## Load the Models with Ollama

The workflow uses a local model served by Ollama instead of calling OpenAI's hosted API.

> See [Ollama models](https://ollama.com/library)

For this example, I am using three models, each for a specific step in the workflow:

| Model               | Purpose                                                     | Reason for selection                                                                                    |
| ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `gemma3:4b-it-qat`  | Used for extracting the main content from the website HTML. | Provides a good balance between speed and accuracy, and it can handle large amounts of website content. |
| `gemma3:4b-it-qat`  | Used for summarizing the extracted content.                 | Produces clear and accurate summaries, and it remains efficient for intermediate processing tasks.      |
| `gemma3:12b-it-qat` | Used for generating the final social media post.            | Delivers stronger writing quality and reasoning, which helps create more engaging social media content. |

Pull down the models and verify:

```bash
ollama pull gemma3:4b-it-qat
ollama pull gemma3:12b-it-qat

ollama list
```

Export the model names and endpoint URL as environment variables:

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export MODEL_NAME_4B="gemma3:4b-it-qat"
export MODEL_NAME_12B="gemma3:12b-it-qat"
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
Website URL: https://jupyter4edu.github.io/jupyter-edu-book/
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

![](../images/.gif)

</div>


## Things to Keep in Mind

- The extraction quality depends on the structure of the target website.
- Large web pages may increase token usage and response time.
- The final post generation step uses few-shot prompting through examples stored in `post-examples.json`.