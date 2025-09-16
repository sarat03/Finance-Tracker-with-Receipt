# 📄 Receipt Extractor Web App

## Project Overview & Requirements

**Goal:**  
Build a Python web application that allows users to upload receipt images and extracts structured data from them using OpenAI's GPT-4 Vision API. The extracted data should be presented in a clean, downloadable CSV table, with a modern, user-friendly web interface.

---

### Functional Requirements

1. **Image Upload:**  
   - Users can upload receipt images (JPG, PNG, etc.) via a web interface.

2. **Data Extraction:**  
   - Use OpenAI's GPT-4 Vision API to extract structured data from the uploaded receipt image.
   - Extract the following fields for each item on the receipt:
     - Date
     - Store Name
     - Store Address
     - Item Name
     - Price per Item
     - Tax per Item
     - Category

3. **Output Format:**  
   - The extracted data must be returned as a CSV table (not Markdown, not a summary, not a list).
   - Each row should represent a single item from the receipt.
   - The table should have a header row with the field names above.

4. **Web Interface:**  
   - Display the extracted data in a styled HTML table.
   - Allow users to download the CSV file.
   - Show clear error messages if extraction fails.
   - Use a modern, responsive design for the UI.

5. **Backend:**  
   - Use Flask (or FastAPI) for the backend.
   - The backend should handle file uploads, call the GPT-4 Vision API, parse the response, and return the structured data.
   - The OpenAI API key should be securely managed (for demo, hardcoding is acceptable, but note security risks).

6. **Robustness:**  
   - Handle SSL issues gracefully (especially on macOS).
   - Provide clear instructions for installing dependencies and running the app.
   - Ensure the backend only passes the CSV/table data to the frontend (no Markdown summaries or mixed formats).

---

### Prompt for GPT-4 Vision API

**Use this as the user prompt when calling the LLM:**

> You are a receipt data extraction assistant.  
> Given an image of a retail receipt, extract the following fields for each item and output ONLY as a CSV table (no Markdown, no summary, no explanation, no lists):
> - Date
> - Store Name
> - Store Address
> - Item Name
> - Price per Item
> - Tax per Item
> - Category
>
> The CSV should have a header row with these field names.  
> Each row should represent a single item from the receipt.  
> If a field is missing, leave it blank.  
> Do not include any other text, explanation, or formatting—just the CSV table.

---

### Additional Implementation Notes

- Use the `requests` and `Pillow` libraries for backend image handling.
- Use `Flask` for the web server and HTML templating.
- Place HTML templates in a `templates/` directory.
- Use a virtual environment and a `requirements.txt` file for dependencies.
- Provide a `README.md` with setup and usage instructions.
- If running on macOS, document SSL troubleshooting steps (e.g., using Homebrew Python).

---

**Summary:**  
This project should allow a user to upload a receipt image, extract all relevant itemized data using GPT-4 Vision, and present it as a downloadable CSV table in a modern web interface, with robust error handling and clear separation of data and presentation.

## ✨ Features

- **Image Upload**: Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP)
- **AI-Powered Extraction**: Uses OpenAI GPT-4 Vision API for accurate data extraction
- **Structured Output**: Generates CSV format with organized columns
- **Tax Calculation**: Automatically calculates tax per item based on receipt data
- **Item Categorization**: Categorizes items into predefined categories (Utility, Clothes, Luxury, etc.)
- **SSL Compatibility**: Handles SSL certificate issues with multiple fallback methods
- **Modern UI**: Clean, responsive web interface with loading states
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Modular Architecture**: Clean separation of concerns with organized code structure

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ (recommended: Python 3.13 from Homebrew)
- OpenAI API key
- macOS (tested on macOS with Homebrew Python)

### Installation

1. **Clone or download the project files**

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**
   - Open `config.py`
   - Replace the `OPENAI_API_KEY` value with your OpenAI API key:
   ```python
   OPENAI_API_KEY = "your-openai-api-key-here"
   ```

5. **Verify your API key (optional but recommended):**
   ```bash
   python test_api.py
   ```
   - Expected: a short success message confirming the API is reachable

6. **Run the application:**

   **Option A: Organized Version (Recommended)**
   ```bash
   python run_organized.py
   ```
   
   **Option B: Direct Launch**
   ```bash
   python app_organized.py
   ```

7. **Open your browser and go to:**
   ```
   http://127.0.0.1:8080
   ```

## 📁 Project Structure

```
receipt-extractor/
├── 📁 Organized Version (Recommended)
│   ├── receipt_extractor.py      # Core extraction logic module
│   ├── app_organized.py          # Clean Flask application
│   ├── run_organized.py          # Organized launcher script
│   └── 📁 templates/
│       └── index.html            # Beautiful web interface
│
├── 📁 Configuration & Documentation
│   ├── config.py                 # Centralized configuration
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                 # This documentation
│   └── .gitignore               # Version control exclusions
│
├── 📁 Legacy Versions
│   ├── app_final.py             # Previous working version
│   ├── app_robust.py            # SSL-handling version
│   ├── app.py                   # Basic Flask version
│   ├── extract_receipt_v2.py    # Command-line version
│   └── extract_receipt.py       # Original command-line version
│
├── 📁 Assets
│   ├── IMG_0075.jpeg            # Sample receipt image
│   └── venv/                    # Virtual environment
│
└── run.py                       # Legacy launcher
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Upload Image**: Click "Choose Receipt Image" and select your receipt
2. **Extract Data**: Click "Extract Receipt Data" button
3. **View Results**: The CSV output will appear on the page

### Command Line

```bash
python receipt_extractor.py /path/to/your/receipt.jpg
```

## 📊 Output Format

The application extracts the following data in CSV format:

| Column | Description |
|--------|-------------|
| Date | Purchase date (YYYY-MM-DD) |
| Store Name | Name of the store/merchant |
| Store Address | Complete store address |
| Item Name | Name of the purchased item |
| Price per Item | Individual item price |
| Tax per Item | Tax amount for the item |
| Category | Item category (Clothes, Utility, etc.) |

### Example Output:
```csv
Date,Store Name,Store Address,Item Name,Price per Item,Tax per Item,Category
2025-03-30,H&M,Jersey Gardens Mall, 651 Kapkowski Road, Elizabeth, NJ 07201,Jersey Fancy Style P,$44.99,$0.00,Clothes
2025-03-30,H&M,Jersey Gardens Mall, 651 Kapkowski Road, Elizabeth, NJ 07201,Shirts Style Platfor,$39.99,$0.00,Clothes
```

## 🏗️ Architecture

### Organized Version Structure

- **`receipt_extractor.py`**: Core business logic
  - `ReceiptExtractor` class with all extraction methods
  - SSL handling and API communication
  - Image processing utilities

- **`app_organized.py`**: Web application layer
  - Flask routes and request handling
  - File validation and error handling
  - Clean separation from business logic

- **`templates/index.html`**: User interface
  - Modern, responsive design
  - Interactive JavaScript features
  - Professional styling

- **`config.py`**: Configuration management
  - API keys and settings
  - Environment-specific configurations
  - Centralized configuration

## 🔧 Technical Details

### SSL Issues Resolution

The application includes multiple SSL handling strategies to work around macOS SSL certificate issues:

1. **SSL Verification Disabled**: Uses `verify=False` for API calls
2. **Multiple Retry Methods**: Implements 3 retry attempts with different SSL configurations
3. **Cipher Configuration**: Uses `DEFAULT@SECLEVEL=1` for compatibility
4. **Session Management**: Custom session creation with SSL context

### API Configuration

- **Model**: GPT-4o (latest vision model)
- **Max Tokens**: 2048
- **Timeout**: 60 seconds
- **Retry Attempts**: 3

## 🛠️ Troubleshooting

### SSL Certificate Issues
If you encounter SSL errors, the app automatically handles them with multiple fallback methods. The organized version (`app_organized.py`) is recommended for macOS users.

### Port Already in Use
If port 8080 is busy, the app will show an error. You can:
- Stop other applications using port 8080
- Modify the port in `config.py`: `FLASK_PORT = 8081`

### API Key Issues
- Ensure your OpenAI API key is valid and has sufficient credits
- Check that you have access to the GPT-4o model
- Update the key in `config.py`

### Missing Files
If you get missing file errors:
- Ensure all files are in the correct directory structure
- Check that `templates/` folder contains `index.html`
- Verify `receipt_extractor.py` is in the root directory

## 📝 Dependencies

- **Flask**: Web framework
- **Pillow**: Image processing
- **Requests**: HTTP client
- **urllib3**: HTTP library
- **OpenAI API**: AI model access

## 🔒 Security Notes

- This is a development server - not suitable for production
- API keys are configured in `config.py` for local use only
- SSL verification is disabled for compatibility
- Use environment variables for production deployments

## 📄 License

This project is for educational and personal use. Please respect OpenAI's terms of service.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Happy Receipt Processing! 📄✨** 