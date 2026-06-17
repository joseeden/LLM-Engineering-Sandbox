import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from database import DB_FILE
from file_utils import load_sql_file


BASE_DIR = Path(__file__).resolve().parent
SQL_DIR = BASE_DIR / "sql"


class Tool:
    """
    Base class for tools that can be used by the customer service agent.
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

    def execute(self, arguments: str) -> str:
        raise NotImplementedError("Each tool must implement its own execute method.")

    def parse_arguments(self, arguments: str) -> dict[str, Any]:
        return json.loads(arguments)


class VerifyCustomerTool(Tool):
    name = "verify_customer"
    description = "Verifies a customer's identity using their full name and PIN."
    parameters = {
        "name": {
            "type": "string",
            "description": "The customer's full name, such as John Doe.",
        },
        "pin": {
            "type": "string",
            "description": "The customer's PIN.",
        },
    }

    def execute(self, arguments: str) -> str:
        try:
            args = self.parse_arguments(arguments)
            first_name, last_name = args["name"].lower().split()

            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    load_sql_file(SQL_DIR / "verify_customer.sql"),
                    (first_name, last_name, args["pin"]),
                )
                result = cursor.fetchone()

            if result:
                return str(result[0])

            return str(-1)
        except Exception as error:
            return f"Error in {self.name}: {error}"


class GetOrdersTool(Tool):
    name = "get_orders"
    description = "Retrieves the order history for a verified customer."
    parameters = {
        "customer_id": {
            "type": "integer",
            "description": "The customer's unique ID.",
        }
    }

    def execute(self, arguments: str) -> str:
        try:
            args = self.parse_arguments(arguments)

            with sqlite3.connect(DB_FILE) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    load_sql_file(SQL_DIR / "get_orders.sql"),
                    (args["customer_id"],),
                )
                orders = [dict(row) for row in cursor.fetchall()]

            return json.dumps(orders)
        except Exception as error:
            return f"Error in {self.name}: {error}"


class CheckRefundEligibilityTool(Tool):
    name = "check_refund_eligibility"
    description = "Checks if an order is eligible for a refund based on the order date."
    parameters = {
        "customer_id": {
            "type": "integer",
            "description": "The customer's unique ID.",
        },
        "order_id": {
            "type": "integer",
            "description": "The unique ID of the order.",
        },
    }

    def execute(self, arguments: str) -> str:
        try:
            args = self.parse_arguments(arguments)

            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    load_sql_file(SQL_DIR / "check_refund_eligibility.sql"),
                    (args["order_id"], args["customer_id"]),
                )
                result = cursor.fetchone()

            if not result:
                return str(False)

            order_date = datetime.fromisoformat(result[0])
            return str((datetime.now() - order_date).days <= 30)
        except Exception as error:
            return f"Error in {self.name}: {error}"


class IssueRefundTool(Tool):
    name = "issue_refund"
    description = "Issues a refund for an order."
    parameters = {
        "customer_id": {
            "type": "integer",
            "description": "The customer's unique ID.",
        },
        "order_id": {
            "type": "integer",
            "description": "The unique ID of the order.",
        },
    }

    def execute(self, arguments: str) -> str:
        try:
            args = self.parse_arguments(arguments)
            print(
                f"Refund issued for order {args['order_id']} "
                f"for customer {args['customer_id']}"
            )
            return str(True)
        except Exception as error:
            return f"Error in {self.name}: {error}"


class ShareFeedbackTool(Tool):
    name = "share_feedback"
    description = "Allows a customer to provide feedback about their experience."
    parameters = {
        "customer_id": {
            "type": "integer",
            "description": "The customer's unique ID.",
        },
        "feedback": {
            "type": "string",
            "description": "The feedback text from the customer.",
        },
    }

    def execute(self, arguments: str) -> str:
        try:
            args = self.parse_arguments(arguments)
            print(
                f"Feedback received from customer {args['customer_id']}: "
                f"{args['feedback']}"
            )
            return "Thank you for your feedback!"
        except Exception as error:
            return f"Error in {self.name}: {error}"


def build_customer_service_tools() -> list[Tool]:
    return [
        VerifyCustomerTool(),
        GetOrdersTool(),
        CheckRefundEligibilityTool(),
        IssueRefundTool(),
        ShareFeedbackTool(),
    ]
