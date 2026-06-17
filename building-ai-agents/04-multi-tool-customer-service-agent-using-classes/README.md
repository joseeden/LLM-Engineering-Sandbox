# Multi-Tool Customer Service Agent Using Classes

## Overview

This project builds on the same customer service agent as [Multi-Tool Customer Service Agent](https://github.com/joseeden/LLM-Engineering-Sandbox/blob/master/building-ai-agents/03-multi-tool-customer-service-agent/README.md), but this version organizes the implementation with Python classes.

The agent can verify a customer, retrieve order history, check refund eligibility, issue a simulated refund, and collect customer feedback.

The main difference is architecture:

- The previous project uses plain functions and dictionaries.
- This project uses *Classes* and each customer service tool is encapsulated in its own class.

<!-- The prompt, tool schemas, SQL commands, and seed data are externalized into folders so the Python files stay focused on application logic. -->

<!-- ## Use Case

Customer support agents need to verify identity before showing private customer or order information.

They also need to retrieve order data, follow refund rules, and ask for confirmation before taking important actions.

This project demonstrates the same workflow as the previous multi-tool agent, but with an object-oriented structure that is easier to extend as the number of tools grows. -->

## Workflow

The workflow processes each customer message in a tool-calling loop.

1. Rebuild the local SQLite database from CSV seed data.
2. Load the customer service developer prompt from `prompts/developer-prompt.txt`.
3. Register Python tool classes with the customer service agent.
4. Generate OpenAI tool schemas from the registered tool classes.
5. Read the customer message from the command line.
6. Send the conversation and available tools to the model.
7. Execute the requested tool class when the model asks for one.
8. Send the tool result back to the model.
9. Print the final assistant response.

## Project Structure

```text
04-multi-tool-customer-service-agent-using-classes/
├── data/
│   ├── customers.csv
│   └── orders.csv
├── prompts/
│   └── developer-prompt.txt
├── sql/
│   ├── check_refund_eligibility.sql
│   ├── create_tables.sql
│   ├── get_orders.sql
│   ├── insert_customer.sql
│   ├── insert_order.sql
│   ├── reset_tables.sql
│   ├── select_customer_ids.sql
│   └── verify_customer.sql
├── agents.py
├── customer_service_tools.py
├── database.py
├── file_utils.py
├── main.py
├── pyproject.toml
└── README.md
```

As mentioned, the previous project [Multi-Tool Customer Service Agent](https://github.com/joseeden/LLM-Engineering-Sandbox/blob/master/building-ai-agents/03-multi-tool-customer-service-agent/README.md) and this project solve the same problem. 

Both projects use:

- The OpenAI Responses API
- Tool calling
- A local SQLite database
- CSV seed data
- External SQL files
- An external developer prompt
- Tool schemas generated from Python tool classes

However, this project changes the internal Python structure.

| Area          | Previous project              | This project                                       |
| ------------- | ----------------------------- | -------------------------------------------------- |
| Agent flow    | Written directly in `main.py` | Encapsulated in `Agent` and `CustomerServiceAgent` |
| Tool logic    | Plain Python functions        | One class per tool                                 |
| Tool registry | Function dictionary           | Tool object registry                               |
| Entry point   | `main.py` contains most logic | `main.py` starts the app only                      |
| Extensibility | Simple and direct             | Easier to grow and manage                          |

## Main Python Files

### `main.py`

This is the application entry point.

It loads environment variables, rebuilds the database, creates the customer service agent, and starts the chat loop.

### `agents.py`

This contains the object-oriented agent classes.

| Class                  | Purpose                                                                  |
| ---------------------- | ------------------------------------------------------------------------ |
| `Agent`                | Manages the OpenAI client, prompts, tools, messages, and tool execution. |
| `CustomerServiceAgent` | Registers customer service tools and runs the chat loop.                 |

### `customer_service_tools.py`

This contains the tool classes.

Each tool class owns the Python logic for one tool call.

| Class                         | Purpose                                         |
| ----------------------------- | ----------------------------------------------- |
| `Tool`                        | Base class for all tools.                       |
| `VerifyCustomerTool`          | Verifies customer identity.                     |
| `GetOrdersTool`               | Retrieves customer orders.                      |
| `CheckRefundEligibilityTool`  | Checks if a customer is eligible for a refund.  |
| `IssueRefundTool`             | Issues a refund to a customer.                  |
| `ShareFeedbackTool`           | Shares customer feedback.                       |



### `database.py`

This builds the local SQLite database from external SQL files and CSV seed data.

The database is rebuilt when the app starts, so changes to `data/customers.csv` or `data/orders.csv` are picked up on the next run.

### `file_utils.py`

This contains small helper functions for loading text, JSON, and SQL files.

## External Files

### Prompts

The `prompts/` folder contains the developer prompt used to guide the agent's behavior.

```text
prompts/
└── developer-prompt.txt
```

This makes the agent instructions easier to update without editing Python code.

### Tool Schemas

The `tools/` folder used to contain the OpenAI tool definitions passed to the model.

```text
tools/
└── customer-service-tools.json
```

**Update:** The JSON file was removed to reduce duplication. The tool classes in `customer_service_tools.py` are now the single source of truth for tool names, descriptions, parameters, and execution logic.

The schema metadata and runtime behavior is now defined in each tool class. The agent registers those classes and generates the OpenAI tool schemas from them.

```python
tools=self.get_tool_schemas()
```

The model receives those generated schemas, chooses a tool by name, and then the matching Python class executes the tool call.

```python
return self.tools[fn_name].execute(tool_call.arguments) 
```

The `main.py` file only passes the model and developer prompt file to the `CustomerServiceAgent`.

```python
agent = CustomerServiceAgent(
    model=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
    developer_prompt_file=DEVELOPER_PROMPT_FILE,
)
```

### SQL Files

The `sql/` folder contains database setup commands and query files.

```text
sql/
├── check_refund_eligibility.sql
├── create_tables.sql
├── get_orders.sql
├── insert_customer.sql
├── insert_order.sql
├── reset_tables.sql
├── select_customer_ids.sql
└── verify_customer.sql
```

This keeps SQL separate from the Python tool and database code.

### Seed Data

The `data/` folder contains CSV files used to populate the local SQLite database.

`database.py` reads these files when the app starts, inserts each customer into the `customers` table, and then creates sample orders in the `orders` table.

```text
data/
├── customers.csv
└── orders.csv
```

The `customers.csv` file uses these columns:

| Column        | Purpose                                 |
| ------------- | --------------------------------------- |
| `customer_id` | The customer's primary key.             |
| `first_name`  | The customer's first name.              |
| `last_name`   | The customer's last name.               |
| `pin`         | The PIN used for customer verification. |

The `orders.csv` file uses these columns:

| Column         | Purpose                                 |
| -------------- | --------------------------------------- |
| `customer_id`  | The customer ID linked to `customers`.  |
| `days_ago`     | How many days ago the order was placed. |
| `product_name` | The purchased product name.             |
| `amount`       | The order amount.                       |


To add or change test records, update `data/customers.csv` or `data/orders.csv` and restart the app so the database is rebuilt with the new seed data.

These records are stored in `dummy_database.db`, which is rebuilt each time the app starts, so any changes made directly to the database will be lost when the app restarts. 

1. To create the database manually without running the app:

    ```bash
    uv run python database.py
    ```

2. To check the tables in the database:

    ```bash
    sqlite3 dummy_database.db ".tables"
    ```

    Output:

    ```bash
    customers  orders
    ```

3. To check the users in the `customers` table:

    ```bash
    sqlite3 -header -column dummy_database.db "SELECT * FROM customers;"  
    ```

    Output:

    ```bash
    id  first_name  last_name  pin 
    --  ----------  ---------  ----
    1   John        Doe        1234
    2   Jane        Smith      5678
    3   Alex        Coal       2468
    4   Jon         Snow       1357
    5   David       Brown      1122
    6   Walter      White      3344
    7   Michael     Scott      5566
    8   Sarah       Miller     7788
    9   Chris       Anderson   9900
    10  Jessica     Thomas     4321
    11  Daniel      Moore      8765
    12  Laura       Martin     1212
    13  James       Jackson    3434
    14  Olivia      White      5656
    15  Robert      Harris     7878
    16  Sophia      Clark      9090
    17  William     Lewis      1010
    18  Emma        Walker     2020
    19  Benjamin    Hall       3030
    20  Ava         Young      4040
    ```
4. To check the orders in the `orders` table:

    ```bash
    sqlite3 -header -column dummy_database.db "SELECT * FROM orders;"  
    ```

    **Note:** There are 71 total orders, where each customer has more than one order. 

    Output:

    ```bash
    id  customer_id  date                        product_name        amount
    --  -----------  --------------------------  ------------------  ------
    1   1            2026-06-07T15:49:41.102957  Laptop              1200.0
    2   1            2026-05-03T15:49:41.102991  Mouse               25.0  
    3   1            2026-06-13T15:49:41.103001  Laptop Stand        42.0  
    4   2            2026-06-12T15:49:41.103007  Keyboard            75.0  
    5   2            2026-05-17T15:49:41.103017  Desk Mat            22.0  
    6   3            2026-05-03T15:49:41.103023  Mouse               25.0 
    ....
    ...
    ```

## Prerequisites

- Python 3.12+
- `uv`
- An OpenAI account
- OpenAI API credentials

## Setup

1. Go to this project folder.

    ```bash
    cd project-llm-engineering-sandbox/building-ai-agents/04-multi-tool-customer-service-agent-using-classes
    ```

2. Copy the environment file.

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables.

    ```env
    OPENAI_API_KEY=your_openai_key_here
    OPENAI_BASE_URL=https://api.openai.com/v1
    MODEL_NAME=gpt-5-nano
    ```

    **Note:** Never commit real API keys to source control.

4. Install dependencies.

    ```bash
    uv sync
    ```

## Run The Application

Run the chatbot from this project folder.

```bash
uv run python main.py
```

The app starts a command-line chat session.

```text
Welcome to the customer service chatbot.
How can we help you today?
Type 'exit' to end the conversation.

Your input:
```

You can test with a sample customer from `data/customers.csv`.

```text
Jon Snow 1357
```

Try asking for a refund first. The assistant should ask for identity verification before sharing order details or checking refund eligibility.

<div class='img-center'>

![](../images/17062026-multitool-agent-2.GIF)

</div>


## Notes on Externalized Files

The prompts, tool schemas, SQL commands, and seed data are externalized into folders so the Python files stay focused on application logic.

- `main.py` stays small.
- Agent behavior is isolated in `agents.py`.
- Tool behavior is isolated in `customer_service_tools.py`.
- External files can be changed without editing the core agent loop.

This is still a learning project, but the structure is closer to how a larger agent application would be organized.
