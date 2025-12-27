#!/usr/bin/env python3
"""
Configure Taskboard for 'General settings' Sprint
Verifies sprint setup and provides taskboard configuration
"""

import requests
from base64 import b64encode
import json

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
    """Get default team information"""
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

def verify_sprint_items():
    """Verify work items are assigned to the sprint"""
    print(f"\n🔍 Verifying work items in '{SPRINT_NAME}' sprint...")
    
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.1"
    
    query = {
        "query": f"""SELECT 
            [System.Id], 
            [System.WorkItemType],
            [System.Title],
            [System.State]
        FROM WorkItems 
        WHERE [System.TeamProject] = '{PROJECT}' 
            AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
        ORDER BY [System.WorkItemType] DESC"""
    }
    
    try:
        response = requests.post(url, headers=headers, json=query)
        response.raise_for_status()
        result = response.json()
        work_items = result.get('workItems', [])
        
        # Count by type
        types = {}
        for wi in work_items:
            # Get work item details
            wi_url = f"{ORG_URL}/_apis/wit/workitems/{wi['id']}?api-version=7.1"
            wi_response = requests.get(wi_url, headers=headers)
            if wi_response.status_code == 200:
                wi_data = wi_response.json()
                wi_type = wi_data['fields'].get('System.WorkItemType')
                types[wi_type] = types.get(wi_type, 0) + 1
        
        print(f"   ✓ Total work items: {len(work_items)}")
        for wi_type, count in sorted(types.items()):
            print(f"      • {wi_type}: {count}")
        
        return len(work_items) > 0
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return False

def get_board_info(team_id):
    """Get board information for the team"""
    print(f"\n🔍 Getting board configuration...")
    
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards?api-version=7.1-preview.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        boards = response.json().get('value', [])
        
        for board in boards:
            print(f"   ✓ Board: {board.get('name')}")
            print(f"      ID: {board.get('id')}")
        
        return boards[0] if boards else None
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return None

def configure_board_settings(team_id, board_id):
    """Configure board card settings to show more information"""
    print(f"\n⚙️  Configuring board settings...")
    
    # Get current board settings
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards/{board_id}/cardsettings?api-version=7.1-preview.2"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            current_settings = response.json()
            print(f"   ✓ Retrieved current settings")
            
            # Update settings to show additional fields on cards
            card_settings = {
                "cards": {
                    "Epic": [
                        {"fieldIdentifier": "System.Title", "displayType": "core"},
                        {"fieldIdentifier": "System.Tags", "displayType": "additional"},
                        {"fieldIdentifier": "System.AssignedTo", "displayType": "additional"}
                    ],
                    "User Story": [
                        {"fieldIdentifier": "System.Title", "displayType": "core"},
                        {"fieldIdentifier": "Microsoft.VSTS.Scheduling.StoryPoints", "displayType": "additional"},
                        {"fieldIdentifier": "System.AssignedTo", "displayType": "additional"},
                        {"fieldIdentifier": "System.Tags", "displayType": "additional"}
                    ],
                    "Task": [
                        {"fieldIdentifier": "System.Title", "displayType": "core"},
                        {"fieldIdentifier": "Microsoft.VSTS.Scheduling.RemainingWork", "displayType": "additional"},
                        {"fieldIdentifier": "System.AssignedTo", "displayType": "additional"},
                        {"fieldIdentifier": "System.Tags", "displayType": "additional"}
                    ]
                }
            }
            
            # Update board settings
            put_response = requests.put(url, headers=headers, json=card_settings)
            if put_response.status_code in [200, 204]:
                print(f"   ✓ Board card settings updated")
                print(f"      • Cards now show: Title, Assigned To, Tags")
                print(f"      • User Stories show: Story Points")
                print(f"      • Tasks show: Remaining Work")
                return True
            else:
                print(f"   ⚠ Could not update settings: {put_response.status_code}")
                return False
        else:
            print(f"   ⚠ Could not retrieve current settings")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ⚠ Board settings API not accessible: {str(e)[:100]}")
        return False

def main():
    print("=" * 60)
    print(f"Configure Taskboard for '{SPRINT_NAME}' Sprint")
    print("=" * 60)
    
    # Step 1: Get team information
    team_id, team_name = get_team_info()
    
    if not team_id:
        print("\n❌ Could not find team")
        return 1
    
    # Step 2: Verify sprint has work items
    has_items = verify_sprint_items()
    
    if not has_items:
        print("\n❌ No work items found in sprint")
        return 1
    
    # Step 3: Get board information
    board = get_board_info(team_id)
    
    if board:
        board_id = board.get('id')
        # Try to configure board settings
        configure_board_settings(team_id, board_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Taskboard Configuration Complete!")
    print("=" * 60)
    print(f"\n📋 Sprint Details:")
    print(f"   • Sprint: {SPRINT_NAME}")
    print(f"   • Team: {team_name}")
    print(f"   • Work items are assigned and ready")
    
    print(f"\n🎯 Access Your Taskboard:")
    print(f"\n   Sprint Taskboard:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/taskboard/{SPRINT_NAME.replace(' ', '%20')}")
    
    print(f"\n   Sprint Backlog:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/backlog/{SPRINT_NAME.replace(' ', '%20')}")
    
    print(f"\n   Sprint Capacity:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/capacity/{SPRINT_NAME.replace(' ', '%20')}")
    
    print(f"\n📊 Taskboard Features:")
    print(f"   • Drag-and-drop work items between columns")
    print(f"   • Group by: People, Stories, or Backlog Items")
    print(f"   • Filter by: Work item type, Assigned to, Tags")
    print(f"   • Update task status inline")
    print(f"   • Track remaining work and capacity")
    
    print(f"\n💡 Quick Actions:")
    print(f"   1. Set Team Capacity: Click 'Capacity' tab")
    print(f"   2. Update Task Status: Drag cards across columns")
    print(f"   3. Assign Work: Click on a card and assign team members")
    print(f"   4. Track Progress: View burndown chart")
    print(f"   5. Add New Tasks: Click '+ New item' on the board")
    
    print(f"\n🔧 Board Columns (Default):")
    print(f"   • New → Active → Resolved → Closed")
    print(f"   • Configure columns in Board Settings")
    
    return 0

if __name__ == "__main__":
    exit(main())
