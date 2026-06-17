from pathlib import Path
from typing import Any

from openai import OpenAI

from customer_service_tools import Tool, build_customer_service_tools
from file_utils import load_text_file


class Agent:
    """
    Base class for an agent that can interact with the OpenAI API.
    """

    def __init__(
        self,
        model: str,
        developer_prompt_file: Path,
    ):
        self.client = OpenAI()
        self.model = model
        self.messages: list[dict[str, Any]] = [
            {
                "role": "developer",
                "content": load_text_file(developer_prompt_file),
            }
        ]
        self.tools: dict[str, Tool] = {}

    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        return [tool.get_schema() for tool in self.tools.values()]

    def execute_tool_call(self, tool_call: Any) -> str:
        fn_name = tool_call.name

        if fn_name not in self.tools:
            return f"Unknown tool: {fn_name}"

        try:
            print(f"Calling {fn_name} with arguments: {tool_call.arguments}")
            return self.tools[fn_name].execute(tool_call.arguments)
        except Exception as error:
            return f"Error calling {fn_name}: {error}"

    def print_message_text(self, message: Any) -> None:
        for content_item in getattr(message, "content", []):
            text = getattr(content_item, "text", None)

            if text:
                print(text)

    def run(self) -> None:
        raise NotImplementedError("The run method must be implemented by a subclass.")


class CustomerServiceAgent(Agent):
    """
    Customer service agent with tools for verification, orders, refunds, and feedback.
    """

    def __init__(
        self,
        model: str,
        developer_prompt_file: Path,
    ):
        super().__init__(model, developer_prompt_file)
        self.register_tools(build_customer_service_tools())

    def register_tools(self, tools: list[Tool]) -> None:
        for tool in tools:
            self.register_tool(tool)

    def run(self) -> None:
        print(
            "\nWelcome to the customer service chatbot."
            "\nHow can we help you today?"
            "\nType 'exit' to end the conversation."
        )

        while True:
            user_input = input("\nYour input: ")

            if user_input == "exit":
                break

            self.messages.append({"role": "user", "content": user_input})

            for _ in range(5):
                response = self.client.responses.create(
                    model=self.model,
                    input=self.messages,
                    tools=self.get_tool_schemas(),
                )

                for reply in response.output:
                    self.messages.append(reply)

                    if reply.type == "function_call":
                        tool_output = self.execute_tool_call(reply)
                        self.messages.append(
                            {
                                "type": "function_call_output",
                                "call_id": reply.call_id,
                                "output": str(tool_output),
                            }
                        )
                        continue

                    if reply.type == "message":
                        self.print_message_text(reply)

                if not isinstance(self.messages[-1], dict) and self.messages[-1].type == "message":
                    break
