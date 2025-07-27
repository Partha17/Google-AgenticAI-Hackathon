#!/usr/bin/env python3
"""
Simple test script to verify MCP connection and authentication
"""
import os
import sys
import requests
import json

def test_mcp_connection():
    """Test MCP connection directly"""
    
    # Use the same URL as deployed service
    base_url = "https://fi-mcp-server-bpzxyhr4dq-uc.a.run.app"
    auth_url = f"{base_url}/auth"
    test_url = f"{base_url}/mcp/test"
    
    print("🧪 Testing MCP Connection to Cloud Run...")
    print(f"Base URL: {base_url}")
    print(f"Auth URL: {auth_url}")
    print(f"Test URL: {test_url}")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 2: Authentication
    print("\n2️⃣ Testing Authentication...")
    auth_token = None
    session_id = None
    
    try:
        auth_payload = {"phoneNumber": "2222222222"}
        response = requests.post(
            auth_url,
            json=auth_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            auth_data = response.json()
            if auth_data.get("success"):
                auth_token = auth_data.get("token")
                session_id = auth_data.get("sessionId")
                print("   ✅ Authentication successful!")
                print(f"   Token: {auth_token}")
                print(f"   Session: {session_id}")
            else:
                print("   ❌ Authentication failed - no success field")
        else:
            print(f"   ❌ Authentication failed - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 3: Data Retrieval
    print("\n3️⃣ Testing Data Retrieval...")
    if auth_token and session_id:
        try:
            # Test with phone parameter
            response = requests.get(f"{test_url}?phone=2222222222", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ Data retrieval successful!")
                
                # Check net worth data
                net_worth = data.get("netWorthResponse", {}).get("totalNetWorthValue", {})
                if net_worth:
                    currency = net_worth.get("currencyCode", "INR")
                    amount = net_worth.get("units", "0")
                    print(f"   💰 Net Worth: {currency} {amount}")
                else:
                    print("   ⚠️ No net worth data found")
                    
            else:
                print(f"   ❌ Data retrieval failed - HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   Exception: {e}")
    else:
        print("   ⏭️ Skipping - no valid auth token")
    
    # Test 4: Multiple requests to check consistency
    print("\n4️⃣ Testing Consistency (5 auth attempts)...")
    success_count = 0
    for i in range(5):
        try:
            response = requests.post(
                auth_url,
                json={"phoneNumber": "2222222222"},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    success_count += 1
                    print(f"   Attempt {i+1}: ✅")
                else:
                    print(f"   Attempt {i+1}: ❌ No success field")
            else:
                print(f"   Attempt {i+1}: ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"   Attempt {i+1}: ❌ Exception: {e}")
    
    print(f"\n📊 Consistency Result: {success_count}/5 successful authentications")
    
    if success_count == 5:
        print("🎉 MCP Connection is FULLY OPERATIONAL!")
        return True
    elif success_count > 0:
        print("⚠️ MCP Connection is INTERMITTENT - needs investigation")
        return False
    else:
        print("❌ MCP Connection is FAILING")
        return False

if __name__ == "__main__":
    success = test_mcp_connection()
    exit(0 if success else 1) 