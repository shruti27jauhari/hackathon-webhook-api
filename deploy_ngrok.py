#!/usr/bin/env python3
"""
Ngrok Local Testing Setup
This script helps you test your webhook locally using ngrok.
"""

import subprocess
import sys
import os
import time
import requests

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

def check_ngrok_installation():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run("ngrok version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ngrok is installed")
            return True
        else:
            return False
    except:
        return False

def install_ngrok():
    """Install ngrok if not available"""
    print("\n📦 Installing ngrok...")
    print("Please install ngrok manually:")
    print("1. Go to https://ngrok.com/download")
    print("2. Download for Windows")
    print("3. Extract and add to PATH")
    print("4. Or run: npm install -g ngrok")
    return False

def start_api():
    """Start the API server"""
    print("\n🚀 Starting API server...")
    print("Starting uvicorn server on port 8000...")
    print("Keep this terminal open!")
    
    # Start the API server
    try:
        subprocess.run("python api.py", shell=True)
    except KeyboardInterrupt:
        print("\n⏹️  API server stopped")

def main():
    print("🚀 Ngrok Local Testing Setup")
    print("=" * 40)
    
    # Check ngrok installation
    if not check_ngrok_installation():
        install_ngrok()
        return
    
    print("\n📋 Setup Steps:")
    print("1. Start your API server (keep terminal open)")
    print("2. Open a new terminal and run: ngrok http 8000")
    print("3. Copy the ngrok URL (e.g., https://abc123.ngrok.io)")
    print("4. Your webhook URL will be: https://abc123.ngrok.io/api/v1/hackrx/run")
    
    print("\n🧪 Test your webhook:")
    print("python test_webhook.py")
    
    print("\n💡 This is for testing only. For production, use Render or Vercel.")
    
    # Ask if user wants to start the API now
    response = input("\n🤔 Start API server now? (y/n): ")
    if response.lower() == 'y':
        start_api()

if __name__ == "__main__":
    main() 