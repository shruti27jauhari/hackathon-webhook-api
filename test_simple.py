#!/usr/bin/env python3
"""
Simple test for the webhook API
"""

import requests
import json

# Your live webhook URL
WEBHOOK_URL = "https://hackathon-webhook-api.onrender.com/api/v1/hackrx/run"

# Test with a real document URL (using a sample PDF)
test_data = {
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "questions": [
        "What is the grace period?",
        "What is the deductible?",
        "What benefits are covered?"
    ]
}

# Headers with authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8"
}

def test_webhook():
    """Test the webhook endpoint"""
    print("🧪 Testing webhook with real document...")
    try:
        response = requests.post(WEBHOOK_URL, json=test_data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Webhook API")
    print("=" * 30)
    test_webhook()
    print(f"\n📡 Your webhook URL: {WEBHOOK_URL}") 