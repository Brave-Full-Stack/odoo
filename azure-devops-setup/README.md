# Azure DevOps Setup for Odoo General Settings

This directory contains Python scripts for importing Odoo 19.0 General Settings configuration from Progress_tracker.csv into Azure DevOps and setting up sprint management.

## 🎯 Project Overview

**Organization:** Aries-Test  
**Project:** Odoo-Dev  
**Sprint:** General settings (4 weeks: Dec 27, 2025 - Jan 24, 2026)  
**Work Items:** 225 total (1 Epic, 42 User Stories, 181 Tasks)

## 📋 Setup Complete

### ✅ Completed Steps

1. **Data Import** - Imported 224 work items from Progress_tracker.csv
2. **Sprint Creation** - Created "General settings" sprint
3. **Work Assignment** - Assigned all 225 work items to sprint
4. **Reporting** - Created 6 shared WIQL queries
5. **Taskboard** - Configured and activated taskboard
6. **Categorization** - Updated User Story titles with category prefixes

### 📊 Work Item Structure

```
Epic (1)
├── [Apps & Modules] User Stories (3)
│   ├── Install and Configure Applications
│   ├── Upgrade Applications
│   └── Uninstall Applications
├── [Users] User Stories (9)
│   ├── User Management
│   ├── Language Configuration
│   ├── Two-Factor Authentication
│   └── ... (6 more)
├── [Authentication] User Stories (4)
│   ├── Facebook OAuth
│   ├── Google OAuth
│   └── ... (2 more)
├── [Companies] User Stories (3)
├── [Email Communication] User Stories (8)
├── [IoT] User Stories (8)
├── [Integrations] User Stories (6)
└── [Developer Mode] User Stories (1)
```

## �� Quick Start

### Prerequisites

```bash
# Install Python dependencies
pip install requests

# Set environment variable for PAT token
export AZURE_DEVOPS_PAT="your-personal-access-token"
```

### Generate Personal Access Token (PAT)

1. Go to: https://dev.azure.com/Aries-Test/_usersSettings/tokens
2. Click "New Token"
3. Grant permissions: Work Items (Read, Write)
4. Copy token and set environment variable

## 📝 Available Scripts

### Core Import Scripts

#### convert-and-import.py
**Status:** ✅ Completed  
**Purpose:** Import Progress_tracker.csv to Azure DevOps

```bash
python3 convert-and-import.py
```

- Parses CSV with EPIC:/USER STORY:/→ Task structure
- Creates 224 work items with proper hierarchy
- Maps priorities: Critical=1, High=2, Medium=3, Low=4
- Converts duration (days) to hours for estimates

#### assign-to-sprint.py
**Status:** ✅ Completed  
**Purpose:** Assign work items to sprint

```bash
python3 assign-to-sprint.py
```

- Assigns all 225 work items to "General settings" sprint
- Tries multiple iteration path formats
- Includes progress tracking

### Configuration Scripts

#### create-queries.py
**Status:** ✅ Completed  
**Purpose:** Create shared WIQL queries for reporting

```bash
python3 create-queries.py
```

Creates 6 queries:
- All Work Items
- User Stories only
- Tasks only
- Active Items
- Completed Items
- Unassigned Items

#### fix-taskboard.py
**Status:** ✅ Completed  
**Purpose:** Fix taskboard visibility by associating sprint with team

```bash
python3 fix-taskboard.py
```

- Associates sprint with Odoo-Dev Team
- Enables taskboard in Sprints section
- Verifies configuration

#### update-user-story-titles.py
**Status:** ✅ Completed  
**Purpose:** Add category prefixes to User Story titles

```bash
python3 update-user-story-titles.py
```

- Updates 42 User Stories
- Format: [Category] - Title
- Categories: Apps & Modules, Users, Authentication, etc.

### Utility Scripts

#### configure-taskboard.py
**Status:** ✅ Verification successful  
**Purpose:** Verify sprint setup and work item counts

```bash
python3 configure-taskboard.py
```

## 🔗 Azure DevOps URLs

### Sprint Management
- **Backlog:** https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog
- **Taskboard:** https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings
- **Sprint Planning:** https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/backlog/General%20settings

### Reporting
- **Queries:** https://dev.azure.com/Aries-Test/Odoo-Dev/_queries
- **Work Items:** https://dev.azure.com/Aries-Test/Odoo-Dev/_workitems

## 📊 Created Queries

| Query Name | ID | Purpose |
|------------|----|-----------------------------------------|
| [General settings] All Work Items | 47ac2509... | All items in sprint |
| [General settings] User Stories | 7fd8d8f3... | User Stories only |
| [General settings] Tasks | 98583350... | Tasks only |
| [General settings] Active Items | 51eae97a... | In Progress work |
| [General settings] Completed Items | 01ac0757... | Finished work |
| [General settings] Unassigned Items | f8c8c7d5... | Unassigned work |

## 🔐 Security Notes

### ⚠️ NEVER COMMIT PAT TOKENS!

All scripts use environment variables for authentication:

```bash
# Set PAT token before running scripts
export AZURE_DEVOPS_PAT="your-token-here"
```

The .gitignore file prevents committing:
- .env files
- *.pat files
- config.ini files

### Safe Usage

```bash
# Option 1: Environment variable (recommended)
export AZURE_DEVOPS_PAT="your-token"
python3 script.py

# Option 2: Interactive prompt
python3 script.py
# Script will prompt: "Enter your Azure DevOps PAT: "
```

## 🗂️ File Structure

```
azure-devops-setup/
├── README.md                      # This file
├── .gitignore                     # Prevents committing secrets
├── .env.example                   # Template for environment variables
│
├── convert-and-import.py          # ✅ Import CSV to Azure DevOps
├── assign-to-sprint.py            # ✅ Assign items to sprint
├── create-queries.py              # ✅ Create WIQL queries
├── fix-taskboard.py               # ✅ Fix taskboard visibility
├── update-user-story-titles.py    # ✅ Add category prefixes
└── configure-taskboard.py         # ✅ Verify configuration
```

## 🎓 What Was Learned

### Azure DevOps Insights

1. **Sprint-Team Association**
   - Creating a sprint at project level ≠ team can access it
   - Must explicitly add sprint to team's iteration settings
   - Fixed by: POST to /{team_id}/_apis/work/teamsettings/iterations

2. **Iteration Path Formats**
   - Different APIs accept different formats
   - Work item assignment: "ProjectName\SprintName"
   - Classification nodes: "\ProjectName\Iteration\SprintName"

3. **Dashboard API Permissions**
   - Dashboard API requires elevated permissions
   - Alternative: Create shared WIQL queries for manual dashboard assembly

4. **API Rate Limiting**
   - Add 0.2-0.3s delays between bulk operations
   - Azure DevOps REST API: 7.1 (various preview versions)

## 📈 Next Steps

### Manual Configuration Required

1. **Team Capacity**
   - Go to Sprint → Capacity tab
   - Set team member work hours
   - Define days off

2. **Work Assignment**
   - Assign User Stories to team members
   - Break down tasks if needed
   - Set remaining work estimates

3. **Dashboard Creation**
   - Use created queries to build custom dashboard
   - Add charts: Burndown, Velocity, CFD

4. **Start Sprint**
   - Review sprint backlog
   - Confirm capacity
   - Begin tracking

## 🛠️ Troubleshooting

### "Taskboard not visible"
Run fix-taskboard.py to associate sprint with team

### "401 Unauthorized"
- Verify PAT token is valid
- Check token has Work Items (Read, Write) permissions
- Ensure token hasn't expired

### "400 Bad Request"
- Check API payload format
- Verify field names match Azure DevOps schema
- Review API version compatibility

### "409 Conflict"
- Resource already exists
- Check if work item/sprint/query name is unique

## 📚 References

- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/)
- [Work Items API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/)
- [WIQL Syntax](https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)

---

**Last Updated:** December 27, 2025  
**Status:** ✅ All setup complete, ready for sprint execution
