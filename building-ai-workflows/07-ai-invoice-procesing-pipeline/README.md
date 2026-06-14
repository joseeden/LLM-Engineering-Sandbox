## AI Invoice Processing Pipeline

This project automates invoice processing using PDF parsing, AI-powered data extraction, and database storage.

Instead of manually reviewing invoices, the workflow extracts key information from PDF documents and converts it into structured records that can be stored and processed automatically.

The goal is to transform unstructured invoice documents into structured data that can be used by other systems.

## Workflow 

The workflow processes invoices in multiple steps.

1. Load one or more PDF invoices              
2. Extract text from each PDF                 
3. Send the text to an LLM                    
4. Extract invoice details as structured JSON 
5. Store the extracted data in SQLite         

Each step has a single responsibility, which makes the workflow easier to understand and maintain.

### 1. Using Code to Extract Content 

Before sending data to an LLM, the workflow extracts text directly from the PDF using Python. While this can be done with an LLM, it is more efficient to use code for this step because:

- It reduces AI requests
- It reduces processing costs
- It keeps the workflow simple

Since PDF text extraction can be performed locally, there is no need to use an LLM for this task.

### 2. Structured Extraction 

After the text is extracted, it is sent to an LLM for invoice processing.

The model is responsible for identifying important invoice details such as:

- Vendor information
- Customer information
- Invoice number
- Invoice date
- Tax amount
- Total amount

Instead of returning free-form text, the model returns structured JSON that follows a predefined schema.

This structured output makes the extracted data easier to validate, store, and process.

### 3. Database Storage

After invoice data is extracted, the workflow stores the results in a SQLite database.

- Stores invoice records
- Supports future reporting
- Supports automation workflows
- Makes searching easier

The database becomes the final destination for the extracted invoice information.

## Use Case 

Many business documents contain valuable information, but that information is often locked inside PDFs.

This workflow combines PDF processing, structured AI outputs, and database storage to automatically convert invoice documents into structured records.

The result is a simple AI-powered document processing pipeline that can be extended to support reporting, analytics, automation, or integrations with other systems.

## Project Structure

```text