#!/usr/bin/env python3
"""
Professional Board Configuration for Azure DevOps
Configures Kanban boards, columns, card settings, and swimlanes
"""

import requests
from base64 import b64encode
import json
import os

# Configuration
ORG_URL = "https://dev.azure.com/Aries-Test"
PROJECT = "Odoo-Dev"
TEAM = "Odoo-Dev Team"
PAT = os.environ.get('AZURE_DEVOPS_PAT') or input('Enter your Azure DevOps PAT: ').strip()

# Create auth header
auth_string = f":{PAT}"
auth_b64 = b64encode(auth_string.encode('ascii')).decode('ascii')
headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def get_team_id():
    """Get team ID"""
    url = f"{ORG_URL}/_apis/projects/{PROJECT}/teams?api-version=7.1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        teams = response.json().get('value', [])
        for team in teams:
            if team['name'] == TEAM:
                return team['id']
    return None

def get_boards(team_id):
    """Get all boards for the team"""
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards?api-version=7.1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('value', [])
    return []

def configure_stories_board(team_id, board_id):
    """Configure Stories board with custom columns and settings"""
    print("\n📋 Configuring Stories Board...")
    
    # Define custom columns for Stories board
    columns = [
        {"name": "New", "itemLimit": 0, "stateMappings": {"User Story": "New"}},
        {"name": "Ready", "itemLimit": 10, "stateMappings": {"User Story": "Active"}},
        {"name": "In Progress", "itemLimit": 8, "stateMappings": {"User Story": "Active"}},
        {"name": "Code Review", "itemLimit": 5, "stateMappings": {"User Story": "Active"}},
        {"name": "Testing", "itemLimit": 5, "stateMappings": {"User Story": "Resolved"}},
        {"name": "Done", "itemLimit": 0, "stateMappings": {"User Story": "Closed"}}
    ]
    
    # Get current board configuration
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards/{board_id}/columns?api-version=7.1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        current_columns = response.json().get('value', [])
        print(f"   Current columns: {len(current_columns)}")
        
        # Note: Modifying board columns requires different API approach
        # For now, we'll document the recommended configuration
        print("   ✓ Board configuration retrieved")
        return True
    else:
        print(f"   ✗ Failed to get board configuration: {response.status_code}")
        return False

def configure_card_fields(team_id, board_id):
    """Configure card fields displayed on board"""
    print("\n🎴 Configuring Card Fields...")
    
    # Define fields to show on cards
    card_settings = {
        "cards": {
            "User Story": [
                {"fieldIdentifier": "System.AssignedTo", "displayType": "AVATAR"},
                {"fieldIdentifier": "System.Tags", "displayType": "CORE"},
                {"fieldIdentifier": "System.State", "displayType": "CORE"},
                {"fieldIdentifier": "Microsoft.VSTS.Scheduling.StoryPoints", "displayType": "CORE"},
                {"fieldIdentifier": "System.IterationPath", "displayType": "CORE"}
            ],
            "Task": [
                {"fieldIdentifier": "System.AssignedTo", "displayType": "AVATAR"},
                {"fieldIdentifier": "System.Tags", "displayType": "CORE"},
                {"fieldIdentifier": "Microsoft.VSTS.Scheduling.RemainingWork", "displayType": "CORE"},
                {"fieldIdentifier": "System.State", "displayType": "CORE"}
            ]
        }
    }
    
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards/{board_id}/cardsettings?api-version=7.1-preview.2"
    
    # First, get current settings
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("   ✓ Retrieved current card settings")
        return True
    else:
        print(f"   ℹ Card settings: {response.status_code} (may require manual configuration)")
        return False

def configure_swimlanes(team_id, board_id):
    """Configure swimlanes for better organization"""
    print("\n🏊 Configuring Swimlanes...")
    
    # Recommended swimlane configuration
    swimlanes = {
        "defaultLane": {"name": "Default"},
        "lanes": [
            {"name": "Expedite", "color": "red"},
            {"name": "Standard", "color": "blue"},
            {"name": "Low Priority", "color": "gray"}
        ]
    }
    
    print("   ℹ Swimlanes configuration prepared")
    print("   Note: Swimlanes typically configured via web UI")
    return True

def get_board_settings(team_id, board_id):
    """Get current board settings"""
    url = f"{ORG_URL}/{PROJECT}/{team_id}/_apis/work/boards/{board_id}/boardsettings?api-version=7.1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def print_board_recommendations():
    """Print recommendations for board configuration"""
    print("\n" + "=" * 60)
    print("📊 PROFESSIONAL BOARD CONFIGURATION RECOMMENDATIONS")
    print("=" * 60)
    
    print("\n1. STORIES BOARD (Kanban)")
    print("   Recommended Columns:")
    print("   • New → Ready → In Progress → Code Review → Testing → Done")
    print("   • Set WIP limits: Ready(10), In Progress(8), Code Review(5)")
    print()
    
    print("2. CARD CUSTOMIZATION")
    print("   Show on User Story cards:")
    print("   • Assigned To (avatar)")
    print("   • Category Tags")
    print("   • Story Points")
    print("   • Iteration")
    print()
    print("   Show on Task cards:")
    print("   • Assigned To (avatar)")
    print("   • Remaining Work")
    print("   • State")
    print()
    
    print("3. SWIMLANES")
    print("   Configure by:")
    print("   • Priority (Expedite / Standard / Low)")
    print("   • Category ([Apps & Modules], [Users], [IoT], etc.)")
    print("   • Parent (Group by User Story)")
    print()
    
    print("4. BOARD FILTERS")
    print("   Create quick filters for:")
    print("   • My Work (Assigned to @Me)")
    print("   • Blocked Items")
    print("   • High Priority")
    print("   • By Category (Apps, Users, IoT, etc.)")
    print()
    
    print("5. SPRINT BOARD")
    print("   • Use for daily standups")
    print("   • Track sprint progress")
    print("   • Update remaining work daily")
    print("   • Review burndown chart")
    print()

def create_board_setup_guide():
    """Create a detailed setup guide"""
    guide = """
# Professional Azure DevOps Boards Configuration Guide

## 🎯 Overview
This guide provides step-by-step instructions for setting up professional boards in Azure DevOps for the Odoo-Dev project.

## 📋 Board Types

### 1. Stories Board (Kanban)
**Purpose:** Continuous flow of User Stories across development lifecycle

**Configuration Steps:**
1. Navigate to: Boards → Boards → Stories
2. Click ⚙️ (Board settings)
3. Configure Columns:
   - **New** (No WIP limit) → New User Stories
   - **Ready** (WIP: 10) → Groomed and ready for development
   - **In Progress** (WIP: 8) → Active development
   - **Code Review** (WIP: 5) → Awaiting/in review
   - **Testing** (WIP: 5) → QA/Testing phase
   - **Done** (No WIP limit) → Completed stories

4. Column → State Mapping:
   - New → New
   - Ready, In Progress, Code Review → Active
   - Testing → Resolved
   - Done → Closed

### 2. Sprint Board (Taskboard)
**Purpose:** Sprint execution and daily task tracking

**Already Configured:**
- Sprint: General settings
- Duration: 4 weeks (Dec 27, 2025 - Jan 24, 2026)
- Work Items: 225 assigned

**Access:** Boards → Sprints → Taskboard

### 3. Features Board
**Purpose:** Track higher-level features (if using Epic → Feature → Story hierarchy)

## 🎴 Card Customization

### User Story Cards
**Fields to Display:**
1. **Assigned To** (Avatar with user photo)
2. **Tags** (Category tags: Apps & Modules, Users, IoT, etc.)
3. **Story Points** (Effort estimation)
4. **State** (New, Active, Resolved, Closed)
5. **Iteration** (Sprint name)
6. **Priority** (1=Critical, 2=High, 3=Medium, 4=Low)

**Setup:**
1. Board Settings → Card Fields
2. Select "User Story"
3. Add fields from list above
4. Arrange in preferred order

### Task Cards
**Fields to Display:**
1. **Assigned To** (Avatar)
2. **Remaining Work** (Hours remaining)
3. **State** (To Do, In Progress, Done)
4. **Tags** (If needed)
5. **Original Estimate** (Initial hours)

## 🏊 Swimlane Configuration

### Option 1: By Priority
```
┌─────────────────────────────────────┐
│ 🔴 Expedite (Priority 1)           │
├─────────────────────────────────────┤
│ 🔵 Standard (Priority 2-3)         │
├─────────────────────────────────────┤
│ ⚪ Low Priority (Priority 4)       │
└─────────────────────────────────────┘
```

### Option 2: By Category (Recommended)
```
┌─────────────────────────────────────┐
│ 📱 Apps & Modules                  │
├─────────────────────────────────────┤
│ 👥 Users & Authentication          │
├─────────────────────────────────────┤
│ 📧 Email Communication             │
├─────────────────────────────────────┤
│ 🤖 IoT                             │
├─────────────────────────────────────┤
│ 🔌 Integrations                    │
└─────────────────────────────────────┘
```

**Setup:**
1. Board Settings → Swimlanes
2. Choose grouping: Tag or Custom field
3. For category-based: Create query for each category
4. For priority-based: Use Priority field

## 🔍 Board Filters

### Quick Filters to Create

1. **My Work**
   - Field: Assigned To
   - Operator: = @Me

2. **Blocked**
   - Field: Tags
   - Operator: Contains
   - Value: Blocked

3. **High Priority**
   - Field: Priority
   - Operator: <= 2

4. **Apps & Modules**
   - Field: Tags
   - Operator: Contains
   - Value: Apps & Modules

5. **No Assignee**
   - Field: Assigned To
   - Operator: Is Empty

**Setup:**
1. Board view → Filter icon
2. Add filter
3. Save as "Favorite"
4. Access via quick filter dropdown

## 📊 Board Styling

### Card Colors
**Configure by Tags:**
1. Board Settings → Styles
2. Add styling rule:
   - Rule: Tag equals "Critical"
   - Card color: Red
   - Repeat for different tags/priorities

**Recommended Color Coding:**
- 🔴 Critical/Blocked: Red
- 🟠 High Priority: Orange
- 🟡 In Review: Yellow
- 🟢 Ready to Deploy: Green
- 🔵 Standard: Blue

## 🎯 Best Practices

### Daily Usage
1. **Morning Standup:**
   - Open Sprint Taskboard
   - Review "In Progress" column
   - Update remaining work on tasks
   - Move completed tasks to Done

2. **Sprint Planning:**
   - Use Product Backlog view
   - Drag stories to sprint
   - Check team capacity
   - Set sprint goal

3. **Refinement:**
   - Stories board → New column
   - Add acceptance criteria
   - Estimate story points
   - Move to Ready column

### Workflow Rules
1. **User Story must have:**
   - Clear title with category prefix
   - Acceptance criteria
   - Story point estimate
   - At least one task

2. **Before moving to "In Progress":**
   - User Story assigned to developer
   - Tasks created and estimated
   - Dependencies identified

3. **Before moving to "Done":**
   - All tasks completed
   - Code reviewed and merged
   - Tests passing
   - Documentation updated

## 🔗 Quick Access URLs

- **Stories Board:** https://dev.azure.com/Aries-Test/Odoo-Dev/_boards/board/t/Odoo-Dev%20Team/Stories
- **Sprint Taskboard:** https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings
- **Product Backlog:** https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog
- **Board Settings:** Click ⚙️ icon on any board

## 📝 Manual Configuration Required

The following must be configured through the web UI:

1. ✅ **Board Columns** - Add custom columns to Stories board
2. ✅ **Card Fields** - Select which fields appear on cards
3. ✅ **Swimlanes** - Configure swimlane grouping
4. ✅ **Styling Rules** - Set card colors based on criteria
5. ✅ **Quick Filters** - Create and save custom filters
6. ✅ **Column WIP Limits** - Set work-in-progress limits

## 🎓 Training Resources

- [Azure Boards Overview](https://learn.microsoft.com/en-us/azure/devops/boards/get-started/what-is-azure-boards)
- [Customize Kanban Board](https://learn.microsoft.com/en-us/azure/devops/boards/boards/customize-cards)
- [Sprint Planning](https://learn.microsoft.com/en-us/azure/devops/boards/sprints/assign-work-sprint)

---

**Next:** See AZURE_DEVOPS_PROFESSIONAL_SETUP.md for complete Azure DevOps configuration
"""
    
    return guide

def main():
    print("=" * 60)
    print("Professional Board Configuration")
    print("=" * 60)
    
    # Get team ID
    print("\n🔍 Getting team information...")
    team_id = get_team_id()
    if not team_id:
        print("   ✗ Could not find team")
        return 1
    print(f"   ✓ Team ID: {team_id}")
    
    # Get boards
    print("\n📋 Getting boards...")
    boards = get_boards(team_id)
    if not boards:
        print("   ✗ No boards found")
        return 1
    
    print(f"   ✓ Found {len(boards)} boards:")
    stories_board = None
    for board in boards:
        print(f"      • {board['name']} (ID: {board['id']})")
        if board['name'] == 'Stories':
            stories_board = board
    
    # Configure Stories board
    if stories_board:
        configure_stories_board(team_id, stories_board['id'])
        configure_card_fields(team_id, stories_board['id'])
        configure_swimlanes(team_id, stories_board['id'])
    
    # Print recommendations
    print_board_recommendations()
    
    # Create setup guide
    print("\n📄 Creating board setup guide...")
    guide_content = create_board_setup_guide()
    guide_path = "BOARD_CONFIGURATION_GUIDE.md"
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    print(f"   ✓ Guide created: {guide_path}")
    
    print("\n" + "=" * 60)
    print("✅ Board Configuration Analysis Complete!")
    print("=" * 60)
    print(f"\n📖 Review the guide: {guide_path}")
    print("\n💡 Most board customizations require web UI configuration")
    print("   Follow the guide for step-by-step instructions")
    
    return 0

if __name__ == "__main__":
    exit(main())
