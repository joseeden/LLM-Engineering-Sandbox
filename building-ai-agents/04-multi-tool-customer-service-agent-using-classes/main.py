import os
from pathlib import Path

from dotenv import load_dotenv

from agents import CustomerServiceAgent
from database import create_db_and_tables


BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"

DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "developer-prompt.txt"


def main():
    load_dotenv()
    create_db_and_tables()

    agent = CustomerServiceAgent(
        model=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
        developer_prompt_file=DEVELOPER_PROMPT_FILE,
    )
    agent.run()


if __name__ == "__main__":
    main()
