#!/usr/bin/env python3
"""
Configure Team Sprints in Azure DevOps
This script adds sprints to the team's iteration path so they appear in the Sprints view
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
import json

class TeamSprintConfigurator:
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
                # Get the first team (usually the default project team)
                team = teams['value'][0]
                print(f"✓ Found team: {team['name']} (ID: {team['id']})")
                return team['id'], team['name']
        
        print(f"❌ Failed to get teams: {response.status_code}")
        return None, None
    
    def get_all_iterations(self):
        """Get all iterations (sprints) in the project"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/work/teamsettings/iterations?api-version=7.0"
        
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            iterations = response.json()
            print(f"\n✓ Found {len(iterations.get('value', []))} iterations at project level")
            for iteration in iterations.get('value', []):
                print(f"  - {iteration['name']}")
            return iterations.get('value', [])
        else:
            print(f"❌ Failed to get iterations: {response.status_code}")
            return []
    
    def get_project_iterations(self):
        """Get all iterations from the project classification nodes"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/classificationnodes/iterations?$depth=2&api-version=7.0"
        
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            data = response.json()
            iterations = []
            
            # Check if there are child iterations
            if 'children' in data:
                for child in data['children']:
                    iterations.append({
                        'name': child['name'],
                        'path': child['path'],
                        'id': child['id'],
                        'url': child['url']
                    })
            
            print(f"\n📋 Project Iterations Found: {len(iterations)}")
            for it in iterations:
                print(f"  - {it['name']} (Path: {it['path']})")
            
            return iterations
        else:
            print(f"❌ Failed to get project iterations: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    
    def get_team_iterations(self, team_id):
        """Get iterations configured for the team"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.0"
        
        response = requests.get(url, auth=self.auth)
        
        if response.status_code == 200:
            iterations = response.json()
            print(f"\n📊 Team Iterations Currently Configured: {len(iterations.get('value', []))}")
            for iteration in iterations.get('value', []):
                print(f"  - {iteration['name']}")
            return iterations.get('value', [])
        else:
            print(f"❌ Failed to get team iterations: {response.status_code}")
            return []
    
    def add_iteration_to_team(self, team_id, iteration_path):
        """Add an iteration to the team's settings using iteration path"""
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.0"
        
        # Use the full iteration path
        payload = iteration_path
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, auth=self.auth, headers=headers, data=json.dumps(payload))
        
        if response.status_code not in [200, 201]:
            print(f"    Error details: {response.status_code} - {response.text}")
        
        return response.status_code in [200, 201]
    
    def configure_team_sprints(self):
        """Main function to configure team sprints"""
        print("🔧 Configuring Team Sprints...\n")
        
        # Get team ID
        team_id, team_name = self.get_team_id()
        if not team_id:
            return False
        
        # Get all project iterations
        project_iterations = self.get_project_iterations()
        if not project_iterations:
            print("\n❌ No sprints found at project level!")
            print("Run create_sprints.py first to create the sprints.")
            return False
        
        # Get team's current iterations
        team_iterations = self.get_team_iterations(team_id)
        team_iteration_ids = [it.get('id') for it in team_iterations]
        
        # Add missing iterations to team
        print(f"\n🔄 Adding sprints to team '{team_name}'...")
        added = 0
        
        for iteration in project_iterations:
            if iteration['id'] not in team_iteration_ids:
                # Pass the full iteration object
                success = self.add_iteration_to_team(team_id, iteration)
                if success:
                    print(f"  ✓ Added: {iteration['name']}")
                    added += 1
                else:
                    print(f"  ⚠️  Failed to add: {iteration['name']}")
            else:
                print(f"  ⏭️  Already configured: {iteration['name']}")
        
        print(f"\n✅ Configuration complete!")
        print(f"   - Added {added} new sprints to team")
        print(f"   - Total team sprints: {len(team_iterations) + added}")
        
        print(f"\n🌐 View sprints at:")
        print(f"   https://dev.azure.com/{self.organization}/{self.project}/_sprints")
        
        return True

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
    
    configurator = TeamSprintConfigurator(org, project, pat)
    
    try:
        success = configurator.configure_team_sprints()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
