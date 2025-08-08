#!/usr/bin/env python3
"""
Railway Deployment Helper Script
This script helps you deploy your API to Railway for the hackathon webhook.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        # Use shell=True for Windows compatibility
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_railway_cli():
    """Check if Railway CLI is available"""
    print("\n📋 Checking Railway CLI installation...")
    
    # Try different ways to check for Railway CLI
    commands_to_try = [
        "railway --version",
        "railway --help",
        "npx railway --version"
    ]
    
    for cmd in commands_to_try:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Railway CLI is available")
                return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            continue
    
    print("❌ Railway CLI not found. Please install it first:")
    print("   npm install -g @railway/cli")
    print("   Then run: railway login")
    return False

def check_railway_login():
    """Check if user is logged into Railway"""
    print("\n🔐 Checking Railway login status...")
    try:
        result = subprocess.run("railway whoami", shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Logged into Railway")
            return True
        else:
            print("❌ Not logged into Railway. Please run: railway login")
            return False
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("❌ Not logged into Railway. Please run: railway login")
        return False

def main():
    print("🚀 Railway Deployment Setup for Hackathon Webhook")
    print("=" * 50)
    
    # Check if Railway CLI is installed
    if not check_railway_cli():
        return
    
    # Check if user is logged in
    if not check_railway_login():
        return
    
    # Create new project or link to existing
    print("\n🏗️  Setting up Railway project...")
    project_output = run_command("railway init", "Initializing Railway project")
    if not project_output:
        print("❌ Failed to initialize Railway project")
        return
    
    # Deploy the application
    print("\n🚀 Deploying to Railway...")
    deploy_output = run_command("railway up", "Deploying application")
    if not deploy_output:
        print("❌ Failed to deploy to Railway")
        return
    
    # Get the deployment URL
    print("\n🌐 Getting deployment URL...")
    url_output = run_command("railway domain", "Getting domain")
    if url_output:
        domain = url_output.strip()
        webhook_url = f"https://{domain}/api/v1/hackrx/run"
        print(f"\n🎉 Deployment successful!")
        print(f"📡 Your webhook URL: {webhook_url}")
        print(f"\n📝 Copy this URL and submit it to the hackathon platform!")
        print(f"🔗 Health check: https://{domain}/api/v1/health")
    else:
        print("❌ Failed to get deployment URL")

if __name__ == "__main__":
    main() 