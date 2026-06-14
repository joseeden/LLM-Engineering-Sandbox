CREATE TABLE
IF NOT EXISTS invoices
(
    id INTEGER PRIMARY KEY,
    vendor_name TEXT,
    vendor_address TEXT,
    vendor_tax_id TEXT,
    customer_name TEXT,
    customer_address TEXT,
    customer_tax_id TEXT,
    invoice_number TEXT,
    date TEXT,
    total_amount REAL,
    tax REAL
);