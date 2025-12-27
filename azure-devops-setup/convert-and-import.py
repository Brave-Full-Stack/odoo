#!/usr/bin/env python3
"""
Convert Progress_tracker.csv to Azure DevOps format and import
This script:
1. Reads Progress_tracker.csv
2. Converts to Azure DevOps work item structure
3. Creates work items via REST API without Area/Iteration paths (assigned later)
"""

import csv
import requests
import time
from base64 import b64encode
from typing import Dict, Optional, List

# Configuration
ORG_URL = "https://dev.azure.com/Aries-Test"
PROJECT = "Odoo-Dev"
API_VERSION = "7.1-preview.3"

def get_pat_token():
    """Get PAT token from user input"""
    print("=" * 60)
    print("Azure DevOps Authentication")
    print("=" * 60)
    print()
    print("To authenticate, you need a Personal Access Token (PAT).")
    print()
    print("How to get PAT:")
    print("1. Go to: https://dev.azure.com/Aries-Test/_usersSettings/tokens")
    print("2. Click: + New Token")
    print("3. Name: Odoo-Dev Import")
    print("4. Scopes: Work Items (Read, write, & manage)")
    print("5. Copy the token")
    print()
    
    pat = input("Enter your PAT token: ").strip()
    return pat

class AzureDevOpsClient:
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.base_url = f"{organization}/{project}/_apis/wit"
        
        # Create authentication header
        auth_string = f":{pat}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json-patch+json',
            'Accept': 'application/json'
        }
        
        self.work_item_map = {}  # Title -> ID mapping
    
    def create_work_item(self, work_type: str, title: str, description: str = "", priority: int = 2, tags: str = "", story_points: float = None, estimate: float = None) -> Optional[int]:
        """Create a work item using REST API"""
        url = f"{self.base_url}/workitems/${work_type}?api-version={API_VERSION}"
        
        # Build JSON patch document with essential fields
        operations = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
        ]
        
        if description:
            operations.append({"op": "add", "path": "/fields/System.Description", "value": description})
        
        if priority:
            operations.append({"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": int(priority)})
        
        if tags:
            operations.append({"op": "add", "path": "/fields/System.Tags", "value": tags})
        
        if story_points and work_type == "User Story":
            operations.append({"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": float(story_points)})
        
        if estimate and work_type == "Task":
            operations.append({"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate", "value": float(estimate)})
        
        try:
            response = requests.post(url, headers=self.headers, json=operations)
            response.raise_for_status()
            
            result = response.json()
            work_item_id = result.get('id')
            self.work_item_map[title] = work_item_id
            return work_item_id
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                error_data = e.response.text[:300]
                print(f"  Details: {error_data}")
            return None
    
    def add_parent_link(self, child_id: int, parent_id: int):
        """Add a parent link to a work item"""
        url = f"{self.base_url}/workitems/{child_id}?api-version={API_VERSION}"
        
        operations = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{self.organization}/_apis/wit/workItems/{parent_id}"
            }
        }]
        
        try:
            response = requests.patch(url, headers=self.headers, json=operations)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

def parse_progress_tracker(csv_file: str) -> Dict[str, List[Dict]]:
    """Parse Progress_tracker.csv and convert to Azure DevOps structure"""
    print("\n" + "=" * 60)
    print("Parsing Progress_tracker.csv...")
    print("=" * 60)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Found {len(rows)} rows in Progress_tracker.csv")
    
    # Convert priority mapping
    priority_map = {
        'Critical': 1,
        'High': 2,
        'Medium': 3,
        'Low': 4
    }
    
    # Parse rows into work items
    epics = []
    user_stories = []
    tasks = []
    
    current_epic = None
    current_user_story = None
    
    for row in rows:
        phase = row['Phase']
        task_name = row['Task Name']
        duration = float(row['Duration (Days)']) if row['Duration (Days)'] else 0
        priority = priority_map.get(row['Priority'], 3)
        notes = row['Notes']
        
        # Convert duration to hours (assuming 8-hour workday)
        hours = duration * 8
        
        # Extract tags from phase
        tags = []
        if ':' in phase:
            tag = phase.split(':')[1].strip().lower().replace(' & ', ';').replace(' ', '-')
            tags.append(tag)
        
        if phase.startswith('EPIC:'):
            # This is an Epic
            current_epic = {
                'type': 'Epic',
                'title': task_name,
                'description': notes,
                'priority': priority,
                'tags': ';'.join(tags) if tags else 'general-settings'
            }
            epics.append(current_epic)
        
        elif phase.startswith('USER STORY:'):
            # This is a User Story
            story_points = round(duration, 1) if duration > 0 else 2
            current_user_story = {
                'type': 'User Story',
                'title': task_name,
                'description': notes,
                'priority': priority,
                'story_points': story_points,
                'tags': ';'.join(tags) if tags else '',
                'parent': current_epic['title'] if current_epic else None
            }
            user_stories.append(current_user_story)
        
        elif phase.startswith('  → Task'):
            # This is a Task
            task = {
                'type': 'Task',
                'title': task_name,
                'description': notes,
                'priority': priority,
                'estimate': hours,
                'tags': ';'.join(tags) if tags else '',
                'parent': current_user_story['title'] if current_user_story else None
            }
            tasks.append(task)
    
    print(f"\n📊 Parsed Structure:")
    print(f"  - Epics: {len(epics)}")
    print(f"  - User Stories: {len(user_stories)}")
    print(f"  - Tasks: {len(tasks)}")
    
    return {
        'epics': epics,
        'user_stories': user_stories,
        'tasks': tasks
    }

def import_work_items(client: AzureDevOpsClient, work_items: Dict[str, List[Dict]]):
    """Import work items to Azure DevOps"""
    
    epics = work_items['epics']
    user_stories = work_items['user_stories']
    tasks = work_items['tasks']
    
    created_count = 0
    failed_count = 0
    
    # Step 1: Create Epics
    print("\n" + "=" * 60)
    print(f"[1/3] Creating Epics ({len(epics)} items)")
    print("=" * 60)
    
    for epic in epics:
        print(f"Creating: {epic['title']}... ", end="", flush=True)
        
        work_item_id = client.create_work_item(
            work_type="Epic",
            title=epic['title'],
            description=epic['description'],
            priority=epic['priority'],
            tags=epic['tags']
        )
        
        if work_item_id:
            print(f"✓ ID: {work_item_id}")
            created_count += 1
        else:
            print("✗ Failed")
            failed_count += 1
        
        time.sleep(0.5)
    
    # Step 2: Create User Stories
    print("\n" + "=" * 60)
    print(f"[2/3] Creating User Stories ({len(user_stories)} items)")
    print("=" * 60)
    
    for idx, story in enumerate(user_stories, 1):
        print(f"[{idx}/{len(user_stories)}] {story['title'][:50]}... ", end="", flush=True)
        
        work_item_id = client.create_work_item(
            work_type="User Story",
            title=story['title'],
            description=story['description'],
            priority=story['priority'],
            tags=story['tags'],
            story_points=story['story_points']
        )
        
        if work_item_id:
            print(f"✓ {work_item_id}", end="")
            created_count += 1
            
            # Link to parent Epic
            if story['parent'] and story['parent'] in client.work_item_map:
                parent_id = client.work_item_map[story['parent']]
                if client.add_parent_link(work_item_id, parent_id):
                    print(" → Linked")
                else:
                    print(" → ⚠")
            else:
                print()
        else:
            print("✗")
            failed_count += 1
        
        if (idx % 10) == 0:
            print(f"\n  Progress: {idx}/{len(user_stories)} user stories\n")
            time.sleep(0.5)
        else:
            time.sleep(0.3)
    
    # Step 3: Create Tasks
    print("\n" + "=" * 60)
    print(f"[3/3] Creating Tasks ({len(tasks)} items)")
    print("=" * 60)
    
    for idx, task in enumerate(tasks, 1):
        title_display = task['title'][:45] + "..." if len(task['title']) > 45 else task['title']
        print(f"[{idx}/{len(tasks)}] {title_display} ", end="", flush=True)
        
        work_item_id = client.create_work_item(
            work_type="Task",
            title=task['title'],
            description=task['description'],
            priority=task['priority'],
            tags=task['tags'],
            estimate=task['estimate']
        )
        
        if work_item_id:
            print(f"✓ {work_item_id}", end="")
            created_count += 1
            
            # Link to parent User Story
            if task['parent'] and task['parent'] in client.work_item_map:
                parent_id = client.work_item_map[task['parent']]
                if client.add_parent_link(work_item_id, parent_id):
                    print(" ✓")
                else:
                    print(" ⚠")
            else:
                print()
        else:
            print("✗")
            failed_count += 1
        
        if (idx % 20) == 0:
            print(f"\n  Progress: {idx}/{len(tasks)} tasks\n")
            time.sleep(0.5)
        else:
            time.sleep(0.2)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Import Complete!")
    print("=" * 60)
    print(f"✓ Successfully created: {created_count} work items")
    print(f"✗ Failed: {failed_count} work items")
    print(f"\nView in Azure DevOps:")
    print(f"  {ORG_URL}/{PROJECT}/_workitems")
    print(f"  {ORG_URL}/{PROJECT}/_backlogs/backlog")
    
    return created_count, failed_count

def main():
    print("\n" + "=" * 60)
    print("Progress Tracker → Azure DevOps Importer")
    print("=" * 60)
    
    # Get PAT token
    pat = get_pat_token()
    if not pat:
        print("❌ PAT token is required!")
        return 1
    
    # Parse Progress_tracker.csv
    csv_file = "../Progress_tracker.csv"
    try:
        work_items = parse_progress_tracker(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: {csv_file} not found!")
        print("Make sure Progress_tracker.csv exists in the parent directory")
        return 1
    
    # Create Azure DevOps client
    client = AzureDevOpsClient(ORG_URL, PROJECT, pat)
    
    # Import work items
    created, failed = import_work_items(client, work_items)
    
    print("\n📝 Next Steps:")
    print("1. Go to Azure DevOps and verify work items")
    print("2. Assign Area Paths manually (Project Settings → Areas)")
    print("3. Assign Iteration Paths/Sprints manually (Backlogs → Drag to sprints)")
    print("4. Create dashboards and set team capacity")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit(main())
