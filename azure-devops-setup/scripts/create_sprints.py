#!/usr/bin/env python3
"""
Create and configure sprints in Azure DevOps for the Odoo Microservices project.
Organizes work items into 6 sprints based on project phases.
"""

import os
import sys
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class SprintManager:
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.auth = HTTPBasicAuth('', pat)
        self.api_version = "7.0"
        self.team_name = "Odoo-Microservices Team"
    
    def test_connection(self) -> bool:
        """Test connection to Azure DevOps."""
        url = f"https://dev.azure.com/{self.organization}/_apis/projects?api-version={self.api_version}"
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                print(f"✓ Connected to Azure DevOps organization: {self.organization}")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def get_team_context(self) -> Optional[str]:
        """Get the team ID for sprint creation."""
        url = f"https://dev.azure.com/{self.organization}/_apis/projects/{self.project}/teams?api-version={self.api_version}"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            
            teams = response.json().get('value', [])
            for team in teams:
                if team['name'] == self.team_name or team['name'] == self.project:
                    print(f"✓ Found team: {team['name']} (ID: {team['id']})")
                    return team['id']
            
            # If team not found, use the first team
            if teams:
                print(f"✓ Using default team: {teams[0]['name']}")
                return teams[0]['id']
            
            print("✗ No teams found")
            return None
        except Exception as e:
            print(f"✗ Error getting team context: {e}")
            return None
    
    def get_classification_node(self, team_id: str) -> Optional[str]:
        """Get the classification node for iterations."""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{team_id}/_apis/work/teamsettings?api-version={self.api_version}"
        try:
            response = requests.get(url, auth=self.auth)
            response.raise_for_status()
            
            settings = response.json()
            backlog_iteration = settings.get('backlogIteration', {})
            path = backlog_iteration.get('path', '')
            print(f"✓ Classification path: {path}")
            return path
        except Exception as e:
            print(f"✗ Error getting classification node: {e}")
            return None
    
    def create_iteration(self, name: str, start_date: str, finish_date: str) -> Optional[str]:
        """Create an iteration (sprint) in Azure DevOps."""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/classificationnodes/iterations?api-version={self.api_version}"
        
        payload = {
            "name": name,
            "attributes": {
                "startDate": start_date,
                "finishDate": finish_date
            }
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                auth=self.auth,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                iteration = response.json()
                print(f"  ✓ Created: {name} ({start_date} to {finish_date})")
                return iteration.get('path', '')
            else:
                # Sprint might already exist
                print(f"  ⚠️  Sprint '{name}' might already exist (Status: {response.status_code})")
                return f"{self.project}\\{name}"
        except Exception as e:
            print(f"  ✗ Error creating iteration: {e}")
            return None
    
    def get_sprint_definitions(self) -> List[Dict]:
        """Return sprint definitions with dates and phase assignments."""
        start_date = datetime.now()
        
        return [
            {
                "name": "Sprint 1",
                "start": start_date,
                "duration": 10,  # days
                "phases": ["Phase-0", "Phase-1"],
                "description": "Foundation: Microservices Design & Service Mesh Setup"
            },
            {
                "name": "Sprint 2",
                "start": start_date + timedelta(days=10),
                "duration": 10,
                "phases": ["Phase-2", "Phase-3"],
                "description": "Core Development: Services & Event Bus"
            },
            {
                "name": "Sprint 3",
                "start": start_date + timedelta(days=20),
                "duration": 10,
                "phases": ["Phase-4", "Phase-5"],
                "description": "Infrastructure: Observability & API Gateway"
            },
            {
                "name": "Sprint 4",
                "start": start_date + timedelta(days=30),
                "duration": 5,
                "phases": ["Phase-6", "Phase-7"],
                "description": "DevOps: Registry & GitOps"
            },
            {
                "name": "Sprint 5",
                "start": start_date + timedelta(days=35),
                "duration": 5,
                "phases": ["Phase-8"],
                "description": "Automation: CI/CD Pipeline"
            },
            {
                "name": "Sprint 6",
                "start": start_date + timedelta(days=40),
                "duration": 5,
                "phases": ["Phase-9", "Testing", "Validation", "Additional"],
                "description": "Cloud & Testing: AWS Deployment & Validation"
            }
        ]
    
    def create_all_sprints(self) -> Dict[str, str]:
        """Create all sprints and return mapping of sprint names to paths."""
        print("\n🏃 Creating sprints...")
        
        sprint_paths = {}
        sprints = self.get_sprint_definitions()
        
        for sprint in sprints:
            start = sprint['start'].strftime('%Y-%m-%d')
            end = (sprint['start'] + timedelta(days=sprint['duration'])).strftime('%Y-%m-%d')
            
            path = self.create_iteration(sprint['name'], start, end)
            if path:
                sprint_paths[sprint['name']] = path
            
            time.sleep(0.5)  # Rate limiting
        
        print(f"\n✓ Created {len(sprint_paths)} sprints")
        return sprint_paths
    
    def get_phase_to_sprint_mapping(self) -> Dict[str, str]:
        """Map phases to sprint names."""
        return {
            "Phase-0": "Sprint 1",
            "Phase-1": "Sprint 1",
            "Phase-2": "Sprint 2",
            "Phase-3": "Sprint 2",
            "Phase-4": "Sprint 3",
            "Phase-5": "Sprint 3",
            "Phase-6": "Sprint 4",
            "Phase-7": "Sprint 4",
            "Phase-8": "Sprint 5",
            "Phase-9": "Sprint 6",
            "Testing": "Sprint 6",
            "Validation": "Sprint 6",
            "Additional": "Sprint 6"
        }
    
    def get_work_items_by_phase(self, phase: str) -> List[int]:
        """Get all work items (Epics and User Stories) for a phase."""
        url = f"{self.base_url}/wit/wiql?api-version={self.api_version}"
        
        query = {
            "query": f"""
                SELECT [System.Id]
                FROM WorkItems
                WHERE [System.WorkItemType] IN ('Epic', 'User Story')
                AND [System.Tags] CONTAINS '{phase}'
                AND [System.TeamProject] = @project
            """
        }
        
        try:
            response = requests.post(url, json=query, auth=self.auth)
            response.raise_for_status()
            
            work_items = response.json().get('workItems', [])
            return [item['id'] for item in work_items]
        except Exception as e:
            print(f"✗ Error getting work items for {phase}: {e}")
            return []
    
    def assign_work_item_to_sprint(self, work_item_id: int, iteration_path: str) -> bool:
        """Assign a work item to a sprint."""
        url = f"{self.base_url}/wit/workitems/{work_item_id}?api-version={self.api_version}"
        
        operations = [
            {
                "op": "add",
                "path": "/fields/System.IterationPath",
                "value": iteration_path
            }
        ]
        
        try:
            response = requests.patch(
                url,
                json=operations,
                auth=self.auth,
                headers={"Content-Type": "application/json-patch+json"}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            return False
    
    def assign_work_items_to_sprints(self, sprint_paths: Dict[str, str]):
        """Assign all work items to their respective sprints."""
        print("\n📋 Assigning work items to sprints...")
        
        phase_to_sprint = self.get_phase_to_sprint_mapping()
        total_assigned = 0
        
        # Map Epic IDs to sprint names for easier assignment
        epic_to_sprint = {
            299: "Sprint 1",  # Phase-0
            300: "Sprint 1",  # Phase-1
            301: "Sprint 2",  # Phase-2
            302: "Sprint 2",  # Phase-3
            303: "Sprint 3",  # Phase-4
            304: "Sprint 3",  # Phase-5
            305: "Sprint 4",  # Phase-6
            306: "Sprint 4",  # Phase-7
            307: "Sprint 5",  # Phase-8
            308: "Sprint 6",  # Phase-9
        }
        
        # Assign Epics first
        print("\n  📋 Assigning Epics to sprints...")
        for epic_id, sprint_name in epic_to_sprint.items():
            if sprint_name in sprint_paths:
                if self.assign_work_item_to_sprint(epic_id, sprint_paths[sprint_name]):
                    total_assigned += 1
                    print(f"    ✓ Epic #{epic_id} → {sprint_name}")
                time.sleep(0.1)
        
        # Assign User Stories based on their story ID prefix
        print("\n  📖 Assigning User Stories to sprints...")
        story_ranges = {
            "Sprint 1": range(309, 321),  # Stories 0.1-1.6
            "Sprint 2": range(321, 331),  # Stories 2.1-3.5
            "Sprint 3": range(331, 342),  # Stories 4.1-5.6
            "Sprint 4": range(342, 351),  # Stories 6.1-7.5
            "Sprint 5": range(351, 357),  # Stories 8.1-8.6
            "Sprint 6": range(357, 379),  # Stories 9.1-A.6
        }
        
        for sprint_name, story_ids in story_ranges.items():
            if sprint_name not in sprint_paths:
                continue
            
            assigned = 0
            for story_id in story_ids:
                if self.assign_work_item_to_sprint(story_id, sprint_paths[sprint_name]):
                    assigned += 1
                time.sleep(0.1)
            
            print(f"    ✓ {sprint_name}: {assigned} stories")
            total_assigned += assigned
        
        print(f"\n✓ Assigned {total_assigned} work items to sprints")
    
    def print_sprint_summary(self):
        """Print a summary of all sprints and their contents."""
        print("\n" + "="*70)
        print("📊 SPRINT SUMMARY")
        print("="*70)
        
        sprints = self.get_sprint_definitions()
        
        for i, sprint in enumerate(sprints, 1):
            start = sprint['start'].strftime('%Y-%m-%d')
            end = (sprint['start'] + timedelta(days=sprint['duration'])).strftime('%Y-%m-%d')
            
            print(f"\n{sprint['name']} ({sprint['duration']} days)")
            print(f"  📅 Dates: {start} to {end}")
            print(f"  📝 Description: {sprint['description']}")
            print(f"  🏷️  Phases: {', '.join(sprint['phases'])}")
        
        print("\n" + "="*70)


def main():
    print("="*70)
    print("🏃 Azure DevOps Sprint Creator")
    print("="*70)
    
    # Load environment variables
    org = os.getenv('AZURE_DEVOPS_ORG')
    project = os.getenv('AZURE_DEVOPS_PROJECT')
    pat = os.getenv('AZURE_DEVOPS_PAT')
    
    if not all([org, project, pat]):
        print("\n❌ Missing required environment variables:")
        print("  - AZURE_DEVOPS_ORG")
        print("  - AZURE_DEVOPS_PROJECT")
        print("  - AZURE_DEVOPS_PAT")
        print("\nMake sure to source .env file:")
        print("  source azure-devops-setup/.env")
        sys.exit(1)
    
    manager = SprintManager(org, project, pat)
    
    # Test connection
    if not manager.test_connection():
        print("❌ Failed to connect to Azure DevOps")
        sys.exit(1)
    
    # Create sprints
    sprint_paths = manager.create_all_sprints()
    
    if not sprint_paths:
        print("❌ No sprints were created")
        sys.exit(1)
    
    # Assign work items to sprints
    manager.assign_work_items_to_sprints(sprint_paths)
    
    # Print summary
    manager.print_sprint_summary()
    
    print("\n" + "="*70)
    print("✅ Sprint setup complete!")
    print("="*70)
    print("\n🔗 Next steps:")
    print("  1. View sprints in Azure DevOps")
    print("  2. Run: python3 scripts/generate_dashboard.py")
    print("  3. Start sprint planning!")
    print()


if __name__ == "__main__":
    main()
