
# AI Assistant with Tool Calling

## Overview

This Python script creates a basic AI assistant that can answer a user's questions.

The assistant can answer general questions on its own. However, when the user asks for the temperature in a city, the LLM is expected to call the backend tool `get_temperature` instead of generating the answer itself.

The goal is not to retrieve real weather data. The tool always returns a fixed value of `20.0°C` so it is easy to verify that the LLM actually used the tool.

The script performs the following steps:

1. The LLM determines that a tool call is needed.
2. It calls the local `get_temperature` function.
3. The function returns a hardcoded temperature of `20.0°C`.
4. The result is sent back to the LLM to generate the final answer.

In a real application, the tool could connect to a weather API, database, CRM, calendar, payment system, or internal company service.

<!-- 
## Workflow

1. The AI agent receives a user request.
2. Decides whether it needs a tool.
3. Calls backend code controlled by the application.
4. Sends the tool result back to the model.
5. Returns a final natural-language answer. -->

## Project Structure

```text
01-ai-assistant-with-tool-calling/
│
├── prompts
│   ├── prompt_assistant.txt
│   └── prompt_user.txt
│
├── pyproject.toml
├── README.md
└── main.py
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
    cd project-llm-engineering-sandbox/building-ai-agents/01-ai-assistant-with-tool-calling
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

    <!-- **Note:** The OpenAI SDK automatically appends the correct endpoint paths based on the method being called, so the base URL should just be this. -->

4. Install UV 

    Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Verify installation:

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


## Prompts

The workflow stores prompts in the `prompts/` directory.

```text
prompts/
├── prompt_assistant.txt
└── prompt_user.txt
```

The prompts could be written directly in `main.py`, but they are stored separately to keep the application code cleaner and make prompt updates easier to manage.

- `prompt_user.txt` tells the LLM when and how to request the tool.
- `prompt_assistant.txt` helps the LLM write the final answer using the tool result.

If the user asks for the temperature in a city, the LLM should recognize that it needs to call the `get_temperature` tool instead of generating an answer directly. The tool will return a fixed value of `20.0°C`, which is then sent back to the LLM to generate the final response.


## Run the Application

Generate a blog post from an outline:

```bash
uv run python main.py
```

Expected output:

```text
Your question: 
```

Provide a question about the weather, for example:

```text
Your question: What is the temperature in Paris?
```

It should answer like this:

```text
Fetching temperature for: Paris
The temperature in Paris is 20.0°C.
Would you like a forecast or more details (humidity, wind, etc.)?
```

You can re-run the scripts and ask about different cities, and the temperature return should always be `20.0°C` since the tool is hardcoded to return that value.