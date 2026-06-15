import os

import requests
from dotenv import load_dotenv


load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER")
WHATSAPP_API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v23.0")


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


## --------------------------------------------------------------##

# This uses the default template "hello_world" that comes with the WhatsApp Business API. You can create your own templates in the Facebook Business Manager and update the template name and language code below.

def send_whatsapp_template_message() -> None:
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
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US",
            },
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


if __name__ == "__main__":
    send_whatsapp_template_message()
    print("WhatsApp template message sent successfully.")
