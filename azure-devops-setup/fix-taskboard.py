#!/usr/bin/env python3
"""
Fix Sprint Taskboard Availability
Associates the sprint with the team's iteration settings
"""

import requests
from base64 import b64encode
from datetime import datetime, timedelta
import json
import os

# Configuration
ORG_URL = "https://dev.azure.com/Aries-Test"
PROJECT = "Odoo-Dev"
PAT = os.environ.get('AZURE_DEVOPS_PAT') or input('Enter your Azure DevOps PAT: ').strip()
SPRINT_NAME = "General settings"

# Create auth header
auth_string = f":{PAT}"
auth_b64 = b64encode(auth_string.encode('ascii')).decode('ascii')
headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def get_team_info():
    """Get team information"""
    print("\n🔍 Getting team information...")
    
    url = f"{ORG_URL}/_apis/projects/{PROJECT}/teams?api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        teams = response.json().get('value', [])
        
        if teams:
            team = teams[0]
            print(f"   ✓ Team: {team['name']}")
            print(f"   ✓ Team ID: {team['id']}")
            return team['id'], team['name']
        else:
            print("   ⚠ No teams found")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return None, None

def get_project_iterations():
    """Get all project iterations"""
    print("\n🔍 Checking project iterations...")
    
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?$depth=2&api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        iterations = response.json()
        
        print(f"   ✓ Found project iterations")
        
        # Find our sprint
        sprint_path = None
        if 'children' in iterations:
            for child in iterations['children']:
                if child.get('name') == SPRINT_NAME:
                    sprint_path = child.get('path')
                    print(f"   ✓ Found sprint: {sprint_path}")
                    return child
        
        print(f"   ⚠ Sprint '{SPRINT_NAME}' not found in project iterations")
        return None
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return None

def get_team_iterations(team_id):
    """Get team's iteration settings"""
    print(f"\n🔍 Checking team iteration settings...")
    
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        iterations = response.json().get('value', [])
        
        print(f"   ✓ Team has {len(iterations)} configured iterations")
        
        for iteration in iterations:
            iter_name = iteration.get('name', 'Unknown')
            iter_path = iteration.get('path', '')
            print(f"      • {iter_name}")
            if SPRINT_NAME in iter_name or SPRINT_NAME in iter_path:
                print(f"        ✓ Sprint is already configured for team")
                return True, iteration.get('id')
        
        print(f"   ⚠ Sprint '{SPRINT_NAME}' not configured for team")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return False, None

def add_sprint_to_team(team_id, sprint_id):
    """Add sprint to team's iterations"""
    print(f"\n📌 Adding sprint to team iterations...")
    
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.1"
    
    payload = {
        "id": sprint_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"   ✓ Sprint added to team successfully")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"   Details: {e.response.text[:300]}")
        return False

def set_current_iteration(team_id):
    """Set the sprint as current iteration for the team"""
    print(f"\n⚙️  Setting sprint as current iteration...")
    
    # Get team settings
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/teamsettings?api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        settings = response.json()
        
        # Update to set backlog iteration
        update_url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/teamsettings?api-version=7.1"
        
        update_data = {
            "backlogIteration": settings.get('backlogIteration'),
            "defaultIteration": settings.get('defaultIteration'),
            "defaultIterationMacro": "current"
        }
        
        patch_response = requests.patch(update_url, headers=headers, json=update_data)
        if patch_response.status_code in [200, 204]:
            print(f"   ✓ Team settings updated")
            return True
        else:
            print(f"   ⚠ Could not update team settings: {patch_response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ⚠ Settings update not critical: {str(e)[:100]}")
        return False

def verify_taskboard_access(team_id):
    """Verify taskboard is accessible"""
    print(f"\n✅ Verifying taskboard access...")
    
    # Check team iterations again
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        iterations = response.json().get('value', [])
        
        for iteration in iterations:
            if SPRINT_NAME in iteration.get('name', ''):
                print(f"   ✓ Sprint is configured and accessible")
                print(f"   ✓ Iteration ID: {iteration.get('id')}")
                return True
        
        print(f"   ⚠ Sprint still not visible in team iterations")
        return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print(f"Fix Taskboard Access for '{SPRINT_NAME}'")
    print("=" * 60)
    
    # Step 1: Get team
    team_id, team_name = get_team_info()
    if not team_id:
        print("\n❌ Could not get team information")
        return 1
    
    # Step 2: Check if sprint exists in project
    sprint_info = get_project_iterations()
    if not sprint_info:
        print("\n❌ Sprint not found in project iterations")
        print("\n💡 Creating sprint in project iterations...")
        
        # Create the sprint
        create_url = f"{ORG_URL}/{PROJECT}/_apis/wit/classificationnodes/iterations?api-version=7.1"
        
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(weeks=4)).strftime("%Y-%m-%d")
        
        sprint_data = {
            "name": SPRINT_NAME,
            "attributes": {
                "startDate": start_date,
                "finishDate": end_date
            }
        }
        
        try:
            response = requests.post(create_url, headers=headers, json=sprint_data)
            if response.status_code in [200, 201]:
                sprint_info = response.json()
                print(f"   ✓ Sprint created successfully")
            elif response.status_code == 409:
                print(f"   ⚠ Sprint already exists (409)")
                # Try to get it again
                sprint_info = get_project_iterations()
            else:
                print(f"   ✗ Could not create sprint: {response.status_code}")
                print(f"   Details: {response.text[:300]}")
        except Exception as e:
            print(f"   ✗ Error creating sprint: {e}")
    
    if not sprint_info:
        print("\n❌ Cannot proceed without sprint information")
        return 1
    
    sprint_id = sprint_info.get('identifier') or sprint_info.get('id')
    print(f"\n   Sprint ID: {sprint_id}")
    
    # Step 3: Check if sprint is in team's iterations
    is_configured, team_sprint_id = get_team_iterations(team_id)
    
    # Step 4: Add sprint to team if not configured
    if not is_configured:
        success = add_sprint_to_team(team_id, sprint_id)
        if not success:
            print("\n⚠ Could not add sprint to team automatically")
            print("\n📝 Manual Steps Required:")
            print("   1. Go to Project Settings → Team Configuration")
            print(f"   2. Select team: {team_name}")
            print("   3. Go to 'Iterations and Areas' tab")
            print(f"   4. Select iteration: {SPRINT_NAME}")
            print("   5. Save changes")
    
    # Step 5: Set as current iteration
    set_current_iteration(team_id)
    
    # Step 6: Verify
    is_accessible = verify_taskboard_access(team_id)
    
    # Summary
    print("\n" + "=" * 60)
    if is_accessible:
        print("✅ Taskboard Configuration Fixed!")
    else:
        print("⚠️  Taskboard May Need Manual Configuration")
    print("=" * 60)
    
    print(f"\n🎯 Access Your Taskboard Now:")
    print(f"\n   Sprint Taskboard:")
    print(f"   {ORG_URL}/{PROJECT}/{team_name.replace(' ', '%20')}/_sprints/taskboard/{SPRINT_NAME.replace(' ', '%20')}")
    
    print(f"\n   Alternative URL:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/taskboard")
    print(f"   (Then select '{SPRINT_NAME}' from the dropdown)")
    
    print(f"\n   Sprint Backlog:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/backlog/{SPRINT_NAME.replace(' ', '%20')}")
    
    if not is_accessible:
        print(f"\n📝 If taskboard still not visible:")
        print(f"   1. Go to Project Settings:")
        print(f"      {ORG_URL}/{PROJECT}/_settings/")
        print(f"   2. Click 'Teams' → Select '{team_name}'")
        print(f"   3. Click 'Iterations and Area Paths'")
        print(f"   4. Under 'Iterations', click 'Select iterations'")
        print(f"   5. Check the box next to '{SPRINT_NAME}'")
        print(f"   6. Click 'Save and close'")
        print(f"   7. Refresh the Sprints page")
    
    print(f"\n💡 Quick Check:")
    print(f"   • Verify sprint appears in dropdown on Sprints page")
    print(f"   • All 225 work items should be visible on taskboard")
    print(f"   • You should be able to drag items between columns")
    
    return 0

if __name__ == "__main__":
    exit(main())
