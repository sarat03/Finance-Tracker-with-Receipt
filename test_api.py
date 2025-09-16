#!/usr/bin/env python3
"""
Simple test script to verify OpenAI API key is working
"""

import requests
import json

def test_openai_api():
    """Test if OpenAI API key is working"""
    
    # Try to import config
    try:
        from config import OPENAI_API_KEY
        print(f"✅ Config loaded successfully")
        print(f"🔑 API Key: {OPENAI_API_KEY[:10]}..." if len(OPENAI_API_KEY) > 10 else "🔑 API Key: [too short]")
    except ImportError as e:
        print(f"❌ Error loading config: {e}")
        return False
    
    # Check if API key is still placeholder
    if OPENAI_API_KEY == "your-openai-api-key-here":
        print("❌ API key is still set to placeholder value!")
        print("📝 Please update the OPENAI_API_KEY in config.py with your actual API key")
        return False
    
    # Test API call
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "Hello! Please respond with 'API is working' if you can see this message."}
        ],
        "max_tokens": 50
    }
    
    try:
        print("🔄 Testing API connection...")
        response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ API test successful!")
            print(f"📝 Response: {message}")
            return True
        else:
            print(f"❌ API test failed with status {response.status_code}")
            print(f"📝 Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed with exception: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing OpenAI API Configuration")
    print("=" * 40)
    
    success = test_openai_api()
    
    print("=" * 40)
    if success:
        print("🎉 API is working correctly! You can now use the receipt extractor.")
    else:
        print("⚠️  API test failed. Please check your configuration.")
        print("\n📋 Troubleshooting steps:")
        print("1. Make sure you have a valid OpenAI API key")
        print("2. Update the OPENAI_API_KEY in config.py")
        print("3. Ensure you have internet connection")
        print("4. Check if your API key has sufficient credits") 