# test-slack.py

import os
import requests

from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_message(message: str):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message},
        timeout=30,
    )

    response.raise_for_status()


send_message("Hello from test-slack.py")

print("Slack notification sent successfully.")
