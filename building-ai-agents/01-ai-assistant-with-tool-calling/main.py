import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent

PROMPTS_DIR = BASE_DIR / "prompts"
USER_PROMPT_FILE = PROMPTS_DIR / "prompt_user.txt"
ASST_PROMPT_FILE = PROMPTS_DIR / "prompt_assistant.txt"

load_dotenv(BASE_DIR / ".env")

client = OpenAI()

MODEL_NAME = os.getenv("MODEL_NAME")


def get_temperature(city: str) -> float:
    """
    Get the current temperature for a given city.
    """
    print("\nFetching temperature for:", city)
    return 20.0


def load_prompt(prompt_file: Path) -> str:
    return prompt_file.read_text(encoding="utf-8")


def main():
    user_input = input("\nYour question: ")
    prompt = load_prompt(USER_PROMPT_FILE).format(user_input=user_input)
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )
    reply = response.output_text

    if reply.startswith("get_temperature:"):
        arg = reply.split(":", 1)[1].strip()
        temperature = get_temperature(arg)
        prompt = load_prompt(ASST_PROMPT_FILE).format(
            user_input=user_input,
            arg=arg,
            temperature=temperature,
        )
        response = client.responses.create(
            model=MODEL_NAME,
            input=prompt,
        )
        reply = response.output_text
        print(reply)
    else:
        print(reply)


if __name__ == "__main__":
    main()
