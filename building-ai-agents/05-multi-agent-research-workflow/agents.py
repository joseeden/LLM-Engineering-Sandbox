import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from openai import OpenAI

from file_utils import load_text_file
from schemas import SearchConfig
from search_client import search_searx
from tools import Tool, build_research_planner_tools


BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"


class Agent:
    """
    Base class for agents that interact with the OpenAI API.
    """

    def __init__(self, prompt_file: Path, model: str | None = None):
        self.client = OpenAI()
        self.model = model or os.getenv("MODEL_NAME", "gpt-4.1-mini")
        self.messages: list[dict[str, Any]] = [
            {
                "role": "developer",
                "content": load_text_file(prompt_file).format(
                    today=datetime.now().strftime("%Y-%m-%d")
                ),
            }
        ]
        self.tools: dict[str, Tool] = {}

    def register_tool(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def register_tools(self, tools: list[Tool]) -> None:
        for tool in tools:
            self.register_tool(tool)

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        return [tool.get_schema() for tool in self.tools.values()]

    def execute_tool_call(self, tool_call: Any) -> str:
        fn_name = tool_call.name

        if fn_name not in self.tools:
            return f"Unknown tool: {fn_name}"

        try:
            print(f"Calling {fn_name} with arguments: {tool_call.arguments}")
            return str(self.tools[fn_name].execute(tool_call.arguments))
        except Exception as error:
            return f"Error calling {fn_name}: {error}"


class ResearchPlannerAgent(Agent):
    """
    Agent that helps the user create and store a research plan.
    """

    def __init__(self):
        super().__init__(PROMPTS_DIR / "research-planner-agent.txt")
        self.register_tools(build_research_planner_tools())

    def run(self) -> str:
        print("Hi! Please describe today's research task:")

        while True:
            user_input = input(
                "Your Input ('exit' to quit, 'accept' to accept the research plan and continue): "
            )

            if user_input == "exit":
                print("Exiting.")
                sys.exit(0)

            if user_input == "accept":
                return self.create_final_research_plan()

            self.messages.append({"role": "user", "content": user_input})
            self.process_next_turn()

    def create_final_research_plan(self) -> str:
        prompt = (
            "Please create a final version of the discussed research plan and return "
            "just that plan, with no other comments."
        )
        self.messages.append({"role": "user", "content": prompt})
        response = self.client.responses.create(
            model=self.model,
            input=self.messages,
        )

        print("Here's the final research plan:")
        print(response.output_text)
        return response.output_text

    def process_next_turn(self) -> None:
        while True:
            response = self.client.responses.create(
                model=self.model,
                input=self.messages,
                tools=self.get_tool_schemas(),
            )

            reply = response.output[0]
            self.messages.append(reply)

            if reply.type != "function_call":
                print(response.output_text)
                break

            tool_output = self.execute_tool_call(reply)
            self.messages.append(
                {
                    "type": "function_call_output",
                    "call_id": reply.call_id,
                    "output": tool_output,
                }
            )


class WebSearchAgent(Agent):
    """
    Agent that converts a research plan into web search queries and executes them.
    """

    def __init__(self):
        super().__init__(PROMPTS_DIR / "web-search-agent.txt")

    def run(self, research_plan: str) -> list[dict[str, Any]]:
        print("Deriving search terms...")
        self.messages.append(
            {
                "role": "user",
                "content": (
                    "Here's the research plan based on which you should derive "
                    f"search terms: {research_plan}"
                ),
            }
        )
        response = self.client.responses.parse(
            model=self.model,
            input=self.messages,
            text_format=SearchConfig,
        )

        search_config = response.output_parsed
        results = []

        for search_term in search_config.search_terms:
            results.extend(search_searx(search_term, search_config.time_range))

        return results


class SummaryReportAgent(Agent):
    """
    Agent that summarizes search results into a Markdown report.
    """

    def __init__(self):
        super().__init__(PROMPTS_DIR / "summary-report-agent.txt")

    def run(self, search_results: list[dict[str, Any]]) -> str:
        print("Summarizing search results...")
        self.messages.append(
            {
                "role": "user",
                "content": (
                    "Please create a summary and keep the links based on these "
                    f"search results: {json.dumps(search_results, indent=2)}"
                ),
            }
        )
        response = self.client.responses.create(
            model=self.model,
            input=self.messages,
        )

        report = response.output_text.strip()

        if report.startswith("```markdown"):
            report = report.removeprefix("```markdown").strip()

        if report.endswith("```"):
            report = report.removesuffix("```").strip()

        return report
