"""
Receipt Extractor Web Application
Clean, organized Flask app that uses separate modules
"""

from flask import Flask, render_template, request
import os

# Import our receipt extractor module
from receipt_extractor import ReceiptExtractor

# Import configuration
try:
    from config import (
        FLASK_HOST, FLASK_PORT, FLASK_DEBUG,
        ALLOWED_EXTENSIONS, MAX_FILE_SIZE
    )
except ImportError:
    # Fallback configuration
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 8080
    FLASK_DEBUG = True
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Initialize Flask app
app = Flask(__name__)

# Initialize receipt extractor
extractor = ReceiptExtractor()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [ext[1:] for ext in ALLOWED_EXTENSIONS]

def validate_file_size(file):
    """Check if file size is within limits"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    return size <= MAX_FILE_SIZE

@app.route('/', methods=['GET', 'POST'])
def upload_receipt():
    """Handle file upload and receipt extraction"""
    print("🟢 upload_receipt called, method:", request.method)
    csv = None
    error = None
    
    if request.method == 'POST':
        file = request.files.get('receipt')
        
        # Validate file upload
        if not file:
            error = "No file uploaded. Please select an image file."
        elif file.filename == '':
            error = "No file selected. Please choose an image file."
        else:
            try:
                # Validate file type
                if not allowed_file(file.filename):
                    error = f"Please upload a valid image file. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
                else:
                    # Validate file size
                    if not validate_file_size(file):
                        error = f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
                    else:
                        print(f"📸 Processing image: {file.filename}")
                        
                        # Check if API key is configured
                        if extractor.api_key == "your-openai-api-key-here":
                            error = "OpenAI API key not configured. Please update the API key in config.py"
                        else:
                            # Extract receipt data using our module
                            csv = extractor.extract_receipt_data(file)
                            print("✅ Receipt data extracted successfully")
                        
            except Exception as e:
                error = f"Error processing receipt: {str(e)}"
                print(f"❌ Error details: {e}")
                import traceback
                traceback.print_exc()
    
    return render_template('index.html', csv=csv, error=error)

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return render_template('index.html', error="File too large. Please choose a smaller image."), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server error"""
    return render_template('index.html', error="Internal server error. Please try again."), 500

def main():
    """Main function to run the application"""
    print("🚀 Starting Receipt Extractor Web App...")
    print("📱 Open your browser and go to: http://127.0.0.1:8080")
    print("⚠️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(
        debug=FLASK_DEBUG, 
        host=FLASK_HOST, 
        port=FLASK_PORT
    )

if __name__ == '__main__':
    main() 