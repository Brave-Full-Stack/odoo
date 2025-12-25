#!/usr/bin/env python3
"""
Azure DevOps Connection Diagnostic Tool
Tests connection and provides detailed feedback
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

def test_connection():
    print("=" * 70)
    print("Azure DevOps Connection Diagnostic Tool")
    print("=" * 70)
    print()
    
    # Get credentials from environment or prompt
    org = os.environ.get('AZURE_DEVOPS_ORG')
    project = os.environ.get('AZURE_DEVOPS_PROJECT')
    pat = os.environ.get('AZURE_DEVOPS_PAT')
    
    if not org:
        org = input("Enter Azure DevOps Organization name: ").strip()
    if not project:
        project = input("Enter Project name: ").strip()
    if not pat:
        pat = input("Enter Personal Access Token (PAT): ").strip()
    
    print("\n📋 Configuration:")
    print(f"  Organization: {org}")
    print(f"  Project: {project}")
    print(f"  PAT Token: {pat[:10]}...{pat[-5:]} (length: {len(pat)})")
    print()
    
    # Test 1: Organization connection
    print("🔍 Test 1: Testing organization access...")
    org_url = f"https://dev.azure.com/{org}/_apis/projects?api-version=7.0"
    
    try:
        response = requests.get(org_url, auth=HTTPBasicAuth('', pat), timeout=10)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            projects = [p['name'] for p in data.get('value', [])]
            print(f"  ✅ Organization access successful!")
            print(f"  Found {len(projects)} project(s):")
            for p in projects:
                print(f"    - {p}")
        elif response.status_code == 401:
            print("  ❌ Authentication failed (401)")
            print("  Possible issues:")
            print("    1. PAT token is expired")
            print("    2. PAT token is invalid or copied incorrectly")
            print("    3. Organization name is incorrect")
            print("\n  💡 Solution:")
            print("    1. Go to: https://dev.azure.com/{org}")
            print("    2. Click profile icon → Personal Access Tokens")
            print("    3. Create new token with 'Work Items: Read, write, & manage' scope")
            print("    4. Copy the entire token (should be very long)")
            return False
        elif response.status_code == 404:
            print("  ❌ Organization not found (404)")
            print(f"  The organization '{org}' does not exist")
            print("\n  💡 Solution:")
            print("    1. Go to: https://dev.azure.com")
            print("    2. Check your organization name in the URL")
            print("    3. Update AZURE_DEVOPS_ORG in .azure_devops.env")
            return False
        else:
            print(f"  ❌ Unexpected error: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Connection error: {e}")
        return False
    
    print()
    
    # Test 2: Project access
    print("🔍 Test 2: Testing project access...")
    project_url = f"https://dev.azure.com/{org}/{project}/_apis/wit/workitemtypes?api-version=7.0"
    
    try:
        response = requests.get(project_url, auth=HTTPBasicAuth('', pat), timeout=10)
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ Project '{project}' access successful!")
            data = response.json()
            work_item_types = [wit['name'] for wit in data.get('value', [])]
            print(f"  Available work item types: {', '.join(work_item_types)}")
        elif response.status_code == 404:
            print(f"  ❌ Project '{project}' not found")
            print(f"\n  💡 Available projects in organization: {', '.join(projects)}")
            return False
        else:
            print(f"  ❌ Cannot access project: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Connection error: {e}")
        return False
    
    print()
    print("=" * 70)
    print("✅ All tests passed! You can now run: python3 import_to_azure_devops.py")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
