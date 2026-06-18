import json
from typing import Any

import database


class Tool:
    """
    Base class for tools that can be used by an agent.
    """

    name: str
    description: str
    parameters: dict[str, Any]

    def get_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.parameters,
                "additionalProperties": False,
                "required": list(self.parameters.keys()),
            },
        }

    def parse_arguments(self, arguments: str) -> dict[str, Any]:
        if not arguments:
            return {}

        return json.loads(arguments)

    def execute(self, arguments: str) -> Any:
        raise NotImplementedError("Each tool must implement its own execute method.")


class StoreResearchPlanTool(Tool):
    name = "store_research_plan"
    description = "Stores a user's research plan in the database."
    parameters = {
        "short_summary": {
            "type": "string",
            "description": "A very short summary title of the research plan.",
        },
        "details": {
            "type": "string",
            "description": "The details of the research plan.",
        },
    }

    def execute(self, arguments: str) -> dict[str, Any]:
        try:
            args = self.parse_arguments(arguments)
            return database.add_research_plan(
                args["short_summary"],
                args["details"],
            )
        except Exception as error:
            return {"status": "error", "message": str(error)}


class GetResearchPlansTool(Tool):
    name = "get_research_plans"
    description = "Gets a user's research plans from the database."
    parameters = {}

    def execute(self, arguments: str) -> list[dict[str, Any]]:
        try:
            return database.get_research_plans()
        except Exception as error:
            return [{"status": "error", "message": str(error)}]


class DeleteResearchPlanTool(Tool):
    name = "delete_research_plan"
    description = "Deletes a user's research plan from the database."
    parameters = {
        "id": {
            "type": "integer",
            "description": "The ID of the research plan to delete.",
        },
    }

    def execute(self, arguments: str) -> dict[str, Any]:
        try:
            args = self.parse_arguments(arguments)
            return database.delete_research_plan(args["id"])
        except Exception as error:
            return {"status": "error", "message": str(error)}


def build_research_planner_tools() -> list[Tool]:
    return [
        StoreResearchPlanTool(),
        GetResearchPlansTool(),
        DeleteResearchPlanTool(),
    ]
