#!/usr/bin/env python3
"""
Vercel Deployment Helper Script
This script helps you deploy your API to Vercel for the hackathon webhook.
"""

import subprocess
import sys
import os
import json

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def create_vercel_json():
    """Create vercel.json configuration file"""
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "api.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "api.py"
            }
        ]
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    print("✅ Created vercel.json configuration")

def create_requirements_vercel():
    """Create requirements.txt optimized for Vercel"""
    requirements = """fastapi
uvicorn
pydantic
requests
chromadb
sentence-transformers
pdfplumber
python-docx
ollama
llama-cpp-python
openllm
PyPDF2
nltk"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Updated requirements.txt for Vercel")

def main():
    print("🚀 Vercel Deployment Setup for Hackathon Webhook")
    print("=" * 50)
    
    # Create vercel.json configuration
    print("\n📝 Creating Vercel configuration...")
    create_vercel_json()
    create_requirements_vercel()
    
    print("\n📋 Manual Deployment Steps:")
    print("1. Install Vercel CLI: npm install -g vercel")
    print("2. Login to Vercel: vercel login")
    print("3. Deploy: vercel --prod")
    print("\n🌐 After deployment, your webhook URL will be:")
    print("   https://your-app-name.vercel.app/api/v1/hackrx/run")
    
    print("\n💡 Alternative: Deploy to Railway with paid plan")
    print("   Visit: https://railway.com/account/plans")

if __name__ == "__main__":
    main() 