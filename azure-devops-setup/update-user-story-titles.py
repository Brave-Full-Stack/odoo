#!/usr/bin/env python3
"""
Update User Story titles to include category prefix
Format: [Category] - [Original Title]
"""

import requests
from base64 import b64encode
import time

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
    'Accept': 'application/json'
}

headers_wiql = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

headers_patch = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json-patch+json',
    'Accept': 'application/json'
}

# Category mapping based on User Story groups
CATEGORY_MAPPING = {
    # Apps & Modules stories
    "Install and Configure Applications": "Apps & Modules",
    "Upgrade Applications": "Apps & Modules",
    "Uninstall Applications": "Apps & Modules",
    
    # Users stories
    "User Management": "Users",
    "Language Configuration": "Users",
    "Two-Factor Authentication": "Users",
    "Access Rights Management": "Users",
    "Portal Access": "Users",
    "Device Management": "Users",
    "User Lifecycle": "Users",
    "Password Management": "Users",
    "Multi-Company Setup": "Users",
    
    # Authentication stories
    "Facebook OAuth": "Authentication",
    "Google OAuth": "Authentication",
    "Azure AD OAuth": "Authentication",
    "LDAP Authentication": "Authentication",
    
    # Companies stories
    "Company Configuration": "Companies",
    "Branch Management": "Companies",
    "Multi-Company Operations": "Companies",
    
    # Email stories
    "Digest Emails": "Email Communication",
    "Email Templates": "Email Communication",
    "Email Server Configuration": "Email Communication",
    "DNS Configuration": "Email Communication",
    "Outlook Integration": "Email Communication",
    "Gmail Integration": "Email Communication",
    "Mailjet Integration": "Email Communication",
    "Email Troubleshooting": "Email Communication",
    "Mail Plugin Integration": "Email Communication",
    
    # IoT stories
    "IoT Box Setup": "IoT",
    "Odoo IoT Integration": "IoT",
    "Printer Integration": "IoT",
    "Scale Integration": "IoT",
    "Display Integration": "IoT",
    "Measurement Tools": "IoT",
    "Camera Integration": "IoT",
    "Footswitch Integration": "IoT",
    
    # Integrations stories
    "Unsplash Integration": "Integrations",
    "Geolocation Integration": "Integrations",
    "Google Translate Integration": "Integrations",
    "Google Cloud Storage": "Integrations",
    "Azure Storage": "Integrations",
    
    # Developer Tools stories
    "Developer Tools": "Developer Mode"
}

def get_all_user_stories():
    """Get all User Stories from the sprint"""
    print("\n🔍 Finding all User Stories...")
    
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/wiql?api-version=7.1"
    
    query = {
        "query": f"""SELECT 
            [System.Id],
            [System.Title],
            [System.Tags]
        FROM WorkItems 
        WHERE [System.TeamProject] = '{PROJECT}' 
            AND [System.WorkItemType] = 'User Story'
            AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
        ORDER BY [System.Id]"""
    }
    
    try:
        response = requests.post(url, headers=headers_wiql, json=query)
        response.raise_for_status()
        result = response.json()
        work_items = result.get('workItems', [])
        
        # Get full details for each work item
        user_stories = []
        for wi in work_items:
            wi_url = f"{ORG_URL}/_apis/wit/workitems/{wi['id']}?api-version=7.1"
            wi_response = requests.get(wi_url, headers=headers)
            if wi_response.status_code == 200:
                user_stories.append(wi_response.json())
        
        print(f"   ✓ Found {len(user_stories)} User Stories")
        return user_stories
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return []

def update_user_story_title(work_item_id: int, current_title: str, new_title: str):
    """Update User Story title"""
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.1"
    
    operations = [{
        "op": "replace",
        "path": "/fields/System.Title",
        "value": new_title
    }]
    
    try:
        response = requests.patch(url, headers=headers_patch, json=operations)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"      ✗ Error: {str(e)[:100]}")
        return False

def main():
    print("=" * 60)
    print("Update User Story Titles with Categories")
    print("=" * 60)
    
    # Get all User Stories
    user_stories = get_all_user_stories()
    
    if not user_stories:
        print("\n❌ No User Stories found")
        return 1
    
    print(f"\n📝 Updating User Story titles...")
    print("   Format: [Category] - [Title]\n")
    
    updated_count = 0
    skipped_count = 0
    
    for idx, story in enumerate(user_stories, 1):
        story_id = story['id']
        fields = story['fields']
        current_title = fields.get('System.Title', '')
        
        # Determine category
        category = None
        for title_pattern, cat in CATEGORY_MAPPING.items():
            if title_pattern in current_title:
                category = cat
                break
        
        # If no category found, try to infer from tags
        if not category:
            tags = fields.get('System.Tags', '')
            if 'apps' in tags or 'modules' in tags:
                category = "Apps & Modules"
            elif 'users' in tags:
                category = "Users"
            elif 'authentication' in tags or 'oauth' in tags:
                category = "Authentication"
            elif 'companies' in tags:
                category = "Companies"
            elif 'email' in tags:
                category = "Email Communication"
            elif 'iot' in tags:
                category = "IoT"
            elif 'integrations' in tags:
                category = "Integrations"
            elif 'developer' in tags:
                category = "Developer Mode"
        
        # Check if title already has category prefix
        if current_title.startswith('[') or ' - ' in current_title[:20]:
            print(f"   [{idx}/{len(user_stories)}] ID {story_id}: Already formatted - SKIP")
            skipped_count += 1
            continue
        
        if category:
            new_title = f"[{category}] - {current_title}"
            
            print(f"   [{idx}/{len(user_stories)}] ID {story_id}:", end=" ")
            print(f"\n      Old: {current_title}")
            print(f"      New: {new_title}", end=" ")
            
            if update_user_story_title(story_id, current_title, new_title):
                print("✓")
                updated_count += 1
            else:
                print("✗")
            
            time.sleep(0.2)  # Rate limiting
        else:
            print(f"   [{idx}/{len(user_stories)}] ID {story_id}: No category found - SKIP")
            print(f"      Title: {current_title}")
            skipped_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Update Complete!")
    print("=" * 60)
    print(f"✓ Updated: {updated_count} User Stories")
    print(f"⊘ Skipped: {skipped_count} User Stories")
    print(f"📊 Total: {len(user_stories)} User Stories")
    
    print(f"\n🔗 View Changes:")
    print(f"   Backlog: {ORG_URL}/{PROJECT}/_backlogs/backlog")
    print(f"   Sprint: {ORG_URL}/{PROJECT}/_sprints/taskboard/{SPRINT_NAME.replace(' ', '%20')}")
    print(f"   Queries: {ORG_URL}/{PROJECT}/_queries")
    
    print(f"\n💡 Changes are immediately visible in:")
    print(f"   • Backlogs page")
    print(f"   • Sprint Taskboard")
    print(f"   • Work Item queries")
    print(f"   • All dashboards")
    
    return 0

if __name__ == "__main__":
    exit(main())
