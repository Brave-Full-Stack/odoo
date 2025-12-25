# Azure DevOps Setup Guide for Odoo Microservices Project

## Prerequisites

- Python 3.8 or higher
- `requests` library
- Azure DevOps account (free for up to 5 users)

## Step 1: Create Azure DevOps Account & Project

### 1.1 Sign Up
1. Go to https://dev.azure.com
2. Sign in with Microsoft account (or create new one)
3. Your organization URL will be: `https://dev.azure.com/YOUR_ORG_NAME`

### 1.2 Create Project
1. Click **"+ New Project"**
2. **Project name:** `Odoo-Microservices` (or your preferred name)
3. **Visibility:** Private (recommended)
4. **Work item process:** Agile (recommended) or Scrum
5. Click **"Create"**

### 1.3 Create Personal Access Token (PAT)
1. Click your profile icon (top right) → **"Personal access tokens"**
2. Click **"+ New Token"**
3. **Name:** `Odoo-microservices`  *(This is just the label of the Azure DevOps token)*
4. **Organization:** Odoo-Microservices
5. **Expiration:** 6 months
6. **Scopes:** 
   - ✅ Work Items: **Read, write, & manage**
7. Click **"Create"**
8. **⚠️ COPY THE TOKEN NOW** - You'll need this for the `.env` file (it won't be shown again)

## Step 2: Install Dependencies

```bash
cd /home/brave/Desktop/FullStack/odoo

# Install Python requests library
pip install requests

# Or if using system Python:
sudo apt install python3-pip -y
pip3 install requests
```

## Step 3: Configure Environment Variables (Optional but Recommended)

Create a `.env` file to avoid typing credentials every time:

```bash
# Create .env file
cat > .azure_devops.env << 'EOF'
export AZURE_DEVOPS_ORG="your-organization-name"
export AZURE_DEVOPS_PROJECT="Odoo-Microservices"
export AZURE_DEVOPS_PAT="your-personal-access-token-here"
EOF

# Load variables
source .azure_devops.env
```

**⚠️ Security Note:** Add `.azure_devops.env` to `.gitignore` to avoid committing tokens!

```bash
echo ".azure_devops.env" >> .gitignore
```

## Step 4: Run the Import Script

### Option A: With Environment Variables
```bash
# Load environment variables first
source .azure_devops.env

# Run import script
python3 import_to_azure_devops.py
```

### Option B: Interactive Mode
```bash
# Run script (it will prompt for credentials)
python3 import_to_azure_devops.py

# You'll be asked:
# Enter Azure DevOps Organization: your-org-name
# Enter Project Name: Odoo-Microservices
# Enter Personal Access Token: paste-your-token-here
```

### Expected Output
```
======================================================================
Azure DevOps Work Item Importer - Odoo Microservices
======================================================================

🔌 Testing connection...
✓ Connected to Azure DevOps organization: your-org-name

📥 Reading tasks from PROGRESS_TRACKER.csv...
✓ Found 297 tasks to import

🔨 Phase 1: Creating work items...
  ✓ Created: 0.1.1 - Document 11 microservices... (ID: 1)
  ✓ Created: 0.1.2 - Define service boundaries... (ID: 2)
  [... 295 more tasks ...]

✓ Created 297 work items

🔗 Phase 2: Creating dependencies...
  ✓ Linked: 0.1.1 → 0.1.2
  ✓ Linked: 0.1.2 → 0.1.3
  [... more dependencies ...]

✓ Created 156 dependencies

======================================================================
📊 IMPORT SUMMARY
======================================================================
Total tasks in CSV:       297
Work items created:       297
Dependencies created:     156
Success rate:             100.0%
======================================================================

✅ Import complete! View at: https://dev.azure.com/your-org/Odoo-Microservices/_workitems
```

## Step 5: Verify Import in Azure DevOps

1. Open: `https://dev.azure.com/YOUR_ORG/Odoo-Microservices/_workitems`
2. You should see 297 work items organized by:
   - **Title:** Task name from CSV
   - **State:** To Do / Doing / Done (mapped from Status)
   - **Priority:** 1-4 (mapped from Critical/High/Medium/Low)
   - **Tags:** Phase-0, Phase-1, ..., Microservices, Odoo19
   - **Description:** Contains Phase, Task ID, Duration, Dependencies, Notes

## Step 6: Configure Azure Boards

### 6.1 Create Custom Views

**By Phase:**
1. Go to **Boards** → **Work Items**
2. Click **"+ New query"**
3. Add filter: `Tags` `Contains` `Phase-0`
4. Save as: "Phase 0: System Design"
5. Repeat for Phases 1-9

**Sprint Planning (Recommended):**
1. Go to **Boards** → **Sprints**
2. Create sprints aligned with your timeline:
   - Sprint 1 (Week 1-2): Phases 0-1
   - Sprint 2 (Week 2-3): Phase 2 (MVP)
   - Sprint 3 (Week 3-4): Phases 3-4
   - Sprint 4 (Week 4-5): Phases 5-6
   - Sprint 5 (Week 5-6): Phases 7-8
   - Sprint 6 (Week 6+): Phase 9 + Cloud

### 6.2 Configure Board Columns

1. Go to **Boards** → **Board** → **⚙️ Settings**
2. Configure columns:
   - **To Do** (Not Started)
   - **Doing** (In Progress)
   - **Review** (optional)
   - **Done** (Completed)

### 6.3 Enable Dependencies Visualization

1. Go to **Boards** → **Backlogs**
2. Click **"View options"** → Enable **"Show parents"**
3. Go to **Boards** → **Delivery Plans** → **"+ New plan"**
4. Add your backlog to visualize dependencies timeline

## Step 7: Daily Workflow

### Morning Standup
1. Open Azure DevOps Board
2. Review **Doing** column
3. Move new task from **To Do** to **Doing**
4. Check dependencies (predecessor tasks must be Done)

### During Work
1. Update work item:
   - Add comments (discoveries, blockers)
   - Update **Remaining Work** hours
   - Change state if blocked
2. Link commits to work items:
   ```bash
   git commit -m "Implement auth service #123"
   # #123 = work item ID
   ```

### End of Day
1. Update **Completed Work** hours
2. Move finished tasks to **Done**
3. Add blockers as comments

## Step 8: Export Progress (Weekly)

### Option A: Export to Excel
1. Go to **Boards** → **Queries**
2. Run query: "All Work Items"
3. Click **"Open in Excel"**
4. Save as: `progress-week-N.xlsx`

### Option B: Export to CSV
1. Go to **Boards** → **Work Items**
2. Select all items (Ctrl+A)
3. Click **"⋯"** → **"Export to CSV"**

### Option C: Dashboard (Visual)
1. Go to **Overview** → **Dashboards**
2. Click **"+ New dashboard"**
3. Add widgets:
   - **Sprint Burndown**
   - **Work Item Chart** (by state)
   - **Work Item Chart** (by priority)
   - **Velocity**

## Advanced Features

### GitHub Integration
Link your repo to Azure DevOps:
1. Go to **Project Settings** → **GitHub connections**
2. Connect repository: `odoo/odoo`
3. Enable:
   - **Auto-link work items** (from commit messages)
   - **Create work items from GitHub issues**

### CI/CD Integration (Phase 8)
When you reach Phase 8:
1. Azure DevOps has built-in **Azure Pipelines**
2. Use for CI/CD instead of GitHub Actions (or both!)
3. The import script already tracks your tasks

### Notifications
1. Go to **Project Settings** → **Notifications**
2. Enable:
   - **Work item assigned to me**
   - **Work item changed**
   - **Build completed**

## Troubleshooting

### Error: "VS402337: The work item does not exist"
- **Cause:** Invalid project name or permissions
- **Fix:** Verify project name, check PAT has "Work Items (Read, Write, & Manage)" scope

### Error: "HTTP 401 Unauthorized"
- **Cause:** Invalid or expired PAT
- **Fix:** Generate new PAT, ensure it's copied correctly

### Error: "HTTP 400 Bad Request"
- **Cause:** Invalid field values
- **Fix:** Check CSV data for special characters, ensure dates are in ISO format

### Script hangs on dependency creation
- **Cause:** Circular dependencies or invalid task IDs in Blockers column
- **Fix:** Review PROGRESS_TRACKER.csv, ensure blockers reference valid Task IDs

### ImportError: No module named 'requests'
```bash
pip3 install requests
# or
pip3 install --user requests
```

## Cost Breakdown

| Users | Monthly Cost | Features |
|-------|-------------|----------|
| 1-5 | **FREE** | Basic features, 2 GB storage, 1 parallel job |
| 6-10 | $6/user | All free features |
| 11-100 | $6/user | + Advanced analytics |
| Enterprise | Custom | + Unlimited artifacts |

**Your case:** FREE (solo developer, <5 users)

## Resources

- **Azure DevOps Docs:** https://learn.microsoft.com/en-us/azure/devops/
- **Work Item API:** https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/
- **Board Basics:** https://learn.microsoft.com/en-us/azure/devops/boards/get-started/
- **Query Guide:** https://learn.microsoft.com/en-us/azure/devops/boards/queries/

## Next Steps After Import

1. ✅ Verify all 297 tasks imported successfully
2. ✅ Create Sprint 1 and add Phase 0-1 tasks
3. ✅ Move first task (0.1.1) to **Doing**
4. ✅ Follow [GETTING_STARTED.md](GETTING_STARTED.md) to begin implementation
5. ✅ Commit code with work item references: `git commit -m "feat: auth service #1"`

## Advanced Configuration

For production-grade setup including CI/CD pipelines, service connections, environments, and monitoring:

📘 **[Azure DevOps Advanced Guide](AZURE_DEVOPS_ADVANCED.md)**

This guide covers:
- 🔗 Service connections (Harbor, Kubernetes, Azure, AWS)
- 🔐 Variable groups and secrets management
- 🌍 Environment setup with approval gates
- 🔄 Multi-stage CI/CD pipelines for all 11 microservices
- 📊 Dashboard and monitoring configuration
- 🔔 Integration with Slack, Teams, GitHub
- 🛡️ Security scanning and compliance

### Quick Start: Run All Setup

```bash
# Run automated Azure DevOps setup
./scripts/setup-azure-devops.sh

# Or step by step:
python3 import_to_azure_devops.py                    # Import work items
./scripts/configure-service-connections.sh            # Setup connections
./scripts/create-variable-groups.sh                   # Create variable groups
./scripts/setup-environments.sh                       # Configure environments
```

## Available CI/CD Pipelines

This project includes production-ready Azure Pipeline configurations:

1. **[microservices-pipeline.yml](ci-cd/azure-pipelines/microservices-pipeline.yml)**
   - Builds all 11 microservices in parallel
   - Runs tests, security scans, code coverage
   - Deploys to Dev → Staging → Production
   - 7 stages with approval gates

2. **[infrastructure-pipeline.yml](ci-cd/azure-pipelines/infrastructure-pipeline.yml)**
   - Terraform/Bicep infrastructure management
   - Helm chart deployments
   - DNS and SSL configuration
   - Monitoring stack setup

3. **[azure-pipelines.yml](ci-cd/azure-pipelines/azure-pipelines.yml)**
   - Legacy monolithic Odoo deployment
   - Docker build and push to Harbor
   - Kubernetes deployment with health checks

### Pipeline Setup in Azure DevOps

1. Go to **Pipelines** → **New pipeline**
2. Select **Azure Repos Git**
3. Choose **Odoo-Microservices** repository
4. Select **Existing Azure Pipelines YAML file**
5. Choose one of:
   - `/ci-cd/azure-pipelines/microservices-pipeline.yml` (recommended)
   - `/ci-cd/azure-pipelines/infrastructure-pipeline.yml`
   - `/ci-cd/azure-pipelines/azure-pipelines.yml`
6. Click **Run**

---

**Questions?** Check troubleshooting section above or Azure DevOps documentation.
