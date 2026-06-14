# Few-Shot Prompting with OpenAI API

## Overview 

This example demonstrates how to implement few-shot prompting using the OpenAI API. 

Few-shot prompting is a technique where you provide the model with a few examples of the desired output format, which helps guide the model's response.

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
    cd project-llm-engineering-sandbox/building-ai-workflows/04-dynamic-content
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


## Adding Examples 

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

Example:

```text
What do you want to post about? 

Best Practices In Digital Evidence Collection
```


