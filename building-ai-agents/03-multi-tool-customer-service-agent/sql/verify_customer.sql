SELECT id
FROM customers
WHERE LOWER(first_name) = ?
AND LOWER(last_name) = ?
AND pin = ?;
