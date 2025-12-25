# 🚀 Azure DevOps Quick Start Guide

Complete automation setup for Azure Boards with sprint-based organization.

## 📁 Organized Structure

All Azure DevOps related files are now in the `azure-devops-setup/` folder:

```
azure-devops-setup/
├── README.md                          # Detailed documentation
├── .env                               # Azure credentials
├── sprint-dashboard.html              # 📊 Interactive dashboard (open in browser)
├── sprint-dashboard.md                # 📄 Markdown dashboard
├── scripts/                           # Automation scripts
│   ├── import_to_azure_devops.py
│   ├── create_epics_and_stories.py
│   ├── link_tasks_to_stories.py
│   ├── create_sprints.py             # ✅ Sprint creation
│   └── generate_dashboard.py         # ✅ Dashboard generator
└── docs/                              # Documentation
    ├── AZURE_DEVOPS_SETUP.md
    ├── AZURE_BOARDS_CONFIGURATION_GUIDE.md
    └── AZURE_BOARDS_SETUP_COMPLETE.md
```

## ✅ What's Been Done

- ✅ **298 Tasks** imported from PROGRESS_TRACKER.csv
- ✅ **10 Epics** created (Phases 0-9)
- ✅ **70 User Stories** created with hierarchy
- ✅ **269 Tasks** linked to their parent stories (90% success)
- ✅ **6 Sprints** created with dates
- ✅ **80 Work Items** (Epics + Stories) assigned to sprints
- ✅ **HTML + Markdown Dashboards** generated

## 📊 Sprint Organization

| Sprint | Duration | Phases | Epics | Stories | Dates |
|--------|----------|--------|-------|---------|-------|
| **Sprint 1** | 10 days | Phase 0-1 | 2 | 12 | Dec 25 - Jan 4 |
| **Sprint 2** | 10 days | Phase 2-3 | 2 | 10 | Jan 4 - Jan 14 |
| **Sprint 3** | 10 days | Phase 4-5 | 2 | 11 | Jan 14 - Jan 24 |
| **Sprint 4** | 5 days | Phase 6-7 | 2 | 9 | Jan 24 - Jan 29 |
| **Sprint 5** | 5 days | Phase 8 | 1 | 6 | Jan 29 - Feb 3 |
| **Sprint 6** | 5 days | Phase 9 + Testing | 1 | 22 | Feb 3 - Feb 8 |

## 🎯 Quick Actions

### View Dashboard
```bash
# Open HTML dashboard in browser
xdg-open azure-devops-setup/sprint-dashboard.html

# Or view Markdown dashboard
cat azure-devops-setup/sprint-dashboard.md
```

### Regenerate Dashboard
```bash
cd azure-devops
source .env
python3 scripts/generate_dashboard.py
```

### View in Azure DevOps
- **Project**: https://dev.azure.com/Aries-Test/Odoo-Microservices
- **Boards**: https://dev.azure.com/Aries-Test/Odoo-Microservices/_boards
- **Sprints**: https://dev.azure.com/Aries-Test/Odoo-Microservices/_sprints

## 📈 Dashboard Features

The HTML dashboard includes:
- 📊 **Overall project statistics** (378 total work items)
- 🏃 **Sprint-by-sprint breakdown**
- 📈 **Progress bars** for stories and tasks
- 📋 **Work item lists** (Epics, Stories, Tasks)
- 🎨 **Beautiful responsive design**
- 📱 **Mobile-friendly**

## 🔄 Workflow

1. **Plan Sprint**: Review sprint dashboard to see assigned work
2. **Start Sprint**: Activate sprint in Azure DevOps
3. **Daily Work**: Update task states in Azure DevOps
4. **Review Progress**: Regenerate dashboard to see updated metrics
5. **Complete Sprint**: Close sprint and review retrospective

## 📝 Task States

- **New**: Not started
- **Active**: In progress
- **Resolved**: Completed but not verified
- **Closed**: Completed and verified

## 🛠️ Customization

### Update Sprint Dates
Edit `azure-devops-setup/scripts/create_sprints.py`:
```python
start_date = datetime.now()  # Change this
```

### Modify Sprint Assignments
Edit the `story_ranges` in `create_sprints.py`:
```python
story_ranges = {
    "Sprint 1": range(309, 321),  # Adjust ranges
    ...
}
```

### Regenerate Everything
```bash
cd azure-devops
source .env

# Re-create sprints
python3 scripts/create_sprints.py

# Regenerate dashboard
python3 scripts/generate_dashboard.py
```

## 📊 Key Metrics

From the latest dashboard:

- **Total Work Items**: 378
- **Epics**: 10 (covering all 10 phases)
- **User Stories**: 70 (feature groups)
- **Tasks**: 298 (individual work items)
- **Story Points**: ~250 total
- **Sprint Coverage**: 100% (all Epics and Stories assigned)

## 🔗 Related Files

- **[CHECKLIST.md](./CHECKLIST.md)** - Original task checklist
- **[PROGRESS_TRACKER.csv](./PROGRESS_TRACKER.csv)** - Task tracking spreadsheet
- **[azure-devops-setup/README.md](../README.md)** - Detailed Azure DevOps guide

## 🆘 Troubleshooting

### Dashboard shows "Unassigned"
Run the sprint assignment script:
```bash
cd azure-devops
source .env
python3 scripts/create_sprints.py
```

### Can't connect to Azure DevOps
Check your credentials in `azure-devops-setup/.env`:
```bash
AZURE_DEVOPS_ORG=Aries-Test
AZURE_DEVOPS_PROJECT=Odoo-Microservices
AZURE_DEVOPS_PAT=your-token-here
```

### Need to update work items
Make changes in Azure DevOps UI, then regenerate dashboard:
```bash
cd azure-devops
python3 scripts/generate_dashboard.py
```

## 🎉 Next Steps

1. ✅ Open `azure-devops-setup/sprint-dashboard.html` in your browser
2. ✅ Review Sprint 1 work items
3. ⏳ Start Sprint 1 in Azure DevOps
4. ⏳ Assign team members to tasks
5. ⏳ Begin development!

---

**Happy Sprinting! 🏃‍♂️💨**
