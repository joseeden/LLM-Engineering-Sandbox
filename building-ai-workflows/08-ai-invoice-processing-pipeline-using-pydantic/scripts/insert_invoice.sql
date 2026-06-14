INSERT INTO invoices
  (
  vendor_name,
  vendor_address,
  vendor_tax_id,
  customer_name,
  customer_address,
  customer_tax_id,
  invoice_number,
  date,
  total_amount,
  tax
  )
VALUES
  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);