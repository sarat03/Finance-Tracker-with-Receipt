"""
Receipt Extractor Module
Handles all the logic for extracting receipt data from images using OpenAI API
"""

import base64
import requests
from PIL import Image
import io
import urllib3
import ssl
import time

# Disable SSL warnings completely
urllib3.disable_warnings()

# Import configuration
try:
    from config import (
        OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS, OPENAI_TIMEOUT,
        SSL_VERIFY, SSL_RETRY_ATTEMPTS, SSL_RETRY_DELAY, SYSTEM_PROMPT
    )
except ImportError:
    # Fallback configuration if config.py is not available
    OPENAI_API_KEY = "your-openai-api-key-here"
    OPENAI_MODEL = "gpt-4o"
    OPENAI_MAX_TOKENS = 2048
    OPENAI_TIMEOUT = 60
    SSL_VERIFY = False
    SSL_RETRY_ATTEMPTS = 3
    SSL_RETRY_DELAY = 2
    SYSTEM_PROMPT = """Analyze an expense receipt and extract specific information with expert-level accuracy..."""

API_URL = "https://api.openai.com/v1/chat/completions"
USER_PROMPT = SYSTEM_PROMPT


class ReceiptExtractor:
    """Main class for extracting receipt data from images"""
    
    def __init__(self, api_key=None):
        """Initialize the extractor with optional custom API key"""
        self.api_key = api_key or OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.max_tokens = OPENAI_MAX_TOKENS
        self.timeout = OPENAI_TIMEOUT
        
    def image_to_base64(self, image_path_or_file):
        """
        Convert image to base64 string
        Accepts either file path (string) or file object
        """
        try:
            if isinstance(image_path_or_file, str):
                # File path provided
                with Image.open(image_path_or_file) as img:
                    buffered = io.BytesIO()
                    img.save(buffered, format="PNG")
                    return base64.b64encode(buffered.getvalue()).decode()
            else:
                # File object provided (from Flask upload)
                img = Image.open(image_path_or_file.stream)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            raise Exception(f"Error converting image to base64: {str(e)}")
    
    def create_ssl_session(self):
        """Create a session with aggressive SSL bypass"""
        session = requests.Session()
        session.verify = SSL_VERIFY
        
        # Configure SSL context
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_ciphers('DEFAULT@SECLEVEL=1')
        except:
            pass
        
        return session
    
    def make_api_call_with_retries(self, payload, headers, max_retries=None):
        """Make API call with multiple retry strategies"""
        max_retries = max_retries or SSL_RETRY_ATTEMPTS
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}")
                
                # Method 1: Session with SSL disabled
                session = self.create_ssl_session()
                response = session.post(
                    API_URL, 
                    json=payload, 
                    headers=headers, 
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    print("✅ API call successful!")
                    return response
                else:
                    print(f"❌ API returned status {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {str(e)[:100]}...")
                
                if attempt < max_retries - 1:
                    print(f"⏳ Waiting {SSL_RETRY_DELAY} seconds before retry...")
                    time.sleep(SSL_RETRY_DELAY)
        
        # If all attempts failed, try one last time with basic requests
        try:
            print("🔄 Final attempt with basic requests...")
            response = requests.post(
                API_URL, 
                json=payload, 
                headers=headers, 
                timeout=self.timeout, 
                verify=SSL_VERIFY
            )
            if response.status_code == 200:
                print("✅ Final attempt successful!")
                return response
        except Exception as e:
            print(f"❌ Final attempt failed: {e}")
        
        raise Exception("All API call attempts failed. Please check your internet connection and try again.")
    
    def extract_receipt_data(self, image_path_or_file):
        """
        Extract receipt data from image
        Accepts either file path (string) or file object
        """
        try:
            print(f"📸 Processing image...")
            
            # Convert image to base64
            image_b64 = self.image_to_base64(image_path_or_file)
            print("✅ Image converted to base64")
            
            # Prepare API payload
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": [
                        {"type": "text", "text": USER_PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
                    ]}
                ],
                "max_tokens": self.max_tokens
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make API call with retries
            response = self.make_api_call_with_retries(payload, headers)
            
            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code}\n{response.text}")
            
            result = response.json()
            extracted_data = result["choices"][0]["message"]["content"]
            
            print("✅ Receipt data extracted successfully")
            return extracted_data
            
        except Exception as e:
            print(f"❌ Error extracting receipt data: {e}")
            raise


# Convenience functions for backward compatibility
def extract_receipt_from_image(image_b64):
    """Legacy function - use ReceiptExtractor class instead"""
    extractor = ReceiptExtractor()
    # This function expects base64 string, but we need to handle it differently
    # For now, we'll create a temporary file or modify the approach
    raise NotImplementedError("Use ReceiptExtractor.extract_receipt_data() instead")


def image_file_to_base64(file_storage):
    """Legacy function - use ReceiptExtractor class instead"""
    extractor = ReceiptExtractor()
    return extractor.image_to_base64(file_storage)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python receipt_extractor.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    extractor = ReceiptExtractor()
    
    try:
        result = extractor.extract_receipt_data(image_path)
        print("\n" + "="*50)
        print("EXTRACTED RECEIPT DATA:")
        print("="*50)
        print(result)
        print("="*50)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 