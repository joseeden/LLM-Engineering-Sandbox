# config.py
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")

    return anthropic.Anthropic(api_key=api_key)
