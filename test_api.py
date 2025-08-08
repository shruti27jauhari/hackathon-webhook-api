import requests
import json

# API Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEAM_TOKEN = "6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8"

# Sample request from hackathon
sample_request = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("✅ Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_run_queries():
    """Test the main query endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {TEAM_TOKEN}"
    }
    
    try:
        print("🚀 Testing /hackrx/run endpoint...")
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=headers,
            json=sample_request
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Sample answers:")
            for i, answer in enumerate(result['answers'], 1):
                print(f"Q{i}: {answer[:100]}...")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_invalid_token():
    """Test with invalid token"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer invalid_token"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=headers,
            json=sample_request
        )
        
        if response.status_code == 401:
            print("✅ Authentication working correctly")
            return True
        else:
            print(f"❌ Authentication test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing HackRX RAG API")
    print("=" * 50)
    
    # Test health check
    health_ok = test_health_check()
    print()
    
    # Test authentication
    auth_ok = test_invalid_token()
    print()
    
    # Test main functionality
    if health_ok:
        main_ok = test_run_queries()
        print()
        
        if main_ok:
            print("🎉 All tests passed! API is ready for submission.")
        else:
            print("⚠️ Main functionality test failed. Check the API logs.")
    else:
        print("❌ Health check failed. Make sure the API is running.") 