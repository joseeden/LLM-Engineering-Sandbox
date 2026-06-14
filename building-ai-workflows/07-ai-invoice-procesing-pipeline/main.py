import json
import sys
import os
import sqlite3
from pathlib import Path

import requests
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

BASE_DIR = Path(__file__).resolve().parent

PROMPT_FILE = BASE_DIR / "prompts" / "extract_invoice_prompt.txt"
CREATE_TABLE_SQL_FILE = BASE_DIR / "scripts" / "create_invoices_table.sql"
INSERT_INVOICE_SQL_FILE = BASE_DIR / "scripts" / "insert_invoice.sql"
INVOICE_SCHEMA_FILE = BASE_DIR / "schemas" / "invoice_schema.json"
DB_FILE = BASE_DIR / "invoices.db"


def load_text_file(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def load_json_file(file_path: Path) -> dict:
    return json.loads(file_path.read_text(encoding="utf-8"))


def setup_database():
    conn = sqlite3.connect(DB_FILE)

    create_table_sql = load_text_file(CREATE_TABLE_SQL_FILE)
    conn.executescript(create_table_sql)
    conn.commit()

    return conn


def insert_invoice_data(conn, invoice_data: dict):
    insert_sql = load_text_file(INSERT_INVOICE_SQL_FILE)

    values = (
        invoice_data.get("vendor", {}).get("name"),
        invoice_data.get("vendor", {}).get("address"),
        invoice_data.get("vendor", {}).get("taxId"),
        invoice_data.get("customer", {}).get("name"),
        invoice_data.get("customer", {}).get("address"),
        invoice_data.get("customer", {}).get("taxId"),
        invoice_data.get("invoiceNumber"),
        invoice_data.get("date"),
        invoice_data.get("totalAmount"),
        invoice_data.get("tax"),
    )

    conn.execute(insert_sql, values)
    conn.commit()


def get_pdf_content(pdf_path: Path) -> str:
    text = ""

    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

    return text.strip()


def load_prompt(pdf_content: str) -> str:
    prompt_template = load_text_file(PROMPT_FILE)
    return prompt_template.format(pdf_content=pdf_content)


def extract_invoice_details(pdf_content: str) -> dict:
    prompt = load_prompt(pdf_content)
    invoice_schema = load_json_file(INVOICE_SCHEMA_FILE)

    response = requests.post(
        OPENAI_BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        },
        json={
            "model": MODEL_NAME,
            "input": prompt,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "invoice",
                    "schema": invoice_schema,
                    "strict": True,
                }
            },
        },
    )

    response.raise_for_status()

    response_data = response.json()

    received_json = response_data.get("output_text")

    if not received_json:
        output = response_data.get("output", [])

        for item in output:
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    received_json = content.get("text")
                    break

            if received_json:
                break

    if not received_json:
        print(json.dumps(response_data, indent=2))
        raise ValueError("No JSON text found in the OpenAI response.")

    return json.loads(received_json)


def get_pdf_files(path: Path) -> list[Path]:
    if not path.exists():
        raise FileNotFoundError(f"The path '{path}' does not exist.")

    if path.is_file():
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"The file '{path}' is not a PDF file.")

        return [path]

    return sorted(path.glob("*.pdf"))


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python main.py files")
        return

    path = Path(sys.argv[1])
    pdf_files = get_pdf_files(path)

    if not pdf_files:
        print("No PDF files found.")
        return

    success_count = 0
    failed_count = 0

    conn = setup_database()

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}...")

        try:
            pdf_content = get_pdf_content(pdf_file)
            print(f"Extracted text length: {len(pdf_content)} characters")

            invoice_details = extract_invoice_details(pdf_content)
            insert_invoice_data(conn, invoice_details)

            success_count += 1

            print("Extracted Invoice Details:")
            print(json.dumps(invoice_details, indent=2))
            print("---------")

        except Exception as error:
            failed_count += 1
            print(f"An error occurred while processing {pdf_file}: {error}")

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM invoices")
    stored_invoice_count = cursor.fetchone()[0]

    conn.close()

    print("Processing summary:")
    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Invoices stored in database: {stored_invoice_count}")


if __name__ == "__main__":
    main()
