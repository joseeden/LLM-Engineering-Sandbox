# model_runner.py

def run_claude(client, messages):
    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=300,
            temperature=0.2,
            system=(
                "You are a helpful assistant that follows patterns from examples. "
                "Always match tone, structure, and formatting exactly."
            ),
            messages=messages
        )

        return response.content[0].text

    except Exception as e:
        return f"Error: {str(e)}"
