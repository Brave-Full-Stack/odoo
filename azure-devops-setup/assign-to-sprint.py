#!/usr/bin/env python3
"""
Assign all work items to 'General settings' sprint
"""

import requests
from base64 import b64encode

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

def get_all_work_items():
    """Get all work items in the project"""
    print("\n🔍 Finding all work items...")
    
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.1"
    
    query = {
        "query": "SELECT [System.Id], [System.Title], [System.WorkItemType] FROM WorkItems WHERE [System.TeamProject] = 'Odoo-Dev' AND [System.WorkItemType] IN ('Epic', 'User Story', 'Task') ORDER BY [System.Id]"
    }
    
    try:
        response = requests.post(url, headers=headers, json=query)
        response.raise_for_status()
        result = response.json()
        work_items = result.get('workItems', [])
        print(f"   Found {len(work_items)} work items")
        return [wi['id'] for wi in work_items]
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return []

def assign_to_sprint(work_item_ids: list, sprint_name: str):
    """Assign work items to sprint"""
    print(f"\n📌 Assigning work items to '{sprint_name}' sprint...")
    
    # Try different iteration path formats
    iteration_formats = [
        f"Odoo-Dev\\{sprint_name}",
        f"Odoo-Dev\\Iteration\\{sprint_name}",
        f"{PROJECT}\\{sprint_name}"
    ]
    
    success_count = 0
    failed_count = 0
    iteration_path = None
    
    for idx, wi_id in enumerate(work_item_ids, 1):
        url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{wi_id}?api-version=7.1"
        
        # If we haven't found the right format, try all
        if iteration_path is None:
            success = False
            for path_format in iteration_formats:
                operations = [{
                    "op": "add",
                    "path": "/fields/System.IterationPath",
                    "value": path_format
                }]
                
                try:
                    response = requests.patch(
                        url, 
                        headers={
                            'Authorization': f'Basic {auth_b64}', 
                            'Content-Type': 'application/json-patch+json'
                        }, 
                        json=operations
                    )
                    response.raise_for_status()
                    iteration_path = path_format
                    print(f"   ✓ Using iteration path: {iteration_path}")
                    success = True
                    success_count += 1
                    break
                except:
                    continue
            
            if not success:
                print(f"   ✗ WI {wi_id}: Could not find valid iteration path")
                failed_count += 1
        else:
            # Use the format that worked
            operations = [{
                "op": "add",
                "path": "/fields/System.IterationPath",
                "value": iteration_path
            }]
            
            try:
                response = requests.patch(
                    url, 
                    headers={
                        'Authorization': f'Basic {auth_b64}', 
                        'Content-Type': 'application/json-patch+json'
                    }, 
                    json=operations
                )
                response.raise_for_status()
                success_count += 1
                
                if idx % 20 == 0:
                    print(f"   Progress: {idx}/{len(work_item_ids)} items assigned")
            except requests.exceptions.RequestException as e:
                failed_count += 1
                if failed_count <= 3:
                    print(f"   ✗ WI {wi_id}: {str(e)[:100]}")
    
    print(f"\n   ✓ Successfully assigned: {success_count}")
    if failed_count > 0:
        print(f"   ✗ Failed: {failed_count}")
    
    return success_count

def main():
    print("=" * 60)
    print(f"Assign Work Items to '{SPRINT_NAME}' Sprint")
    print("=" * 60)
    
    # Get all work items
    work_item_ids = get_all_work_items()
    
    if not work_item_ids:
        print("\n❌ No work items found")
        return 1
    
    # Assign all work items to sprint
    assigned_count = assign_to_sprint(work_item_ids, SPRINT_NAME)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Assignment Complete!")
    print("=" * 60)
    print(f"Sprint: {SPRINT_NAME}")
    print(f"Work Items Assigned: {assigned_count}/{len(work_item_ids)}")
    print(f"\n📊 View Sprint:")
    print(f"   {ORG_URL}/{PROJECT}/_sprints/taskboard/{SPRINT_NAME.replace(' ', '%20')}")
    print(f"   {ORG_URL}/{PROJECT}/_backlogs/backlog")
    
    return 0 if assigned_count > 0 else 1

if __name__ == "__main__":
    exit(main())
