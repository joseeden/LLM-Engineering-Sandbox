# Using the OpenAI SDK

This example demonstrates how to interact with an OpenAI-compatible API using the official OpenAI Python SDK.

## Project Structure

```text
.
├── .env
├── .env.example
├── main.py
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
    cd project-llm-engineering-sandbox/building-ai-workflows/02-using-openai-sdk
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

    MODEL_NAME=gpt-5
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


## Run the Application

```bash
uv run python main.py
```

Example:

```text
What do you want to post about? 

LLM and ML are useful skills that Cloud and DevOps Engineers must learn.
```

Example output:

> For cloud and DevOps engineers, mastering machine learning and large language models is increasingly essential.
> 
> ML and LLM skills unlock smarter automation, proactive issue detection, and faster recovery across cloud environments.
> 
> They enable you to build intelligent tooling, optimize costs, and strengthen security within your pipelines.
> 
> Integrating ML into CI/CD and infrastructure automation turns operational excellence into a repeatable advantage.
> 
> Invest in learning these skills now to future proof your career and elevate your team's impact.


