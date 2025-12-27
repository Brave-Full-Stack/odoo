# Azure DevOps Professional Setup for Odoo-Dev Project

Complete guide for professional Azure DevOps configuration including Boards, Repos, Pipelines, and more.

## 🎯 Project Context

**Branch:** Odoo-19.0-local-dev  
**Project:** Odoo-Dev  
**Sprint:** General settings (4 weeks)  
**Work Items:** 225 (1 Epic, 42 User Stories, 181 Tasks)

---

## 📋 Table of Contents

1. [Boards Configuration](#1-boards-configuration)
2. [Repos Integration](#2-repos-integration)
3. [Pipelines Setup](#3-pipelines-setup)
4. [Dashboards](#4-dashboards)
5. [Wiki Documentation](#5-wiki-documentation)
6. [Team Configuration](#6-team-configuration)
7. [Notifications](#7-notifications)
8. [Security & Permissions](#8-security--permissions)

---

## 1. Boards Configuration

### 📊 Current Status
✅ Sprint created and configured  
✅ 225 work items assigned  
✅ Taskboard accessible  
✅ User Stories categorized  

### 🎯 Next Steps

#### A. Stories Board (Kanban)

**Purpose:** Continuous flow management for User Stories

**Recommended Columns:**
```
New → Ready → In Progress → Code Review → Testing → Done
```

**Configuration:**
1. Go to: **Boards → Boards → Stories**
2. Click **⚙️ Board Settings**
3. **Columns Tab:**
   - Add custom columns as shown above
   - Set WIP limits:
     - Ready: 10
     - In Progress: 8
     - Code Review: 5
     - Testing: 5

4. **State Mapping:**
   - New → New
   - Ready, In Progress, Code Review → Active
   - Testing → Resolved
   - Done → Closed

#### B. Card Customization

**User Story Cards - Show:**
- ✅ Assigned To (avatar)
- ✅ Tags (category)
- ✅ Story Points
- ✅ State
- ✅ Iteration
- ✅ Priority

**Task Cards - Show:**
- ✅ Assigned To (avatar)
- ✅ Remaining Work
- ✅ State
- ✅ Original Estimate

**Steps:**
1. Board Settings → **Card Fields**
2. Select work item type
3. Add fields listed above
4. Drag to reorder

#### C. Swimlanes (Recommended: By Category)

```
┌──────────────────────────────────┐
│ 📱 Apps & Modules               │
├──────────────────────────────────┤
│ 👥 Users & Authentication       │
├──────────────────────────────────┤
│ 📧 Email Communication          │
├──────────────────────────────────┤
│ 🤖 IoT                          │
├──────────────────────────────────┤
│ 🔌 Integrations                 │
├──────────────────────────────────┤
│ 🏢 Companies                    │
├──────────────────────────────────┤
│ 🔧 Developer Mode               │
└──────────────────────────────────┘
```

**Setup:**
1. Board Settings → **Swimlanes**
2. Choose: "Group by Tags"
3. Or create custom queries per category

#### D. Board Filters

**Create Quick Filters:**

1. **My Work**
   ```
   [System.AssignedTo] = @Me
   ```

2. **Blocked Items**
   ```
   [System.Tags] Contains "Blocked"
   ```

3. **High Priority**
   ```
   [Microsoft.VSTS.Common.Priority] <= 2
   ```

4. **By Category** (Example: Apps & Modules)
   ```
   [System.Title] Contains "[Apps & Modules]"
   ```

**Steps:**
1. Click **Filter** icon on board
2. Add criteria
3. Click **Save as favorite**

#### E. Styling Rules

**Card Color Coding:**
- 🔴 Red: Critical priority or Blocked
- 🟠 Orange: High priority
- 🟡 Yellow: In Code Review
- 🟢 Green: Ready to Deploy
- 🔵 Blue: Standard priority

**Setup:**
1. Board Settings → **Styles**
2. Add rule:
   - Criteria: `[Priority] = 1`
   - Card color: Red
   - Title color: White
3. Repeat for other priorities/states

---

## 2. Repos Integration

### 🔗 Link Git Repository

**Purpose:** Connect Azure DevOps to your GitHub repository for work item tracking

#### A. Connect GitHub Repository

1. Go to: **Project Settings → GitHub connections**
2. Click **Connect to GitHub**
3. Authorize Azure Pipelines
4. Select repository: `Brave-Full-Stack/odoo`
5. Choose branch: `Odoo-19.0-local-dev`

#### B. Enable Work Item Linking

**In Commit Messages:**
```bash
git commit -m "fix: Update user authentication module

Fixes #381 (User Story: Install and Configure Applications)
Related to #423, #424, #425
"
```

**Patterns Recognized:**
- `Fixes #<id>` - Closes work item
- `Related to #<id>` - Links work item
- `Resolves #<id>` - Resolves work item

#### C. Branch Policies

**Setup Protection for main branches:**

1. **Repos → Branches**
2. Select `Odoo-19.0-local-dev`
3. Click **⋮ → Branch policies**

**Recommended Policies:**
- ✅ Require minimum 1 reviewer
- ✅ Check for linked work items
- ✅ Check for comment resolution
- ✅ Require build validation
- ✅ Automatically include code reviewers

#### D. Pull Request Integration

**Link PRs to Work Items:**

1. Create PR with work item reference in description
2. Or use PR sidebar → **Link work item**
3. Work item shows PR status
4. Auto-close work items when PR merged (if using "Fixes #")

---

## 3. Pipelines Setup

### 🔄 CI/CD Configuration

#### A. Build Pipeline (Continuous Integration)

**Purpose:** Automated testing on every commit

**Create: `.azure-pipelines/ci.yml`**

```yaml
# Odoo CI Pipeline for Odoo-19.0-local-dev
trigger:
  branches:
    include:
    - Odoo-19.0-local-dev
  paths:
    exclude:
    - README.md
    - docs/*

pool:
  vmImage: 'ubuntu-latest'

variables:
  PYTHON_VERSION: '3.11'
  ODOO_VERSION: '19.0'

stages:
- stage: Test
  jobs:
  - job: UnitTests
    displayName: 'Run Odoo Unit Tests'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(PYTHON_VERSION)'
      displayName: 'Use Python $(PYTHON_VERSION)'
    
    - script: |
        pip install -r requirements.txt
      displayName: 'Install dependencies'
    
    - script: |
        python odoo-bin --test-enable --stop-after-init --database test_db
      displayName: 'Run Odoo tests'
      continueOnError: true
    
    - task: PublishTestResults@2
      inputs:
        testResultsFormat: 'JUnit'
        testResultsFiles: '**/test-results.xml'
      displayName: 'Publish test results'

- stage: CodeQuality
  dependsOn: Test
  jobs:
  - job: Lint
    displayName: 'Code Quality Checks'
    steps:
    - script: |
        pip install ruff
        ruff check . --config ruff.toml
      displayName: 'Run Ruff linter'
```

**Setup Steps:**
1. **Pipelines → Create Pipeline**
2. Choose **GitHub** (if connected) or **Azure Repos Git**
3. Select repository and branch
4. Choose **Existing Azure Pipelines YAML file**
5. Select `.azure-pipelines/ci.yml`
6. **Run** and verify

#### B. Deployment Pipeline (Continuous Deployment)

**Create: `.azure-pipelines/cd.yml`**

```yaml
# Odoo CD Pipeline - Deploy to environments
trigger: none # Manual trigger only

pool:
  vmImage: 'ubuntu-latest'

parameters:
- name: environment
  displayName: 'Deployment Environment'
  type: string
  default: 'dev'
  values:
  - dev
  - staging
  - production

stages:
- stage: Deploy
  jobs:
  - deployment: DeployOdoo
    displayName: 'Deploy Odoo to ${{ parameters.environment }}'
    environment: '${{ parameters.environment }}'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              echo "Deploying to ${{ parameters.environment }}"
              # Add your deployment steps here
            displayName: 'Deploy Odoo'
```

#### C. Pipeline Variables

**Project Settings → Pipelines → Library:**

1. Create Variable Group: **Odoo-Config**
2. Add variables:
   - `DB_HOST` = your-db-host
   - `DB_PORT` = 5432
   - `ODOO_ADMIN_PASSWD` = (secret)
   - `AZURE_SUBSCRIPTION_ID` = (if deploying to Azure)

3. Link variable group to pipelines

#### D. Service Connections

**Setup for deployments:**

1. **Project Settings → Service connections**
2. **New service connection**
3. Choose type:
   - **GitHub** (for repo access)
   - **Docker Registry** (for container deployments)
   - **Azure Resource Manager** (for Azure deployments)
   - **SSH** (for VM deployments)

---

## 4. Dashboards

### 📊 Create Sprint Dashboard

**Purpose:** Real-time sprint tracking and metrics

#### A. Create Dashboard

1. **Overview → Dashboards**
2. **New dashboard**
3. Name: **General Settings Sprint**
4. Team: Odoo-Dev Team

#### B. Add Widgets

**Recommended Widgets:**

1. **Sprint Burndown**
   - Type: Burndown Chart
   - Configuration: Current sprint
   - Shows: Remaining work vs. days

2. **Sprint Capacity**
   - Type: Sprint Capacity
   - Shows: Team capacity vs. planned work

3. **Work Items Query**
   - Type: Query Results
   - Query: [General settings] Active Items
   - Shows: Current sprint work items

4. **Cumulative Flow Diagram**
   - Type: CFD
   - Shows: Work distribution across board columns

5. **Velocity**
   - Type: Velocity Chart
   - Shows: Story points completed per sprint

6. **Sprint Overview**
   - Type: Sprint Overview
   - Shows: Sprint goals and statistics

7. **Team Members**
   - Type: Team Members
   - Shows: Team roster with capacity

8. **Code Coverage** (if CI configured)
   - Type: Chart for Test Results
   - Shows: Test coverage metrics

#### C. Custom HTML Widgets

**Sprint Goal Widget:**
```html
<div style="padding: 20px; background: #0078d4; color: white;">
  <h2>Sprint Goal</h2>
  <p style="font-size: 18px;">
    Complete General Settings configuration tracking system
    including Apps, Users, Authentication, and IoT modules.
  </p>
  <hr>
  <p><strong>Target:</strong> 225 work items | <strong>Duration:</strong> 4 weeks</p>
</div>
```

**Add via:**
1. Dashboard → Edit
2. Add widget → **Markdown**
3. Paste HTML/Markdown
4. Configure size and position

---

## 5. Wiki Documentation

### 📚 Project Wiki

#### A. Create Wiki Structure

1. **Overview → Wiki**
2. **Create project wiki**
3. Create page structure:

```
📖 Odoo-Dev Wiki
├── 🏠 Home
│   ├── Project Overview
│   ├── Quick Links
│   └── Team Contacts
├── 🎯 Sprint Planning
│   ├── General Settings Sprint
│   ├── Sprint Goals
│   └── Capacity Planning
├── 📋 Work Item Guidelines
│   ├── User Story Template
│   ├── Task Template
│   └── Bug Template
├── 🔧 Development Guide
│   ├── Setup Instructions
│   ├── Coding Standards
│   ├── Git Workflow
│   └── Testing Guidelines
├── 🚀 Deployment
│   ├── Environment Setup
│   ├── Deployment Process
│   └── Rollback Procedures
└── 📊 Reports & Metrics
    ├── Sprint Reports
    ├── Velocity Tracking
    └── Quality Metrics
```

#### B. Home Page Template

```markdown
# Odoo-Dev Project Wiki

## 🎯 Project Overview

**Branch:** Odoo-19.0-local-dev  
**Focus:** General Settings Configuration  
**Sprint:** General settings (Dec 27, 2025 - Jan 24, 2026)

## 🔗 Quick Links

- [Sprint Taskboard](https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings)
- [Product Backlog](https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog)
- [GitHub Repository](https://github.com/Brave-Full-Stack/odoo/tree/Odoo-19.0-local-dev)
- [Sprint Dashboard](#)

## 👥 Team

| Role | Name | Azure DevOps |
|------|------|--------------|
| Product Owner | TBD | @mention |
| Scrum Master | TBD | @mention |
| Developer | TBD | @mention |

## 📊 Current Sprint

**Goal:** Complete General Settings configuration tracking  
**Work Items:** 225 (1 Epic, 42 User Stories, 181 Tasks)  
**Categories:** Apps, Users, Auth, Companies, Email, IoT, Integrations

## 📋 Work Item Categories

- 📱 **Apps & Modules** (3 stories, 24 tasks)
- 👥 **Users** (9 stories, 45 tasks)
- 🔐 **Authentication** (4 stories, 18 tasks)
- 🏢 **Companies** (3 stories, 12 tasks)
- 📧 **Email Communication** (8 stories, 32 tasks)
- 🤖 **IoT** (8 stories, 36 tasks)
- 🔌 **Integrations** (6 stories, 12 tasks)
- 🔧 **Developer Mode** (1 story, 2 tasks)

## 🎓 Resources

- [Azure DevOps Setup Scripts](../azure-devops-setup/README.md)
- [Board Configuration Guide](../azure-devops-setup/BOARD_CONFIGURATION_GUIDE.md)
- [Development Guidelines](#)
```

---

## 6. Team Configuration

### 👥 Team Settings

#### A. Team Profile

1. **Project Settings → Teams → Odoo-Dev Team**
2. Configure:
   - **Description:** "Development team for Odoo-19.0-local-dev General Settings"
   - **Team Administrator:** Set team admin
   - **Team members:** Add all team members

#### B. Capacity Planning

1. **Sprints → Capacity**
2. For each team member:
   - **Capacity per day:** 6 hours (accounting for meetings, etc.)
   - **Days off:** Mark holidays and vacations
   - **Activity:** Development, Testing, Review, etc.

**Example:**
```
Team Member A:
- Capacity: 6 hours/day
- Days off: Dec 30-31 (2 days)
- Activities: Development (80%), Code Review (20%)
```

#### C. Iteration Settings

**Already Configured:**
- ✅ Sprint: General settings
- ✅ Dates: Dec 27, 2025 - Jan 24, 2026
- ✅ Associated with team

**For Future Sprints:**
1. **Project Settings → Team configuration → Iterations**
2. Click **+ Select iteration(s)**
3. Choose from project iterations
4. Set default iteration for new work items

---

## 7. Notifications

### 🔔 Configure Alerts

#### A. Personal Notifications

1. **User Settings (top right) → Notifications**
2. Configure rules:

**Recommended Rules:**
- ✅ **Assigned to me** → Email + Web
- ✅ **Mentioned in discussion** → Email + Web
- ✅ **Pull request reviewer** → Email + Web
- ✅ **Build completion** → Web only
- ✅ **Work item updated** (my items) → Web only

#### B. Team Notifications

1. **Project Settings → Notifications**
2. Create team rules:

**Examples:**
- **Sprint starts** → Email to team
- **Sprint ends** → Email with burndown
- **High priority work item created** → Email to Scrum Master
- **Build fails** → Email to team
- **PR waiting for review** → Teams channel notification

#### C. Integration with Teams/Slack

**Microsoft Teams:**
1. **Project Settings → Service hooks**
2. **+ Create subscription**
3. Select **Microsoft Teams**
4. Choose events:
   - Work item created
   - PR created
   - Build completed
5. Configure Teams channel webhook

---

## 8. Security & Permissions

### 🔒 Access Control

#### A. Project-Level Permissions

**Project Settings → Permissions:**

**Recommended Roles:**
- **Project Administrators** → Full access
- **Contributors** → Most team members
  - Can create/edit work items
  - Can create branches and PRs
  - Can view builds and releases
- **Readers** → Stakeholders
  - View-only access to boards
  - Cannot modify work items

#### B. Area Path Permissions

**If using multiple areas:**
1. **Project Settings → Project configuration → Areas**
2. Create areas per category:
   - Apps & Modules
   - Users
   - IoT
   - etc.
3. Set permissions per area if needed

#### C. Branch Policies

**Already mentioned in Repos section, but critical for security:**
- ✅ Require PR for main branch
- ✅ Require code review
- ✅ Require build validation
- ✅ Restrict who can bypass policies

#### D. Secrets Management

**For Pipeline variables:**
1. **Library → Variable Groups**
2. Mark sensitive variables as **Secret**
3. Use Azure Key Vault for production secrets
4. Never commit secrets to code

---

## 9. Monitoring & Metrics

### 📈 Track Project Health

#### A. Key Metrics to Monitor

1. **Sprint Burndown**
   - Daily remaining work vs. ideal trend
   - Identify if sprint is on track

2. **Velocity**
   - Story points completed per sprint
   - Helps with future sprint planning

3. **Cycle Time**
   - Time from "In Progress" to "Done"
   - Identify bottlenecks

4. **Lead Time**
   - Time from "New" to "Done"
   - Overall process efficiency

5. **Work Item Age**
   - How long items stay in each column
   - Identify stale work

#### B. Quality Metrics

**If CI/CD configured:**
- Test coverage %
- Build success rate
- Deployment frequency
- Mean time to recovery (MTTR)

#### C. Custom Analytics

**Overview → Analytics:**
1. Create custom reports
2. Choose dimensions:
   - Work item type
   - State
   - Priority
   - Assigned to
   - Area path
3. Visualize trends over time

---

## 10. Best Practices Summary

### ✅ Daily Practices

**Morning Standup:**
1. Open Sprint Taskboard
2. Review yesterday's completed tasks
3. Discuss today's planned work
4. Identify blockers
5. Update remaining work

**During Development:**
1. Move tasks to "In Progress"
2. Link commits to work items (#taskid)
3. Update remaining work regularly
4. Create PRs with work item links
5. Review team members' PRs

**End of Day:**
1. Update task status
2. Mark blockers if any
3. Comment on progress in work items

### ✅ Sprint Practices

**Sprint Planning:**
1. Review velocity from previous sprints
2. Set sprint goal
3. Select User Stories from backlog
4. Break down into tasks
5. Estimate hours
6. Check team capacity

**Daily:**
1. Update taskboard
2. Review burndown chart
3. Adjust sprint if needed

**Sprint Review:**
1. Demo completed User Stories
2. Update dashboard
3. Archive completed work items
4. Document lessons learned

**Sprint Retrospective:**
1. What went well?
2. What didn't go well?
3. Action items for next sprint
4. Update team processes

### ✅ Code Quality Practices

1. **Branching Strategy:**
   ```
   main (Odoo-19.0-local-dev)
   ├── feature/user-story-381-apps-config
   ├── feature/user-story-384-user-management
   └── fix/bug-12345-auth-issue
   ```

2. **Commit Messages:**
   ```
   feat: Add OAuth Facebook integration #393
   fix: Correct user role assignment #387
   docs: Update API documentation #422
   test: Add unit tests for LDAP auth #396
   ```

3. **PR Requirements:**
   - Descriptive title
   - Link to User Story/Task
   - Screenshots/videos if UI changes
   - Test results
   - Reviewer assigned

---

## 📋 Quick Setup Checklist

Copy this checklist and track your setup progress:

### Boards
- [ ] Configure Stories board columns
- [ ] Set WIP limits
- [ ] Customize card fields
- [ ] Setup swimlanes
- [ ] Create quick filters
- [ ] Add styling rules

### Repos
- [ ] Connect GitHub repository
- [ ] Configure branch policies
- [ ] Enable work item linking
- [ ] Setup PR templates

### Pipelines
- [ ] Create CI pipeline
- [ ] Configure CD pipeline
- [ ] Setup variable groups
- [ ] Add service connections

### Dashboards
- [ ] Create sprint dashboard
- [ ] Add burndown widget
- [ ] Add velocity widget
- [ ] Add query widgets
- [ ] Add custom widgets

### Wiki
- [ ] Create wiki structure
- [ ] Write home page
- [ ] Add development guidelines
- [ ] Document deployment process

### Team
- [ ] Configure team settings
- [ ] Set team capacity
- [ ] Configure iterations
- [ ] Add team members

### Notifications
- [ ] Setup personal notifications
- [ ] Configure team notifications
- [ ] Integrate with Teams/Slack

### Security
- [ ] Review permissions
- [ ] Configure branch policies
- [ ] Setup secret management

---

## 🔗 Important URLs

**Boards:**
- Stories Board: https://dev.azure.com/Aries-Test/Odoo-Dev/_boards/board/t/Odoo-Dev%20Team/Stories
- Sprint Taskboard: https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings
- Backlog: https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog

**Project Settings:**
- Overview: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/
- Teams: https://dev.azure.com/Aries-Test/_settings/teams
- Permissions: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/permissions

**Queries:**
- All Queries: https://dev.azure.com/Aries-Test/Odoo-Dev/_queries

---

## 📞 Support & Resources

- **Azure DevOps Documentation:** https://learn.microsoft.com/en-us/azure/devops/
- **Odoo Development:** https://www.odoo.com/documentation/19.0/developer.html
- **Project Setup Scripts:** See `azure-devops-setup/` directory

---

**Document Version:** 1.0  
**Last Updated:** December 27, 2025  
**Status:** Ready for implementation  
**Next Review:** Start of next sprint
