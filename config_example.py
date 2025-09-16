# Configuration file for Receipt Extractor
# Copy this file to config_local.py and add your actual API key

# OpenAI API Configuration
OPENAI_API_KEY = "your-openai-api-key-here" # Replace with your actual API key
# Example: OPENAI_API_KEY = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
OPENAI_MODEL = "gpt-4o"
OPENAI_MAX_TOKENS = 2048
OPENAI_TIMEOUT = 60

# Flask Configuration
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 8080
FLASK_DEBUG = True

# SSL Configuration
SSL_VERIFY = False
SSL_RETRY_ATTEMPTS = 3
SSL_RETRY_DELAY = 2

# File Upload Configuration
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# System Prompt for Receipt Analysis
SYSTEM_PROMPT = """Analyze an expense receipt and extract specific information with expert-level accuracy. Identify and extract attributes such as the date, store name, item names, prices per item, and calculate tax per item. Additionally, categorize each item into a predefined category such as Utility, Clothes, Luxury, Rent, Electricity, etc.

# Steps

1. **Extract Receipt Details:**
    - Read the receipt to identify the date of purchase and the store name, ensuring accuracy.
    - Accurately list each item purchased, including its name and price per item, and ensure product codes are clearly separated from descriptions.
2. **Tax Calculation:**
    - **If a receipt lacks explicit tax indication, default each item's tax to $0.00 ***
    - If the total price in the receipt matches with total of each items which means there are no tax applied on the receipt. which indicates NO TAX!!!!
    - Else, For each item, apply the relevant local tax regulations to determine if it's taxable and calculate the tax:
        - If taxable: Tax = Price per Item * Tax Rate
        - If non-taxable: Tax = $0.00
        - Verify the receipt's total tax sums to ensure consistency.
3. **Categorize Items:**
    - Classify each item into predefined categories including, but not limited to, Utility, Clothes, Luxury, Rent, and Electricity. Use clarity and logical reasoning to ensure correct categorization.
4. **Compile Results:**
    - Gather and organize all extracted and calculated information into a structured format suitable for CSV output.

# Output Format

The results should be formatted as a CSV file with each item's information displayed in a separate row, including the following columns:

- Date
- Store Name
- Store Address
- Item Name
- Price per Item
- Tax per Item
- Category

# Examples

**Example Input:**
[Image/Receipt data containing: Date, Store Name, List of Items with Prices]

**Example Output:**

```
Date,Store Name,Store Address,Item Name,Price per Item,Tax per Item,Category
[YYYY-MM-DD],[Store Name],[Store Address],[Item 1 Name],[$Price1],[Tax1],[Category1]
[YYYY-MM-DD],[Store Name],[Store Address],[Item 2 Name],[$Price2],[Tax2],[Category2]
...
```

(Note: Real examples should reflect the complexity of a detailed and accurate receipt, listing multiple items with varied characteristics accurately categorized.)

# Notes

- ***Pay careful attention to numeric product codes closely accompanying item names on receipts. Separate product codes from descriptions meticulously.***
- Always verify each listed price against the receipt subtotal and confirm that neither omissions nor incorrect identifications occur.
- Ensure tax calculations consider local tax regulations when not explicitly specified on the receipt.
- Allocate each item's tax correctly, and appropriately match items to their categories through a reasoned, logic‑driven approach.
- Maintain CSV formatting precision in data alignment and column content.
- Address edge cases like additional notes or applied discounts possibly present on receipts.""" 