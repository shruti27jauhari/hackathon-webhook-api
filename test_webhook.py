#!/usr/bin/env python3
"""
Test script for the webhook endpoint
Run this to verify your API works before deployment
"""

import requests
import json
import time
from api import app
import uvicorn
import threading

def test_webhook():
    """Test the webhook endpoint"""
    
    # Test data
    test_data = {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": [
            "What is this document about?",
            "What is the main topic?"
        ]
    }
    
    headers = {
        "Authorization": "Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8",
        "Content-Type": "application/json"
    }
    
    try:
        print("🧪 Testing webhook endpoint...")
        response = requests.post(
            "http://localhost:8000/api/v1/hackrx/run",
            json=test_data,
            headers=headers,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            return True
        else:
            print("❌ Webhook test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing webhook: {str(e)}")
        return False

def start_server():
    """Start the API server in a separate thread"""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def main():
    print("🚀 Starting API server for testing...")
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(5)
    
    # Test the webhook
    success = test_webhook()
    
    if success:
        print("\n🎉 Your webhook is ready for deployment!")
        print("📡 Webhook URL: https://your-domain.railway.app/api/v1/hackrx/run")
        print("\n📝 Next steps:")
        print("1. Deploy to Railway: python deploy_railway.py")
        print("2. Get your domain: railway domain")
        print("3. Submit the webhook URL to the hackathon platform")
    else:
        print("\n❌ Webhook test failed. Please check the logs above.")

if __name__ == "__main__":
    main() 