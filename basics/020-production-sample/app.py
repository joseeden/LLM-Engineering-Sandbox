# app.py

from config import get_client
from prompt_builder import build_messages
from model_runner import run_claude


def main():
    client = get_client()

    user_input = "My subscription was renewed without permission"

    messages = build_messages(user_input)

    result = run_claude(client, messages)

    print("\n=== MODEL OUTPUT ===\n")
    print(result)


if __name__ == "__main__":
    main()
