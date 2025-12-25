# Azure DevOps Setup

Complete automation and documentation for Azure DevOps Boards configuration for the Odoo Microservices project.

## 📁 Folder Structure

```
azure-devops-setup/
├── README.md                    # This file
├── .env                         # Azure DevOps credentials (copy of .azure_devops.env)
├── scripts/                     # Automation scripts
│   ├── import_to_azure_devops.py          # Import tasks from CSV
│   ├── create_epics_and_stories.py        # Create Epics and User Stories
│   ├── link_tasks_to_stories.py           # Link tasks to their parent stories
│   ├── create_sprints.py                  # Create and configure sprints
│   ├── generate_dashboard.py              # Generate sprint dashboard
│   └── test_azure_connection.py           # Test Azure DevOps connection
└── docs/                        # Documentation
    ├── AZURE_DEVOPS_SETUP.md              # Initial setup guide
    ├── AZURE_BOARDS_CONFIGURATION_GUIDE.md # Manual configuration steps
    └── AZURE_BOARDS_SETUP_COMPLETE.md     # Completion summary
```

## 🚀 Quick Start

### 1. Configure Environment Variables

```bash
# Copy and edit the .env file with your credentials
cp .env.example .env
nano .env
```

Required variables:
```
AZURE_DEVOPS_ORG=your-org-name
AZURE_DEVOPS_PROJECT=your-project-name
AZURE_DEVOPS_PAT=your-personal-access-token
```

### 2. Run Setup Scripts

```bash
# Source environment variables
source .env

# Step 1: Import tasks from CSV (if not already done)
python3 scripts/import_to_azure_devops.py

# Step 2: Create Epics and User Stories
python3 scripts/create_epics_and_stories.py

# Step 3: Link tasks to user stories
python3 scripts/link_tasks_to_stories.py

# Step 4: Create sprints
python3 scripts/create_sprints.py

# Step 5: Generate dashboard
python3 scripts/generate_dashboard.py
```

## 📊 Sprint Structure

The project is organized into 6 sprints:

| Sprint | Duration | Phases | Work Items |
|--------|----------|--------|------------|
| Sprint 1 | 10 days | Phase 0-1 | ~46 tasks |
| Sprint 2 | 10 days | Phase 2-3 | ~64 tasks |
| Sprint 3 | 10 days | Phase 4-5 | ~41 tasks |
| Sprint 4 | 5 days  | Phase 6-7 | ~30 tasks |
| Sprint 5 | 5 days  | Phase 8 | ~18 tasks |
| Sprint 6 | 5 days  | Phase 9 + Testing | ~99 tasks |

## 📈 Dashboards

After running `generate_dashboard.py`, you'll get:
- **sprint-dashboard.html** - Interactive HTML dashboard with charts
- **sprint-dashboard.md** - Markdown dashboard for documentation

## 🔗 Quick Links

- **Azure DevOps**: https://dev.azure.com/Aries-Test/Odoo-Microservices
- **Boards**: https://dev.azure.com/Aries-Test/Odoo-Microservices/_boards
- **Backlogs**: https://dev.azure.com/Aries-Test/Odoo-Microservices/_backlogs

## 📝 Scripts Reference

### import_to_azure_devops.py
Imports all 298 tasks from PROGRESS_TRACKER.csv into Azure DevOps.

**Usage**: `python3 scripts/import_to_azure_devops.py`

### create_epics_and_stories.py
Creates 10 Epics (Phases 0-9) and 70 User Stories with proper hierarchy.

**Usage**: `python3 scripts/create_epics_and_stories.py`

### link_tasks_to_stories.py
Links all tasks to their parent user stories based on CHECKLIST.md structure.

**Usage**: `python3 scripts/link_tasks_to_stories.py`

### create_sprints.py
Creates 6 sprints and assigns Epics/Stories to appropriate iterations.

**Usage**: `python3 scripts/create_sprints.py`

### generate_dashboard.py
Generates HTML and Markdown dashboards showing sprint progress and metrics.

**Usage**: `python3 scripts/generate_dashboard.py`

## 📚 Documentation

See the `docs/` folder for detailed guides:
- Setup instructions
- Manual configuration steps
- Completion summary and metrics

## ✅ Setup Status

- [x] Tasks imported (298)
- [x] Epics created (10)
- [x] User Stories created (70)
- [x] Tasks linked to stories (269/298)
- [ ] Sprints created
- [ ] Work items assigned to sprints
- [ ] Dashboard generated

## 🆘 Troubleshooting

### Connection Issues
Run `python3 scripts/test_azure_connection.py` to verify credentials.

### Missing Tasks
Check that PROGRESS_TRACKER.csv is in the parent directory.

### API Rate Limits
Scripts include sleep delays to avoid rate limiting. If you hit limits, wait a few minutes and retry.

## 📞 Support

For issues or questions, check:
1. Documentation in `docs/` folder
2. Script comments and error messages
3. Azure DevOps API documentation

---

**Last Updated**: December 2024
**Project**: Odoo 19 Microservices Migration
