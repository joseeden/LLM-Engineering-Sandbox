import csv
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"
DB_FILE = BASE_DIR / "dummy_database.db"


def load_sql_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    return file_path.read_text(encoding="utf-8")


def load_customers(file_path: Path) -> list[tuple[int, str, str, str]]:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with file_path.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        return [
            (
                int(row["customer_id"]),
                row["first_name"],
                row["last_name"],
                row["pin"],
            )
            for row in rows
        ]


def load_orders(
    file_path: Path,
    customer_ids: set[int],
) -> list[tuple[int, str, str, float]]:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    orders = []
    with file_path.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)

        for row in rows:
            customer_id = int(row["customer_id"])

            if customer_id not in customer_ids:
                raise ValueError(f"Order references unknown customer ID: {customer_id}")

            order_date = datetime.now() - timedelta(days=int(row["days_ago"]))
            orders.append(
                (
                    customer_id,
                    order_date.isoformat(),
                    row["product_name"],
                    float(row["amount"]),
                )
            )

    return orders


def create_db_and_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.executescript(load_sql_file(SQL_DIR / "create_tables.sql"))
    cursor.executescript(load_sql_file(SQL_DIR / "reset_tables.sql"))

    customers = load_customers(DATA_DIR / "customers.csv")
    cursor.executemany(
        load_sql_file(SQL_DIR / "insert_customer.sql"),
        customers,
    )

    customer_ids = {customer[0] for customer in customers}
    orders = load_orders(DATA_DIR / "orders.csv", customer_ids)
    cursor.executemany(
        load_sql_file(SQL_DIR / "insert_order.sql"),
        orders,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db_and_tables()
    print("Database created and populated successfully.")
