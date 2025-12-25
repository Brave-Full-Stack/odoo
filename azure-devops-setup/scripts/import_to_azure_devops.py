#!/usr/bin/env python3
"""
Azure DevOps Work Item Importer
Imports tasks from PROGRESS_TRACKER.csv into Azure DevOps as work items.
"""

import csv
import json
import sys
import os
from typing import Dict, List, Optional
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


class AzureDevOpsImporter:
    def __init__(self, organization: str, project: str, pat: str):
        """
        Initialize Azure DevOps connection.
        
        Args:
            organization: Your Azure DevOps organization name
            project: Your project name
            pat: Personal Access Token
        """
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.auth = HTTPBasicAuth('', pat)
        self.headers = {'Content-Type': 'application/json-patch+json'}
        self.task_map = {}  # Maps Task ID to Azure DevOps work item ID
        
    def test_connection(self) -> bool:
        """Test connection to Azure DevOps."""
        # Test at organization level, not project level
        url = f"https://dev.azure.com/{self.organization}/_apis/projects?api-version=7.0"
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                print(f"✓ Connected to Azure DevOps organization: {self.organization}")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def create_work_item(self, task_data: Dict) -> Optional[int]:
        """
        Create a work item in Azure DevOps.
        
        Args:
            task_data: Dictionary containing task information
            
        Returns:
            Work item ID if successful, None otherwise
        """
        url = f"{self.base_url}/wit/workitems/$Task?api-version=7.0"
        
        # Map priority to Azure DevOps values (1=High, 2=Medium, 3=Low, 4=Very Low)
        priority_map = {
            'Critical': 1,
            'High': 2,
            'Medium': 2,
            'Low': 3,
            '': 2  # Default to Medium
        }
        
        # Map status to Azure DevOps states (Agile process template)
        state_map = {
            'Not Started': 'New',
            'In Progress': 'Active',
            'Completed': 'Closed',
            'Blocked': 'New',
            '': 'New'
        }
        
        # Build description with all metadata
        description = f"""<div>
<h3>Phase {task_data['phase']}</h3>
<p><strong>Task ID:</strong> {task_data['task_id']}</p>
<p><strong>Duration:</strong> {task_data['duration']} days</p>
<p><strong>Priority:</strong> {task_data['priority']}</p>
"""
        
        if task_data.get('blockers'):
            description += f"<p><strong>Dependencies:</strong> {task_data['blockers']}</p>"
        
        if task_data.get('notes'):
            description += f"<p><strong>Notes:</strong> {task_data['notes']}</p>"
        
        description += "</div>"
        
        # Create work item payload
        operations = [
            {
                "op": "add",
                "path": "/fields/System.Title",
                "value": task_data['task_name']
            },
            {
                "op": "add",
                "path": "/fields/System.Description",
                "value": description
            },
            {
                "op": "add",
                "path": "/fields/System.State",
                "value": state_map.get(task_data['status'], 'To Do')
            },
            {
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Common.Priority",
                "value": priority_map.get(task_data['priority'], 2)
            },
            {
                "op": "add",
                "path": "/fields/System.Tags",
                "value": f"Phase-{task_data['phase']};Microservices;Odoo19"
            }
        ]
        
        # Add original estimate (duration in hours, assuming 8 hours/day)
        if task_data['duration']:
            try:
                hours = float(task_data['duration']) * 8
                operations.append({
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate",
                    "value": hours
                })
            except ValueError:
                pass
        
        # Add start date if exists
        if task_data.get('started_date'):
            operations.append({
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.StartDate",
                "value": task_data['started_date']
            })
        
        # Add completed date if exists
        if task_data.get('completed_date'):
            operations.append({
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Scheduling.FinishDate",
                "value": task_data['completed_date']
            })
        
        # Add completion percentage
        if task_data.get('progress'):
            try:
                progress = int(task_data['progress'])
                operations.append({
                    "op": "add",
                    "path": "/fields/Microsoft.VSTS.Scheduling.CompletedWork",
                    "value": progress
                })
            except ValueError:
                pass
        
        try:
            response = requests.post(url, auth=self.auth, headers=self.headers, json=operations)
            if response.status_code == 200:
                work_item = response.json()
                work_item_id = work_item['id']
                print(f"  ✓ Created: {task_data['task_id']} - {task_data['task_name'][:50]}... (ID: {work_item_id})")
                return work_item_id
            else:
                print(f"  ✗ Failed to create task {task_data['task_id']}: {response.status_code}")
                print(f"    Response: {response.text[:200]}")
                return None
        except Exception as e:
            print(f"  ✗ Error creating task {task_data['task_id']}: {e}")
            return None
    
    def create_dependency(self, source_id: int, target_id: int, link_type: str = "System.LinkTypes.Dependency-Forward"):
        """
        Create a dependency link between two work items.
        
        Args:
            source_id: Source work item ID
            target_id: Target work item ID (the one that depends on source)
            link_type: Type of link (default: Dependency)
        """
        url = f"{self.base_url}/wit/workitems/{target_id}?api-version=7.0"
        
        operations = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": link_type,
                    "url": f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workItems/{source_id}",
                    "attributes": {
                        "comment": "Dependency from CSV import"
                    }
                }
            }
        ]
        
        try:
            response = requests.patch(url, auth=self.auth, headers=self.headers, json=operations)
            if response.status_code == 200:
                return True
            else:
                print(f"    ⚠ Failed to create dependency {source_id} -> {target_id}: {response.status_code}")
                return False
        except Exception as e:
            print(f"    ⚠ Error creating dependency: {e}")
            return False
    
    def import_from_csv(self, csv_file: str):
        """
        Import all tasks from CSV file.
        
        Args:
            csv_file: Path to PROGRESS_TRACKER.csv
        """
        print(f"\n📥 Reading tasks from {csv_file}...")
        
        tasks = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tasks.append({
                    'phase': row['Phase'],
                    'task_id': row['Task ID'],
                    'task_name': row['Task Name'],
                    'duration': row['Duration (Days)'],
                    'priority': row['Priority'],
                    'status': row['Status'],
                    'progress': row['Progress %'],
                    'started_date': row['Started Date'],
                    'completed_date': row['Completed Date'],
                    'blockers': row['Blockers'],
                    'notes': row['Notes']
                })
        
        print(f"✓ Found {len(tasks)} tasks to import\n")
        
        # Phase 1: Create all work items
        print("🔨 Phase 1: Creating work items...")
        for task in tasks:
            work_item_id = self.create_work_item(task)
            if work_item_id:
                self.task_map[task['task_id']] = work_item_id
        
        print(f"\n✓ Created {len(self.task_map)} work items\n")
        
        # Phase 2: Create dependencies
        print("🔗 Phase 2: Creating dependencies...")
        dependency_count = 0
        for task in tasks:
            if task['blockers'] and task['task_id'] in self.task_map:
                target_id = self.task_map[task['task_id']]
                # Parse blockers (can be comma-separated)
                blocker_ids = [b.strip() for b in task['blockers'].split(',') if b.strip()]
                
                for blocker_id in blocker_ids:
                    if blocker_id in self.task_map:
                        source_id = self.task_map[blocker_id]
                        if self.create_dependency(source_id, target_id):
                            dependency_count += 1
                            print(f"  ✓ Linked: {blocker_id} → {task['task_id']}")
        
        print(f"\n✓ Created {dependency_count} dependencies\n")
        
        # Summary
        print("=" * 70)
        print("📊 IMPORT SUMMARY")
        print("=" * 70)
        print(f"Total tasks in CSV:       {len(tasks)}")
        print(f"Work items created:       {len(self.task_map)}")
        print(f"Dependencies created:     {dependency_count}")
        print(f"Success rate:             {len(self.task_map)/len(tasks)*100:.1f}%")
        print("=" * 70)
        print(f"\n✅ Import complete! View at: https://dev.azure.com/{self.organization}/{self.project}/_workitems")


def main():
    print("=" * 70)
    print("Azure DevOps Work Item Importer - Odoo Microservices")
    print("=" * 70)
    
    # Get configuration
    organization = os.getenv('AZURE_DEVOPS_ORG') or input("Enter Azure DevOps Organization: ")
    project = os.getenv('AZURE_DEVOPS_PROJECT') or input("Enter Project Name: ")
    pat = os.getenv('AZURE_DEVOPS_PAT') or input("Enter Personal Access Token: ")
    
    if not all([organization, project, pat]):
        print("✗ Missing required configuration")
        sys.exit(1)
    
    csv_file = 'PROGRESS_TRACKER.csv'
    if not os.path.exists(csv_file):
        print(f"✗ File not found: {csv_file}")
        sys.exit(1)
    
    # Initialize importer
    importer = AzureDevOpsImporter(organization, project, pat)
    
    # Test connection
    print("\n🔌 Testing connection...")
    if not importer.test_connection():
        print("\n✗ Cannot connect to Azure DevOps. Please check your credentials.")
        sys.exit(1)
    
    # Confirm import
    print(f"\n⚠️  This will import 297 tasks into project '{project}'")
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Import cancelled.")
        sys.exit(0)
    
    # Import tasks
    importer.import_from_csv(csv_file)


if __name__ == "__main__":
    main()
