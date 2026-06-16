import json
import os
from pathlib import Path

# Run "uv sync" to install the below packages
from dotenv import load_dotenv
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
    print("Fetching temperature for:", city)
    return 20.0


available_functions = {
    "get_temperature": get_temperature,
}

tools = [
    {
        "type": "function",
        "name": "get_temperature",
        "description": "Get current temperature for a given location.",
        "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City for which to get the temperature."
                    }
                },
            "additionalProperties": False,
            "required": ["city"],
        },
        "strict": True,

    }
]


def load_prompt(prompt_file: Path) -> str:
    return prompt_file.read_text(encoding="utf-8")


def get_function_call(response):
    for output in response.output:
        if output.type == "function_call":
            return output

    return None


def print_response_text(response):
    if response.output_text:
        print(response.output_text)
    else:
        print("I did not receive a final text answer. Please try again.")


def execute_tool_call(tool_call) -> str | float:
    """
    Executes a tool call and returns the output.
    """
    fn_name = tool_call.name
    fn_args = json.loads(tool_call.arguments)

    if fn_name in available_functions:
        function_to_call = available_functions[fn_name]
        try:
            return function_to_call(**fn_args)
        except Exception as e:
            return f"Error calling {fn_name}: {e}"

    return f"Unknown tool: {fn_name}"


def main():
    messages = [
        {"role": "developer", "content": load_prompt(USER_PROMPT_FILE)}
    ]

    while True:
        user_input = input(
            "\nYour question (type 'q' to exit): ")
        if user_input.strip().lower() == "q":
            break

        messages.append({"role": "user", "content": user_input})
        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=tools,
        )

        # add to chat history to keep track of the conversation
        messages.extend(response.output)

        function_call = get_function_call(response)

        if function_call is None:
            print_response_text(response)
            continue

        tool_output = execute_tool_call(function_call)
        messages.append({
            "type": "function_call_output",
            "call_id": function_call.call_id,
            "output": str(tool_output),
        })
        assistant_prompt = {
            "role": "developer",
            "content": load_prompt(ASST_PROMPT_FILE).format(
                user_input=user_input,
                tool_name=function_call.name,
                tool_output=tool_output,
            ),
        }

        response = client.responses.create(
            model=MODEL_NAME,
            input=messages + [assistant_prompt],
        )
        messages.extend(response.output)
        print_response_text(response)


if __name__ == "__main__":
    main()
