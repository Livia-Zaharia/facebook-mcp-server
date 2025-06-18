#!/usr/bin/env python3
"""
Facebook Token Refresh Script

This script helps you generate long-lived Facebook Page access tokens.
"""

import requests
import os
import sys
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

def get_long_lived_user_token(app_id: str, app_secret: str, short_token: str) -> str:
    """Exchange short-lived user token for long-lived one."""
    url = "https://graph.facebook.com/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_token
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "access_token" in data:
        return data["access_token"]
    else:
        raise Exception(f"Error getting long-lived user token: {data}")

def get_page_tokens(user_token: str) -> dict:
    """Get page access tokens using user token."""
    url = "https://graph.facebook.com/me/accounts"
    params = {"access_token": user_token}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "data" in data:
        return data["data"]
    else:
        raise Exception(f"Error getting page tokens: {data}")

def check_token_validity(token: str) -> dict:
    """Check token validity and expiration."""
    url = "https://graph.facebook.com/me"
    params = {"access_token": token}
    
    response = requests.get(url, params=params)
    return response.json()

def main():
    """Main function to refresh Facebook tokens."""
    print("🔑 Facebook Token Refresh Tool")
    print("=" * 40)
    
    # Get app credentials
    app_id = input("Enter your Facebook App ID: ").strip()
    app_secret = input("Enter your Facebook App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ App ID and App Secret are required!")
        sys.exit(1)
    
    print("\n📋 Steps to get a short-lived user token:")
    print("1. Go to: https://developers.facebook.com/tools/explorer/")
    print("2. Select your app")
    print("3. Click 'Generate Access Token'")
    print("4. Select these permissions:")
    print("   - pages_manage_posts")
    print("   - pages_read_engagement")
    print("   - pages_manage_metadata")
    print("   - pages_read_user_content")
    print("5. Copy the generated token")
    
    short_token = input("\nEnter your short-lived user access token: ").strip()
    
    if not short_token:
        print("❌ Short-lived token is required!")
        sys.exit(1)
    
    try:
        print("\n🔄 Exchanging for long-lived user token...")
        long_user_token = get_long_lived_user_token(app_id, app_secret, short_token)
        print("✅ Got long-lived user token!")
        
        print("\n📄 Getting page tokens...")
        pages = get_page_tokens(long_user_token)
        
        if not pages:
            print("❌ No pages found! Make sure you have page permissions.")
            sys.exit(1)
        
        print(f"\n📊 Found {len(pages)} page(s):")
        for i, page in enumerate(pages):
            print(f"{i+1}. {page['name']} (ID: {page['id']})")
        
        if len(pages) == 1:
            selected_page = pages[0]
        else:
            choice = int(input(f"\nSelect page (1-{len(pages)}): ")) - 1
            selected_page = pages[choice]
        
        page_token = selected_page['access_token']
        page_id = selected_page['id']
        page_name = selected_page['name']
        
        print(f"\n✅ Generated tokens for: {page_name}")
        print(f"📝 Page ID: {page_id}")
        print(f"🔑 Page Token: {page_token[:20]}...")
        
        # Check token validity
        print("\n🔍 Checking token validity...")
        validity = check_token_validity(page_token)
        if "error" not in validity:
            print("✅ Token is valid!")
        else:
            print(f"⚠️ Token validation warning: {validity}")
        
        # Update .env file
        update_env = input("\n💾 Update .env file with new tokens? (y/N): ").strip().lower()
        if update_env == 'y':
            env_content = f"""FACEBOOK_ACCESS_TOKEN={page_token}
FACEBOOK_PAGE_ID={page_id}
"""
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ Updated .env file!")
            print("\n🔄 Please restart your MCP server in Cursor!")
        else:
            print("\n📋 Add these to your .env file:")
            print(f"FACEBOOK_ACCESS_TOKEN={page_token}")
            print(f"FACEBOOK_PAGE_ID={page_id}")
        
        print("\n🎉 Token refresh completed!")
        print("⏰ This token will last approximately 60 days.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 