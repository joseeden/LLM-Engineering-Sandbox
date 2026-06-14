
# AI Invoice Processing Pipeline Using Pydantic

## Overview

This project is an enhancement of the previous [AI Invoice Processing Pipeline](https://github.com/joseeden/llm-engineering-sandbox/blob/master/building-ai-workflows/07-ai-invoice-procesing-pipeline/README.md)

The workflow automates invoice processing by extracting text from PDF files, using an LLM to parse the invoice details, and storing the results in a SQLite database.

It uses the same workflow:

1. Load one or more PDF invoices
2. Extract text from each PDF
3. Send the text to an LLM
4. Extract invoice details as structured JSON
5. Store the extracted data in SQLite

Each step has a single responsibility, which makes the workflow easier to understand and maintain.

For more information, please see [AI Invoice Processing Pipeline - Workflow Overview.](https://github.com/joseeden/llm-engineering-sandbox/blob/master/building-ai-workflows/07-ai-invoice-procesing-pipeline/README.md#workflow)

## Project Structure

```text
ai-invoice-processing-pipeline/
│
├── files
│   ├── invoice_001_northstar_cloud.pdf
│   ├── invoice_002_greenfield_office.pdf
│   ├── invoice_003_summit_security.pdf
│   ├── invoice_004_lumen_design.pdf
│   ├── invoice_005_evergreen_training.pdf
│   └── invoice_006_silverline_maintenance.pdf
│
├── prompts
│   └── extract_invoice_prompt.txt
│
├── scripts
│   ├── create_invoices_table.sql
│   └── insert_invoice.sql
│
├── pyproject.toml
├── invoices.db
├── main.py
└── README.md
```

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [An OpenAI account](https://platform.openai.com/login)
- [OpenAI API credentials](https://platform.openai.com/account/api-keys)

## Setup

1. Clone the repository

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox
    cd project-llm-engineering-sandbox/building-ai-workflows/08-ai-invoice-processing-pipeline-using-pydantic
    ```

2. Copy the environment file

    Create a `.env` file from the provided example:

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables

    Open `.env` and update the values.

    **NOTE:** NEVER commit your real API keys to source control.

    ```env
    OPENAI_API_KEY=your_openai_key_here
    OPENAI_BASE_URL="https://api.openai.com/v1"

    MODEL_NAME=your_model_name_here
    ```

    **Note:** The OpenAI SDK automatically appends the correct endpoint paths based on the method being called, so the base URL should just be this.

4. Install UV 

    Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Verify installation:

    ```bash
    uv --version
    ```

5. Install SQLite CLI (Optional, for database validation)

    Linux / macOS

    ```bash
    sudo apt update -y
    sudo apt install -y sqlite3
    ```

6. Install Dependencies

    From the project directory, run:

    ```bash
    uv sync
    ```

    This will:

    1. Create a virtual environment if needed
    2. Install all project dependencies
    3. Use the versions locked in `uv.lock`

## Using Pydantic for Structured Output

The previous version used a JSON schema file to define the expected invoice output.

This version uses **Pydantic** classes which are passed to the OpenAI SDK for structured output parsing.

- The response is returned as a parsed Python object
- The parsed object is easier to validate and store

This makes the code cleaner because the schema is now defined directly in Python.

:::info 

**Why use Pydantic**: Pydantic helps define the shape of the data that the AI should return. Instead of manually writing a long JSON schema, you can create Python classes.

It is easier to read, maintain, reuse, and validate the expected output structure with Pydantic models.

This is useful for invoice processing because invoices have predictable fields such as vendor, customer, invoice number, date, tax, and total amount.

:::

## Pydantic Models

There are three Pydantic models defined in the application: 

- `Vendor`
- `Customer`
- `Invoice`

These models represent the expected structure of the extracted invoice data.

```python
from pydantic import BaseModel

class Vendor(BaseModel):
    name: str
    address: str
    taxId: str

class Customer(BaseModel):
    name: str
    address: str
    taxId: str

class Invoice(BaseModel):
    vendor: Vendor
    customer: Customer
    invoiceNumber: str
    date: str
    totalAmount: float
    tax: float
```

These classes replace the separate `invoice_schema.json` file.

## Run the application

Run the application by specifying the path to the folder that contains the invoice PDF files.

```bash
uv run python main.py files
```

Output:

```text
Processing files/invoice-1.pdf...
Extracted text length: 1450 characters
Extracted Invoice Details:
{
  "vendor": {
    "name": "Sample Vendor",
    "address": "123 Business Street",
    "taxId": "TAX-12345"
  },
  "customer": {
    "name": "Sample Customer",
    "address": "456 Customer Avenue",
    "taxId": "TAX-67890"
  },
  "invoiceNumber": "INV-1001",
  "date": "2026-06-14",
  "totalAmount": 250.0,
  "tax": 25.0
}
---------
Processing summary:
Total PDFs found: 1
Successfully processed: 1
Failed: 0
Invoices stored in database: 1
```

The application processes all PDF files in the `files/` directory, extracts invoice details using the LLM, and stores the results in the `invoices.db` SQLite database.

View the actual records in the `invoices` table:

```bash
sqlite3 -header -column invoices.db \
"SELECT invoice_number, vendor_name, customer_name, total_amount, tax FROM invoices;"
```

Output:

```text
invoice_number  vendor_name                        customer_name               total_amount  tax   
--------------  ---------------------------------  --------------------------  ------------  ------
INV-2026-001    Northstar Cloud Services Pte Ltd   Harborlane Retail Group     1836.65       151.65
INV-2026-002    Greenfield Office Supplies         Cedar Peak Analytics        702.83        58.03 
INV-2026-003    Summit Security Consulting         Bluewave Logistics Pte Ltd  3052.0        252.0 
INV-2026-004    Lumen Creative Design Studio       Orchid Bay Foods            2387.1        197.1 
INV-2026-005    Evergreen Technical Training       Atlas Manufacturing Asia    2376.2        196.2 
INV-2026-006    Silverline Facilities Maintenance  Meridian Workspace Co.      1775.61       146.61
```

<div class='img-center'>

![](../images/1406206-multi-step-workflow-ai-invoice-processing.gif)

</div>


## Better Version

This version keeps the same invoice processing workflow, but it makes the structured output part easier to manage.

- The schema is written as Python classes
- The response is parsed automatically
- The code has less manual JSON handling
- The extracted data is easier to insert into the database

Pydantic makes the project easier to maintain because the expected invoice structure is defined directly in the application code.
