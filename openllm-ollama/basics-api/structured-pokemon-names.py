# structured-pokemon-names.py
import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
url = "http://localhost:11434/api/generate"


prompt = """
Generate a JSON list of three fictional Pokemon names.
Each one should have a type, ability, and an owner. 
The output should be in JSON format.
"""

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "pokemon_name": {
                "type": "string",
                "description": "The Pokemon's name"
            },
            "type": {
                "type": "string",
                "description": "The Pokemon's type"
            },
            "ability": {
                "type": "string",
                "description": "The Pokemon's ability"
            },
            "owner": {
                "type": "string",
                "description": "The Pokemon's owner"
            }
        },
        "required": ["pokemon_name", "type", "ability", "owner"]
    }
}

payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "format": schema,
    "stream": False
}

response = requests.post(url, json=payload)
response.raise_for_status()

data = response.json()
users = json.loads(data["response"])

print(json.dumps(users, indent=2))
