#!/usr/bin/env python3
"""
GitHub Setup Script
This script helps you create a GitHub repository and push your code.
"""

import subprocess
import sys
import os

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

def main():
    print("🚀 GitHub Repository Setup")
    print("=" * 40)
    
    print("\n📋 Manual Steps to Create GitHub Repository:")
    print("1. Go to https://github.com")
    print("2. Click 'New repository'")
    print("3. Name it: hackathon-webhook-api")
    print("4. Make it Public")
    print("5. Don't initialize with README (we already have one)")
    print("6. Click 'Create repository'")
    
    print("\n🔗 After creating the repository, run these commands:")
    print("git remote add origin https://github.com/YOUR_USERNAME/hackathon-webhook-api.git")
    print("git branch -M main")
    print("git push -u origin main")
    
    print("\n💡 Replace YOUR_USERNAME with your actual GitHub username")
    
    # Ask if user wants to run the commands
    response = input("\n🤔 Do you want to run the git commands now? (y/n): ")
    if response.lower() == 'y':
        username = input("Enter your GitHub username: ")
        repo_name = input("Enter your repository name (or press Enter for 'hackathon-webhook-api'): ")
        if not repo_name:
            repo_name = "hackathon-webhook-api"
        
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        
        print(f"\n🔄 Adding remote origin: {remote_url}")
        run_command(f"git remote add origin {remote_url}", "Adding remote origin")
        
        print("\n🔄 Setting main branch...")
        run_command("git branch -M main", "Setting main branch")
        
        print("\n🔄 Pushing to GitHub...")
        run_command("git push -u origin main", "Pushing to GitHub")
        
        print(f"\n🎉 Success! Your code is now on GitHub:")
        print(f"https://github.com/{username}/{repo_name}")
        print(f"\n📝 You can now deploy to Render/Vercel using this repository!")

if __name__ == "__main__":
    main() 