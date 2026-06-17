# Multi-Tool Customer Service Agent

## Overview

This project builds a simple customer service chatbot with an AI agent and multiple backend tools.

The agent can verify a customer, retrieve order history, check refund eligibility, issue a simulated refund, and collect customer feedback.

The agent uses OpenAI tool calling so the model can decide when to call a Python function and then use the function result in the conversation.

## Use Case

Customer support often requires the assistant to check identity before sharing private information.

It also requires the assistant to retrieve order data, follow refund rules, and ask for confirmation before taking important actions.

This project shows how an AI agent can coordinate those steps while keeping customer data access inside controlled backend functions.

## Workflow

The workflow processes each customer message in a tool-calling loop.

1. Load the customer service developer prompt
2. Read the customer message from the command line
3. Send the conversation and available tools to the model
4. Execute the requested tool when the model asks for one
5. Send the tool result back to the model
6. Print the final assistant response

Each tool has a focused responsibility, and the agent combines them during the conversation.


## Project Structure

```text
03-multi-tool-customer-service-agent/
│
├── prompts/
│   └── developer-prompt.txt
│
├── sql/
│   ├── check_refund_eligibility.sql
│   ├── create_tables.sql
│   ├── get_orders.sql
│   ├── insert_customer.sql
│   ├── insert_order.sql
│   ├── reset_tables.sql
│   └── verify_customer.sql
│
├── tools
│   └── customer-service-tools.json
|
├── main.py
├── database.py
|
├── pyproject.toml
└── README.md
```


## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [An OpenAI account](https://platform.openai.com/login)
- [OpenAI API credentials](https://platform.openai.com/account/api-keys)

## Setup

1. Clone the repository.

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox
    cd project-llm-engineering-sandbox/building-ai-agents/03-multi-tool-customer-service-agent
    ```

2. Copy the environment file.

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables.

    Open `.env` and update the values.

    ```env
    OPENAI_API_KEY=your_openai_key_here
    OPENAI_BASE_URL="https://api.openai.com/v1"
    MODEL_NAME=gpt-5-nano
    ```

    **NOTE:** Never commit real API keys to source control.

4. Install dependencies.

    From the project directory, run:

    ```bash
    uv sync
    ```

### Prompts

The `prompts/` directory contains the text file with the customer service instruction prompts used to guide the agent's behavior.

This keeps the Python code cleaner and makes the agent behavior easier to update.

```text
prompts/
└── developer-prompt.txt
```


### SQL Files

The `sql/` directory contains SQL scripts for setting up the database, inserting sample data, and running queries.

This keeps the table creation and seed data commands separate from the Python database setup code.

```text
sql/
├── check_refund_eligibility.sql
├── create_tables.sql
├── get_orders.sql
├── insert_customer.sql
├── insert_order.sql
├── reset_tables.sql
└── verify_customer.sql
```

### Seed Data

The `data/` directory contains CSV seed data used to populate the local SQLite database.

`database.py` reads these files when the app starts, inserts each customer into the `customers` table, and then creates sample orders in the `orders` table.

```text
data/
customers.csv
orders.csv
```

The `customers.csv` file uses these columns:

| Column       | Purpose                                 |
| ------------ | --------------------------------------- |
| `customer_id` | The customer's primary key.             |
| `first_name` | The customer's first name.              |
| `last_name`  | The customer's last name.               |
| `pin`        | The PIN used for customer verification. |

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



### Tools

The agent has five customer service tools.

| Function                   | Purpose                                              |
| -------------------------- | ---------------------------------------------------- |
| `verify_customer`          | Verifies the customer name and PIN.                  |
| `get_orders`               | Retrieves the order history of a verified customer.  |
| `check_refund_eligibility` | Checks whether an order is within the refund period. |
| `issue_refund`             | Simulates issuing a refund after confirmation.       |
| `share_feedback`           | Collects customer feedback.                          |

These tools are defined in the `tools/customer-service-tools.json` file, which is loaded at runtime and passed to the model as available tools.

### Loops 

The application is structured around two main loops:

1. The main loop that processes customer messages and interacts with the model.

    This allows the agent to have a continuous conversation with the customer, where each message can trigger tool calls as needed.

    ```python
    while True:
        user_input = input("Your input: ")

        if user_input == "exit":
            break

        messages.append({"role": "user", "content": user_input})
    ```

2. The tool-calling loop that executes when the model requests a tool.

    This loop runs the corresponding function, and sends the result back to the model. To prevent infinite loops, the number of tool calls is limited to 5 per session.

    This means that the model can call up to 5 tools during the conversation, and after that, it will stop calling tools and just generate responses.

    ```python
    for _ in range(5):
        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=tools,
        )

        ...
    ```

## Run the Application

Run the chatbot from the project directory.

```bash
uv run python main.py
```

It will return a welcome message and prompt for user input.

```text
Welcome to the customer service chatbot. 
How can we help you today? 
Type 'exit' to end the conversation.

Your input: 
```

You can try asking for a refund:

```text
Your input: I'd like to ask for a refund


The assistant should ask for identity verification before sharing order details.

You can test with the sample customers in `data/customers.csv`.

```text
John Doe, PIN 1234
Jane Smith, PIN 5678
```

## Validation

After running the app, the script creates a local SQLite database named `dummy_database.db`.

The database loads sample customers from `data/customers.csv` and creates sample orders for testing the agent.

The app should ask for verification before showing orders, and it should check refund eligibility before issuing a refund.

## Portfolio Note

This project is a useful AI agent lab.

It demonstrates tool calling, customer verification, database access, refund policy checks, and prompt externalization.

It is better as part of an AI agent learning collection than as a standalone flagship portfolio project.
