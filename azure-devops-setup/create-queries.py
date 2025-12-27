#!/usr/bin/env python3
"""
Create Shared Queries for General settings Sprint Dashboard
These queries can be manually added to a dashboard or viewed directly
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

def create_query(query_name: str, wiql: str, folder="Shared Queries"):
    """Create a shared query"""
    print(f"\n📝 Creating query: {query_name}...")
    
    # Try to create in Shared Queries folder
    url = f"{ORG_URL}/{PROJECT}/_apis/wit/queries/{folder.replace(' ', '%20')}?api-version=7.1"
    
    query_data = {
        "name": query_name,
        "wiql": wiql
    }
    
    try:
        response = requests.post(url, headers=headers, json=query_data)
        response.raise_for_status()
        query_id = response.json().get('id')
        query_url = response.json().get('_links', {}).get('html', {}).get('href', '')
        print(f"   ✓ Created query ID: {query_id}")
        return query_id, query_url
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response and e.response.status_code == 409:
            print(f"   ⚠ Query already exists")
            return None, None
        print(f"   ✗ Error: {e}")
        return None, None

def main():
    print("=" * 60)
    print(f"Create Queries for '{SPRINT_NAME}' Sprint")
    print("=" * 60)
    
    queries = []
    
    # 1. All Sprint Work Items
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] All Work Items",
        f"""SELECT
    [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AssignedTo],
    [System.Tags]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
ORDER BY [System.WorkItemType] DESC, [System.Id] ASC"""
    )
    if query_id:
        queries.append(("All Work Items", query_id, query_url))
    
    # 2. User Stories Only
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] User Stories",
        f"""SELECT
    [System.Id],
    [System.Title],
    [System.State],
    [System.AssignedTo],
    [Microsoft.VSTS.Scheduling.StoryPoints],
    [System.Tags]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.WorkItemType] = 'User Story'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
ORDER BY [System.Id] ASC"""
    )
    if query_id:
        queries.append(("User Stories", query_id, query_url))
    
    # 3. Tasks Only
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] Tasks",
        f"""SELECT
    [System.Id],
    [System.Title],
    [System.State],
    [System.AssignedTo],
    [Microsoft.VSTS.Scheduling.OriginalEstimate],
    [Microsoft.VSTS.Scheduling.RemainingWork],
    [System.Tags]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.WorkItemType] = 'Task'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
ORDER BY [System.Id] ASC"""
    )
    if query_id:
        queries.append(("Tasks", query_id, query_url))
    
    # 4. Active Work Items
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] Active Items",
        f"""SELECT
    [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AssignedTo]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
    AND [System.State] = 'Active'
ORDER BY [System.WorkItemType] DESC, [System.Id] ASC"""
    )
    if query_id:
        queries.append(("Active Items", query_id, query_url))
    
    # 5. Completed Work Items
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] Completed Items",
        f"""SELECT
    [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State],
    [System.AssignedTo],
    [Microsoft.VSTS.Common.ClosedDate]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
    AND [System.State] IN ('Done', 'Closed')
ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC"""
    )
    if query_id:
        queries.append(("Completed Items", query_id, query_url))
    
    # 6. Unassigned Items
    query_id, query_url = create_query(
        f"[{SPRINT_NAME}] Unassigned Items",
        f"""SELECT
    [System.Id],
    [System.WorkItemType],
    [System.Title],
    [System.State]
FROM WorkItems
WHERE [System.TeamProject] = '{PROJECT}'
    AND [System.IterationPath] = '{PROJECT}\\{SPRINT_NAME}'
    AND [System.AssignedTo] = ''
ORDER BY [System.WorkItemType] DESC, [System.Id] ASC"""
    )
    if query_id:
        queries.append(("Unassigned Items", query_id, query_url))
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Query Creation Complete!")
    print("=" * 60)
    print(f"Created {len(queries)} queries for '{SPRINT_NAME}' sprint\n")
    
    print("📋 Created Queries:")
    for name, qid, qurl in queries:
        print(f"   ✓ {name} (ID: {qid})")
    
    print(f"\n🔗 View Queries in Azure DevOps:")
    print(f"   {ORG_URL}/{PROJECT}/_queries")
    
    print(f"\n📊 To Create Dashboard Manually:")
    print("   1. Go to: Overview → Dashboards")
    print("   2. Click: + New Dashboard")
    print(f"   3. Name: 'General Settings Sprint Dashboard'")
    print("   4. Add widgets:")
    print("      • Sprint Overview")
    print("      • Sprint Burndown")
    print("      • Sprint Capacity")
    print("      • Query Results widgets using the queries above")
    print("      • Work Item Chart (by State)")
    print("      • Work Item Chart (by Type)")
    
    print(f"\n💡 Quick Links:")
    print(f"   • Queries: {ORG_URL}/{PROJECT}/_queries")
    print(f"   • Boards: {ORG_URL}/{PROJECT}/_boards/board")
    print(f"   • Sprint: {ORG_URL}/{PROJECT}/_sprints/taskboard/{SPRINT_NAME.replace(' ', '%20')}")
    print(f"   • Backlog: {ORG_URL}/{PROJECT}/_backlogs/backlog")
    
    return 0

if __name__ == "__main__":
    exit(main())
