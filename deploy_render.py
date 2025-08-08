#!/usr/bin/env python3
"""
Render Deployment Helper Script
This script helps you deploy your API to Render for the hackathon webhook.
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

def create_render_yaml():
    """Create render.yaml configuration file"""
    render_config = """
services:
  - type: web
    name: hackathon-webhook
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_config)
    print("✅ Created render.yaml configuration")

def main():
    print("🚀 Render Deployment Setup for Hackathon Webhook")
    print("=" * 50)
    
    # Create render.yaml configuration
    print("\n📝 Creating Render configuration...")
    create_render_yaml()
    
    print("\n📋 Manual Deployment Steps:")
    print("1. Go to https://render.com")
    print("2. Sign up/Login with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Select this repository")
    print("6. Configure the service:")
    print("   - Name: hackathon-webhook")
    print("   - Environment: Python")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: uvicorn api:app --host 0.0.0.0 --port $PORT")
    print("7. Click 'Create Web Service'")
    print("\n🌐 After deployment, your webhook URL will be:")
    print("   https://your-app-name.onrender.com/api/v1/hackrx/run")
    
    print("\n💡 Alternative: Deploy to Railway with paid plan")
    print("   Visit: https://railway.com/account/plans")

if __name__ == "__main__":
    main() 