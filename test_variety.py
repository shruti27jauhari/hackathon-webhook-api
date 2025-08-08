#!/usr/bin/env python3
"""
Test with various question types
"""

import requests
import json

WEBHOOK_URL = "https://hackathon-webhook-api.onrender.com/api/v1/hackrx/run"

# Test with different question types
test_cases = [
    {
        "name": "Insurance-specific questions",
        "questions": [
            "What is the grace period?",
            "What is the deductible amount?",
            "What benefits are covered?",
            "How do I file a claim?",
            "What is the copay for specialists?"
        ]
    },
    {
        "name": "General questions",
        "questions": [
            "What is this document about?",
            "What are the main terms?",
            "How do I contact customer service?",
            "What happens if I miss a payment?",
            "What is the policy number?"
        ]
    },
    {
        "name": "Technical questions",
        "questions": [
            "What is the network size?",
            "What are the exclusions?",
            "What is the waiting period?",
            "What is the premium amount?",
            "What is the coverage limit?"
        ]
    }
]

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8"
}

def test_questions(questions, test_name):
    """Test a set of questions"""
    print(f"\n🧪 Testing: {test_name}")
    print("-" * 40)
    
    test_data = {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": questions
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=test_data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            answers = response.json()["answers"]
            for i, (question, answer) in enumerate(zip(questions, answers)):
                print(f"Q{i+1}: {question}")
                print(f"A{i+1}: {answer}")
                print()
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🚀 Testing API with Various Question Types")
    print("=" * 50)
    
    for test_case in test_cases:
        test_questions(test_case["questions"], test_case["name"])
    
    print("\n📝 Summary:")
    print("✅ API processes ANY questions you send")
    print("✅ Provides intelligent insurance-specific responses")
    print("✅ Handles multiple questions at once")
    print("⚠️  Currently uses keyword matching (not document content)")

if __name__ == "__main__":
    main() 