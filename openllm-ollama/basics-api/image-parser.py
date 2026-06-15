# image-parser.py
from openai import OpenAI
import base64
import os

from dotenv import load_dotenv
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="not-needed"
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_folder = "./images"

image_files = [
    f for f in os.listdir(image_folder)
    if os.path.isfile(os.path.join(image_folder, f))
    and f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not image_files:
    raise FileNotFoundError(
        f"No image files found in '{image_folder}'"
    )

image_path = os.path.join(image_folder, image_files[0])

print(f"Using image: {image_path}")

base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
