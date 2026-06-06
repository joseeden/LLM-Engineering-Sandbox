# LLM Engineering Sandbox

An engineering sandbox and architectural reference for building decoupled LLM integrations, establishing clean application boundaries, and exploring production patterns. 

This repository serves as a personal testing ground for implementing clean LLM architectures, managing conversational state, and exploring practical LLMOps without relying on fragile scripts.

## Getting Started

1. Clone the repository and navigate into the directory.

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv ~/venv
   source ~/venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment and API Setup

1. Create a `.env` file in the root of the project.

    ```bash
    cp .env.example .env
    ```

2. Populate your .env file with your respective API provider keys.

    ```env
    ANTHROPIC_API_KEY=your_anthropic_key_here
    OPENAI_API_KEY=your_openai_key_here
    ```

3. (Optional) If you are utilizing the Claude Code CLI tool within this sandbox environment, make sure it is authenticated globally.

    ```bash
    npm install -g @anthropic-ai/claude-code
    claude
    ```