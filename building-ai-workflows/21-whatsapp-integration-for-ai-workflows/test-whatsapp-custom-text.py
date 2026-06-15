import argparse
import os

import requests
from dotenv import load_dotenv


load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v23.0")

DEFAULT_MESSAGE = (
    "Hello there from the other side! "
    "I was triggered from the test script"
)


def validate_env() -> None:
    required_values = {
        "WHATSAPP_ACCESS_TOKEN": WHATSAPP_ACCESS_TOKEN,
        "WHATSAPP_PHONE_NUMBER_ID": WHATSAPP_PHONE_NUMBER_ID,
        "WHATSAPP_TO_NUMBER": WHATSAPP_TO_NUMBER,
    }

    missing_values = [
        name for name, value in required_values.items() if not value
    ]

    if missing_values:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing_values)
        )


def send_whatsapp_text_message(message: str) -> None:
    validate_env()

    url = (
        f"https://graph.facebook.com/{WHATSAPP_API_VERSION}/"
        f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": WHATSAPP_TO_NUMBER,
        "type": "text",
        "text": {
            "body": message,
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    print("Status code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()


def main():
    parser = argparse.ArgumentParser(
        description="Send a custom WhatsApp text message using the WhatsApp Cloud API."
    )

    parser.add_argument(
        "--message",
        default=DEFAULT_MESSAGE,
        help="Message to send to WhatsApp.",
    )

    args = parser.parse_args()

    print(f"Sending message: {args.message}")

    send_whatsapp_text_message(args.message)

    print("WhatsApp message sent successfully.")


if __name__ == "__main__":
    main()
