#!/usr/bin/env python3
"""
Activate Sprint 1 in Azure DevOps
Sets Sprint 1 as the current active sprint for the team
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime

class SprintActivator:
    def __init__(self, organization, project, pat):
        self.organization = organization
        self.project = project
        self.auth = HTTPBasicAuth('', pat)
        self.base_url = f"https://dev.azure.com/{organization}/{project}"
    
    def get_team_id(self):
        """Get the default team ID for the project"""
        url = f"https://dev.azure.com/{self.organization}/_apis/projects/{self.project}/teams?api-version=7.0"
        
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            teams = response.json()
            if teams.get('value'):
                team = teams['value'][0]
                return team['id'], team['name']
        return None, None
    
    def get_team_iterations(self, team_id):
        """Get all iterations configured for the team"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.0"
        
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            return response.json().get('value', [])
        return []
    
    def set_team_current_iteration(self, team_id, iteration_id):
        """Set the current iteration for the team"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{team_id}/_apis/work/teamsettings/iterations/{iteration_id}?api-version=7.0"
        
        # Get the iteration details first
        response = requests.get(url, auth=self.auth)
        if response.status_code != 200:
            return False
        
        iteration_data = response.json()
        
        # Update to set as current
        payload = {
            "id": iteration_id,
            "attributes": {
                "startDate": iteration_data['attributes']['startDate'],
                "finishDate": iteration_data['attributes']['finishDate'],
                "timeFrame": "current"
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.patch(url, auth=self.auth, headers=headers, json=payload)
        return response.status_code == 200
    
    def activate_sprint_1(self):
        """Activate Sprint 1"""
        print("🚀 Activating Sprint 1...\n")
        
        # Get team ID
        team_id, team_name = self.get_team_id()
        if not team_id:
            print("❌ Could not find team")
            return False
        
        print(f"✓ Found team: {team_name}")
        
        # Get team iterations
        iterations = self.get_team_iterations(team_id)
        if not iterations:
            print("❌ No iterations found for team")
            print("\n⚠️  You need to manually add Sprint 1 to team settings first!")
            print("   See: azure-devops-setup/scripts/manual_sprint_setup.py")
            return False
        
        print(f"✓ Found {len(iterations)} iterations\n")
        
        # Find Sprint 1
        sprint_1 = None
        for iteration in iterations:
            if 'Sprint 1' in iteration.get('name', ''):
                sprint_1 = iteration
                break
        
        if not sprint_1:
            print("❌ Sprint 1 not found in team iterations")
            print("\n⚠️  You need to manually add Sprint 1 to team settings first!")
            print("   See: azure-devops-setup/scripts/manual_sprint_setup.py")
            return False
        
        print(f"✓ Found Sprint 1: {sprint_1['name']}")
        print(f"  Start: {sprint_1['attributes'].get('startDate', 'N/A')}")
        print(f"  Finish: {sprint_1['attributes'].get('finishDate', 'N/A')}")
        
        # Check if already current
        if sprint_1['attributes'].get('timeFrame') == 'current':
            print(f"\n✅ Sprint 1 is already active!")
            return True
        
        # Activate it
        print(f"\n🔄 Setting Sprint 1 as current iteration...")
        
        if self.set_team_current_iteration(team_id, sprint_1['id']):
            print(f"✅ Sprint 1 activated successfully!")
            print(f"\n🌐 View at:")
            print(f"   https://dev.azure.com/{self.organization}/{self.project}/_sprints")
            return True
        else:
            print(f"❌ Failed to activate Sprint 1")
            print(f"\n💡 Manual activation:")
            print(f"   1. Go to Boards → Sprints")
            print(f"   2. Select Sprint 1")
            print(f"   3. Click 'Set sprint dates' or 'Start sprint'")
            return False

def main():
    # Get credentials from environment
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
    
    activator = SprintActivator(org, project, pat)
    
    try:
        success = activator.activate_sprint_1()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
