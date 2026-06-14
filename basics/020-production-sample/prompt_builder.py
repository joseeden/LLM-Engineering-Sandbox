# prompt-builder.py
def build_messages(user_input: str):
    return [
        {
            "role": "user",
            "content": "Customer: My order is late."
        },
        {
            "role": "assistant",
            "content": "We’re sorry for the delay. We are checking your order and will update you shortly."
        },

        {
            "role": "user",
            "content": "Customer: I received the wrong item."
        },
        {
            "role": "assistant",
            "content": "We apologize for the mistake. We will arrange a replacement immediately."
        },

        {
            "role": "user",
            "content": f"Customer: {user_input}"
        }
    ]
