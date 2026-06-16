# AI Assistant with Function Calling

## Overview

This lab is similar to the AI Assistant with Tool Calling lab, but it uses OpenAI function calling instead of manual tool requests.

The model receives a structured function definition and can return a structured function call, which Python then executes.

The goal is not to retrieve real weather data. The `get_temperature` function always returns a fixed value of `20.0`, making it easy to verify that the function was called.

The script performs the following steps:

1. The user asks a question.
2. The model decides whether to call a function.
3. Python runs the local `get_temperature` function.
4. The tool result is sent back to the model.
5. The model writes the final answer.

In a real application, the function could connect to a weather API, database, CRM, calendar, payment system, or other internal services.

## Function Calling

Function calling allows a model to use functions defined in your application. When the model needs information or wants to perform an action, it can request a function call. Your code then executes the function and returns the result back to the model.

Note that function calling is a type of tool calling.

| Term             | Meaning                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| Tool calling     | The general concept of an LLM using external tools.                     |
| Function calling | A structured form of tool calling where tools are defined as functions. |

To enable function calling, you provide the model with one or more tool definitions.

In the example below, the `get_temperature` function is defined as a tool:

```python
tools = [
    {
        "type": "function",
        "name": "get_temperature",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City for which to get the temperature."
                }
            },
            "additionalProperties": False,
            "required": ["city"],
        },
        "strict": True,
    }
]
```

The `parameters` field contains a JSON Schema that describes the function arguments. The rest of the object provides information about the function, such as its name, description, type, and validation rules.

The variable name `tools` is arbitrary. Other names would also work, such as:

- `available_tools`
- `function_tools`
- `openai_tools` 

The important part is that the list is passed to the OpenAI request:

```python
response = client.responses.create(
    model=MODEL_NAME,
    input=messages,
    tools=tools,
)
```

If you add more tools later, you normally put them all in the same list:

```bash
tools = [
    {
        "type": "function",
        "name": "get_temperature",
        ...
    },
    {
        "type": "function",
        "name": "get_calendar_events",
        ...
    },
    {
        "type": "function",
        "name": "search_database",
        ...
    },
]
```

## Project Structure

```text
02-ai-assistant-with-function-calling/
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
    cd project-llm-engineering-sandbox/building-ai-agents/02-ai-assistant-with-function-calling
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

4. Install dependencies

    From the project directory, run:

    ```bash
    uv sync
    ```

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

Run the script:

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