#!/usr/bin/env python3
"""
Test script for the live webhook API
"""

import requests
import json

# Your live webhook URL
WEBHOOK_URL = "https://hackathon-webhook-api.onrender.com/api/v1/hackrx/run"
HEALTH_URL = "https://hackathon-webhook-api.onrender.com/api/v1/health"

# Test data
test_data = {
    "documents": "https://example.com/sample.pdf",  # Placeholder URL
    "questions": [
        "What is the grace period for premium payment?",
        "What is the deductible amount?",
        "What benefits are covered?"
    ]
}

# Headers with authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8"
}

def test_health_check():
    """Test the health check endpoint"""
    print("🧪 Testing health check...")
    try:
        response = requests.get(HEALTH_URL)
        print(f"✅ Health check response: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_webhook():
    """Test the main webhook endpoint"""
    print("\n🧪 Testing webhook endpoint...")
    try:
        response = requests.post(WEBHOOK_URL, json=test_data, headers=headers)
        print(f"✅ Webhook response: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def main():
    print("🚀 Testing Live Webhook API")
    print("=" * 40)
    
    # Test health check
    health_ok = test_health_check()
    
    # Test webhook
    webhook_ok = test_webhook()
    
    print("\n" + "=" * 40)
    if health_ok and webhook_ok:
        print("🎉 ALL TESTS PASSED! Your webhook is ready for the hackathon!")
        print(f"\n📡 Submit this URL to the hackathon:")
        print(f"   {WEBHOOK_URL}")
    else:
        print("❌ Some tests failed. Check the deployment.")
    
    print(f"\n🔗 Health check: {HEALTH_URL}")
    print(f"🔗 Webhook endpoint: {WEBHOOK_URL}")

if __name__ == "__main__":
    main() 