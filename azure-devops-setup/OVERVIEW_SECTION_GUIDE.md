# Step-by-Step Guide: Azure DevOps Overview Section Management

## 📋 Odoo-Dev Project - Overview Section Setup

**Branch:** Odoo-19.0-local-dev  
**Project:** Odoo-Dev  
**Organization:** Aries-Test

---

## 🎯 Overview Section Components

The Overview section is the landing page for your Azure DevOps project and includes:
1. **Summary** - Project description and README
2. **Dashboards** - Visual metrics and KPIs
3. **Wiki** - Documentation and knowledge base
4. **Project Details** - Settings and metadata

---

## PART 1: PROJECT SUMMARY & DESCRIPTION

### Step 1.1: Access Project Settings

1. Navigate to Azure DevOps: https://dev.azure.com/Aries-Test/Odoo-Dev
2. Click **Project Settings** (gear icon at bottom left)
3. Select **Overview** from the left sidebar

### Step 1.2: Configure Project Description

1. In the **Project Settings → Overview** page:
   
2. **Project Name:** `Odoo-Dev` (already set)

3. **Description:** Click "Edit" and add:
   ```
   Odoo 19.0 Development Project - General Settings Configuration
   
   This project tracks the development and configuration of Odoo 19.0 
   General Settings including Apps & Modules, User Management, 
   Authentication, Companies, Email Communication, IoT, and Integrations.
   
   Branch: Odoo-19.0-local-dev
   Sprint: General settings (4 weeks)
   Work Items: 225 (1 Epic, 42 User Stories, 181 Tasks)
   ```

4. **Visibility:**
   - Private: Only team members can access
   - Public: Anyone in organization can view
   - *Recommended: Keep Private*

5. Click **Save**

### Step 1.3: Create Project README

1. Go to **Overview** tab (main navigation)

2. You'll see "Add a README to your project"

3. Click **Create README** or **Edit** if one exists

4. Add the following content:

```markdown
# Odoo-Dev Project

## 🎯 Project Overview

**Purpose:** Development and configuration tracking for Odoo 19.0 General Settings  
**Branch:** Odoo-19.0-local-dev  
**Repository:** [Brave-Full-Stack/odoo](https://github.com/Brave-Full-Stack/odoo/tree/Odoo-19.0-local-dev)

## 📊 Current Sprint

**Sprint Name:** General settings  
**Duration:** December 27, 2025 - January 24, 2026 (4 weeks)  
**Work Items:** 225 total
- 1 Epic: General Settings Configuration
- 42 User Stories (categorized)
- 181 Tasks

## 📋 Categories

| Category | User Stories | Tasks | Status |
|----------|--------------|-------|--------|
| 📱 Apps & Modules | 3 | 24 | In Progress |
| 👥 Users | 9 | 45 | In Progress |
| 🔐 Authentication | 4 | 18 | Not Started |
| 🏢 Companies | 3 | 12 | Not Started |
| 📧 Email Communication | 8 | 32 | Not Started |
| 🤖 IoT | 8 | 36 | Not Started |
| 🔌 Integrations | 6 | 12 | Not Started |
| 🔧 Developer Mode | 1 | 2 | Not Started |

## 🔗 Quick Links

### Boards
- [Sprint Taskboard](https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings)
- [Product Backlog](https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog)
- [Stories Board](https://dev.azure.com/Aries-Test/Odoo-Dev/_boards/board/t/Odoo-Dev%20Team/Stories)

### Reports
- [All Work Items Query](https://dev.azure.com/Aries-Test/Odoo-Dev/_queries?id=47ac2509-0257-4982-88f6-3b4186a3af3b)
- [Active Items Query](https://dev.azure.com/Aries-Test/Odoo-Dev/_queries?id=51eae97a-1342-460b-b730-d30ae8986079)

### Documentation
- [Project Wiki](https://dev.azure.com/Aries-Test/Odoo-Dev/_wiki)
- [Setup Scripts](https://github.com/Brave-Full-Stack/odoo/tree/Odoo-19.0-local-dev/azure-devops-setup)

## 👥 Team

| Role | Responsibility |
|------|----------------|
| Product Owner | Sprint planning, backlog prioritization |
| Scrum Master | Process facilitation, blocker removal |
| Developers | Implementation, code review |
| QA | Testing, quality assurance |

## 🎓 Getting Started

### For New Team Members

1. **Access:** Request access to Odoo-Dev project
2. **Setup:** Clone repository and setup development environment
3. **Board:** Review [Sprint Taskboard](https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings)
4. **Work Items:** Get assigned User Stories and Tasks
5. **Documentation:** Read [Setup Guide](https://github.com/Brave-Full-Stack/odoo/blob/Odoo-19.0-local-dev/azure-devops-setup/AZURE_DEVOPS_PROFESSIONAL_SETUP.md)

### Development Workflow

1. Pick task from sprint backlog
2. Create feature branch: `feature/user-story-XXX-description`
3. Commit with work item reference: `git commit -m "feat: description #taskid"`
4. Create Pull Request with work item link
5. Request code review
6. Merge after approval and CI pass

## 📈 Sprint Metrics

- **Velocity:** TBD (after first sprint)
- **Capacity:** TBD (configure in Capacity tab)
- **Burndown:** Track in [Sprint Dashboard](#)

## 📞 Support

- **Questions:** Post in team channel or @mention team members
- **Issues:** Create bug work items
- **Documentation:** Check [Wiki](https://dev.azure.com/Aries-Test/Odoo-Dev/_wiki)

---

*Last Updated: December 28, 2025*
```

5. Click **Save** (Ctrl+S)

---

## PART 2: DASHBOARDS SETUP

Dashboards provide visual insights into your project's health and progress.

### Step 2.1: Create Sprint Dashboard

1. Click **Overview** in main navigation
2. Select **Dashboards** tab
3. Click **+ New Dashboard**

**Dashboard Details:**
- **Name:** `General Settings Sprint Dashboard`
- **Team:** Odoo-Dev Team
- **Description:** `Real-time sprint tracking and metrics for General Settings sprint`

4. Click **Create**

### Step 2.2: Add Sprint Burndown Widget

1. In the dashboard, click **Edit** (pencil icon)
2. Click **+ Add Widget**
3. Search for "Sprint Burndown"
4. Click **Add** on "Sprint Burndown" widget

**Configure Widget:**
- **Name:** Sprint Burndown
- **Size:** 2 x 2
- **Sprint:** General settings
- Click **Save**

5. Drag widget to desired position

### Step 2.3: Add Sprint Capacity Widget

1. Click **+ Add Widget**
2. Search for "Sprint Capacity"
3. Click **Add**

**Configure:**
- **Name:** Team Capacity
- **Size:** 1 x 1
- **Sprint:** General settings
- Click **Save**

### Step 2.4: Add Work Items Query Widget

1. Click **+ Add Widget**
2. Search for "Query Results"
3. Click **Add**

**Configure:**
- **Name:** Active User Stories
- **Size:** 2 x 2
- **Query:** [General settings] User Stories
- Click **Save**

4. Repeat for other queries:
   - Active Tasks
   - Completed Items
   - Unassigned Items

### Step 2.5: Add Cumulative Flow Diagram

1. Click **+ Add Widget**
2. Search for "Cumulative Flow Diagram"
3. Click **Add**

**Configure:**
- **Name:** CFD - Work Distribution
- **Size:** 2 x 2
- **Team:** Odoo-Dev Team
- **Backlog Level:** Stories
- Click **Save**

### Step 2.6: Add Velocity Widget

1. Click **+ Add Widget**
2. Search for "Velocity"
3. Click **Add**

**Configure:**
- **Name:** Team Velocity
- **Size:** 2 x 1
- **Team:** Odoo-Dev Team
- **Iterations:** Last 6 sprints
- Click **Save**

### Step 2.7: Add Markdown Widget (Sprint Goal)

1. Click **+ Add Widget**
2. Search for "Markdown"
3. Click **Add**

**Configure with this content:**
```markdown
## 🎯 Sprint Goal

**Complete General Settings Configuration Tracking System**

### Objectives:
- ✅ Setup Apps & Modules management
- ✅ Configure User Management system
- ✅ Implement Authentication methods
- ✅ Setup Company configuration
- ✅ Configure Email communication
- ✅ Integrate IoT devices
- ✅ Setup external integrations
- ✅ Enable Developer Mode features

### Success Criteria:
- All 225 work items completed
- User acceptance testing passed
- Documentation updated
- Code reviewed and merged

---
**Sprint:** Dec 27, 2025 - Jan 24, 2026 | **Team:** Odoo-Dev
```

**Settings:**
- **Name:** Sprint Goal
- **Size:** 2 x 1
- Click **Save**

### Step 2.8: Add Team Members Widget

1. Click **+ Add Widget**
2. Search for "Team Members"
3. Click **Add**

**Configure:**
- **Name:** Team Members
- **Size:** 1 x 1
- **Team:** Odoo-Dev Team
- Click **Save**

### Step 2.9: Arrange Dashboard Layout

Recommended layout (drag widgets to arrange):

```
┌─────────────────────────────────────────────────┐
│  Sprint Goal              │ Team Members        │
│  (2x1)                    │ (1x1)              │
├─────────────────────────────────────────────────┤
│  Sprint Burndown          │ Capacity            │
│  (2x2)                    │ (1x1)              │
│                           ├──────────────────────┤
│                           │ Velocity            │
│                           │ (1x1)              │
├─────────────────────────────────────────────────┤
│  Active User Stories      │ Active Tasks        │
│  (2x2)                    │ (2x2)              │
├─────────────────────────────────────────────────┤
│  Cumulative Flow Diagram  │ Completed Items     │
│  (2x2)                    │ (2x2)              │
└─────────────────────────────────────────────────┘
```

10. Click **Done Editing**

### Step 2.10: Set as Default Dashboard

1. Click dashboard dropdown (top)
2. Click **⋮** (More actions)
3. Select **Set as team dashboard**
4. Now team members see this when they click Overview

### Step 2.11: Create Additional Dashboards (Optional)

**Quality Dashboard:**
- Code coverage
- Build success rate
- Bug trends
- Test results

**Velocity Dashboard:**
- Historical velocity
- Story point trends
- Capacity planning
- Team performance

---

## PART 3: WIKI SETUP

The Wiki is your project's knowledge base.

### Step 3.1: Create Project Wiki

1. Click **Overview** → **Wiki**
2. Click **Create project wiki**
3. Enter wiki name: `Odoo-Dev Wiki`
4. Click **Create**

### Step 3.2: Create Home Page

The home page is automatically created. Edit it:

1. Click **Edit page** (pencil icon)

2. Replace content with:

```markdown
# Welcome to Odoo-Dev Project Wiki

## 📖 Documentation Hub

This wiki contains all documentation for the Odoo 19.0 General Settings development project.

---

## 🚀 Quick Navigation

### 👋 Getting Started
- [Project Overview](#project-overview)
- [Team Onboarding](Team-Onboarding)
- [Development Setup](Development-Setup)
- [Git Workflow](Git-Workflow)

### 📋 Work Management
- [Sprint Planning](Sprint-Planning)
- [Work Item Guidelines](Work-Item-Guidelines)
- [Definition of Done](Definition-of-Done)

### 🔧 Development
- [Coding Standards](Coding-Standards)
- [Testing Guidelines](Testing-Guidelines)
- [Code Review Process](Code-Review-Process)
- [Deployment Process](Deployment-Process)

### 📊 Reporting
- [Sprint Reports](Sprint-Reports)
- [Metrics & KPIs](Metrics-and-KPIs)

---

## 🎯 Project Overview

**Branch:** Odoo-19.0-local-dev  
**Sprint:** General settings (4 weeks)  
**Timeline:** December 27, 2025 - January 24, 2026

### Categories

- 📱 **Apps & Modules** - Application installation and configuration
- 👥 **Users** - User management and permissions
- 🔐 **Authentication** - OAuth and LDAP integration
- 🏢 **Companies** - Multi-company setup
- 📧 **Email Communication** - Email server and templates
- 🤖 **IoT** - IoT device integration
- 🔌 **Integrations** - External service integrations
- 🔧 **Developer Mode** - Developer tools

---

## 👥 Team

| Role | Contact | Responsibilities |
|------|---------|-----------------|
| Product Owner | @mention | Backlog management, prioritization |
| Scrum Master | @mention | Process facilitation |
| Tech Lead | @mention | Architecture, technical decisions |
| Developers | @mention | Implementation |
| QA Lead | @mention | Quality assurance |

---

## 🔗 Important Links

- [Sprint Taskboard](https://dev.azure.com/Aries-Test/Odoo-Dev/_sprints/taskboard/General%20settings)
- [Product Backlog](https://dev.azure.com/Aries-Test/Odoo-Dev/_backlogs/backlog)
- [GitHub Repository](https://github.com/Brave-Full-Stack/odoo/tree/Odoo-19.0-local-dev)
- [Sprint Dashboard](#)

---

## 📝 Recent Updates

- ✅ Dec 27, 2025: Sprint created and configured
- ✅ Dec 27, 2025: 225 work items imported
- ✅ Dec 27, 2025: User Stories categorized
- ✅ Dec 27, 2025: Taskboard activated

---

*For questions or suggestions, contact the Scrum Master or post in team channel.*
```

3. Click **Save** (Ctrl+S)

### Step 3.3: Create Page Structure

Create the following pages (click **+ New page** for each):

#### 3.3.1 Team Onboarding Page

**Page Name:** `Team-Onboarding`  
**Parent:** Home

**Content:**
```markdown
# Team Onboarding

## Welcome to Odoo-Dev Team! 🎉

### Step 1: Access Setup

1. **Azure DevOps Access**
   - Confirm access to Odoo-Dev project
   - Join Odoo-Dev Team
   - Setup notifications

2. **GitHub Access**
   - Fork/clone repository: Brave-Full-Stack/odoo
   - Checkout branch: Odoo-19.0-local-dev
   - Setup SSH keys

3. **Communication**
   - Join team channels (Teams/Slack)
   - Subscribe to project notifications

### Step 2: Development Environment

1. Clone repository:
   ```bash
   git clone git@github.com:Brave-Full-Stack/odoo.git
   cd odoo
   git checkout Odoo-19.0-local-dev
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup local database:
   ```bash
   # Follow README-LOCAL-SETUP.md
   ```

4. Run Odoo:
   ```bash
   ./odoo-bin --config odoo.conf
   ```

### Step 3: Azure DevOps Orientation

1. **Boards**
   - Review [Sprint Taskboard](#)
   - Understand work item types
   - Learn card workflow

2. **Work Items**
   - Get assigned User Stories
   - Break down into tasks
   - Update remaining work daily

3. **Process**
   - Daily standup routine
   - Sprint planning participation
   - Retrospective contribution

### Step 4: First Task

1. Get assigned a task from sprint backlog
2. Create feature branch
3. Implement and test
4. Create Pull Request
5. Get code review
6. Merge after approval

### Resources

- [Coding Standards](Coding-Standards)
- [Git Workflow](Git-Workflow)
- [Testing Guidelines](Testing-Guidelines)

---

*Questions? Ask your buddy or Scrum Master!*
```

#### 3.3.2 Sprint Planning Page

**Page Name:** `Sprint-Planning`  
**Parent:** Home

**Content:**
```markdown
# Sprint Planning Guide

## Sprint Planning Process

### Before Sprint Planning

**Product Owner:**
- Review and prioritize product backlog
- Ensure User Stories have acceptance criteria
- Prepare sprint goal

**Team:**
- Review previous sprint retrospective actions
- Update team capacity

### Sprint Planning Meeting

**Duration:** 2-4 hours  
**Attendees:** Entire Scrum Team

#### Part 1: What (60 minutes)

1. **Product Owner presents sprint goal**
2. **Review top priority User Stories**
   - Discuss requirements
   - Clarify acceptance criteria
   - Identify dependencies

3. **Team asks questions**
4. **Team commits to stories for sprint**

#### Part 2: How (90 minutes)

1. **Break down User Stories into Tasks**
   - Each task < 8 hours
   - Assign to team members
   - Estimate remaining work

2. **Verify capacity**
   - Check team availability
   - Adjust sprint scope if needed

3. **Finalize sprint backlog**

### Sprint Planning Checklist

- [ ] Sprint goal defined
- [ ] User Stories selected
- [ ] Acceptance criteria clear
- [ ] Tasks created and estimated
- [ ] Team capacity verified
- [ ] Dependencies identified
- [ ] Sprint backlog finalized

### Current Sprint

**Goal:** Complete General Settings Configuration Tracking System  
**Duration:** Dec 27, 2025 - Jan 24, 2026  
**Capacity:** [Update in Capacity tab]

### Sprint Backlog

View current sprint work items:
- [Sprint Taskboard](#)
- [Sprint Backlog](#)

---

*Next Sprint Planning: [Date TBD]*
```

#### 3.3.3 Work Item Guidelines Page

**Page Name:** `Work-Item-Guidelines`  
**Parent:** Home

**Content:**
```markdown
# Work Item Guidelines

## Work Item Types

### Epic
- High-level business objective
- Contains multiple User Stories
- Tracks overall progress

### User Story
- User-focused requirement
- Format: "As a [user], I want [goal], so that [benefit]"
- Has acceptance criteria
- Estimated in story points

### Task
- Technical work item
- Supports a User Story
- Estimated in hours
- Assigned to specific developer

### Bug
- Defect in existing functionality
- Has reproduction steps
- Includes severity and priority

## Creating Work Items

### User Story Template

**Title Format:** `[Category] - [Brief Description]`  
Example: `[Users] - Two-Factor Authentication`

**Description:**
```
As a [user type]
I want [goal]
So that [benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Technical Notes:
[Any technical considerations]

Dependencies:
- Related to #XXX
```

**Fields to Fill:**
- **Iteration:** General settings
- **Area Path:** Odoo-Dev
- **Priority:** 1 (Critical) - 4 (Low)
- **Story Points:** 1, 2, 3, 5, 8, 13
- **Tags:** Category tag (Apps & Modules, Users, etc.)
- **Assigned To:** Team member

### Task Template

**Title Format:** `[Action] [Component/Feature]`  
Example: `Implement OAuth token validation`

**Description:**
```
Detailed description of work to be done.

Technical Approach:
1. Step 1
2. Step 2
3. Step 3

Acceptance Criteria:
- [ ] Code implemented
- [ ] Unit tests added
- [ ] Code reviewed
```

**Fields:**
- **Original Estimate:** Hours (e.g., 4)
- **Remaining Work:** Update daily
- **Parent:** Link to User Story
- **Assigned To:** Developer

## Work Item Workflow

### User Story States
1. **New** - Just created, not refined
2. **Active** - In current sprint, being worked on
3. **Resolved** - Development complete, in testing
4. **Closed** - Accepted and deployed

### Task States
1. **To Do** - Not started
2. **In Progress** - Currently being worked on
3. **Done** - Completed

## Best Practices

### Naming
- ✅ Clear and descriptive
- ✅ Starts with action verb (for tasks)
- ✅ Includes category prefix (for stories)
- ❌ Vague or ambiguous
- ❌ Too long (> 100 characters)

### Descriptions
- ✅ Includes acceptance criteria
- ✅ Links related work items
- ✅ Provides context
- ❌ Empty or minimal
- ❌ Assumes knowledge

### Updates
- ✅ Update remaining work daily
- ✅ Add comments on progress
- ✅ Link commits (#taskid)
- ✅ Attach screenshots if relevant
- ❌ Leave stale for days

### Linking
- ✅ Link tasks to parent story
- ✅ Reference related items
- ✅ Note dependencies
- ✅ Link commits and PRs

## Work Item Commands

In commit messages:
- `Fixes #123` - Closes work item on merge
- `Resolves #123` - Closes work item
- `Related to #123` - Links without closing
- `#123` - Simple link

---

*Follow these guidelines for consistent work item management.*
```

#### 3.3.4 Definition of Done

**Page Name:** `Definition-of-Done`  
**Parent:** Home

**Content:**
```markdown
# Definition of Done

## User Story Definition of Done

A User Story is considered "Done" when:

### Development
- [ ] All tasks completed
- [ ] Code implemented according to design
- [ ] Code follows coding standards
- [ ] No TODO or FIXME comments in production code
- [ ] All acceptance criteria met

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] Manual testing completed
- [ ] Edge cases tested
- [ ] No critical or high priority bugs

### Code Review
- [ ] Pull Request created and linked
- [ ] Code reviewed by at least 1 team member
- [ ] All review comments addressed
- [ ] Code approved by reviewer
- [ ] CI build passing

### Documentation
- [ ] Code comments added for complex logic
- [ ] README updated if needed
- [ ] Wiki updated if needed
- [ ] API documentation updated (if applicable)

### Deployment
- [ ] Merged to main branch
- [ ] Deployed to development environment
- [ ] Smoke testing passed
- [ ] Product Owner acceptance

## Task Definition of Done

A Task is considered "Done" when:

- [ ] Implementation complete
- [ ] Self-reviewed
- [ ] Unit tests added/updated
- [ ] Tests passing locally
- [ ] Committed with work item reference
- [ ] Remaining work set to 0

## Sprint Definition of Done

A Sprint is considered "Done" when:

- [ ] All committed User Stories meet DoD
- [ ] Sprint goal achieved
- [ ] No critical bugs in sprint scope
- [ ] Documentation updated
- [ ] Demo prepared
- [ ] Retrospective completed

## Checklist Usage

### For Developers
Before moving task to "Done":
1. Review task DoD checklist
2. Verify all items checked
3. Update work item state
4. Add completion comment

### For Code Reviewers
Before approving PR:
1. Verify story DoD items
2. Check tests and coverage
3. Validate documentation
4. Approve if all criteria met

### For Product Owner
Before accepting story:
1. Review acceptance criteria
2. Verify in demo environment
3. Check documentation
4. Accept or provide feedback

---

*The Definition of Done ensures consistent quality across all deliverables.*
```

### Step 3.4: Create Additional Pages

Create these pages as needed:
- `Development-Setup` - Local environment setup
- `Git-Workflow` - Branching and commit strategy
- `Coding-Standards` - Code style guidelines
- `Testing-Guidelines` - Test requirements
- `Code-Review-Process` - Review procedures
- `Deployment-Process` - Deployment steps
- `Metrics-and-KPIs` - Project metrics

### Step 3.5: Configure Wiki Settings

1. Click **⋮** (More actions) → **Wiki settings**
2. Configure:
   - **Permissions:** Control who can edit
   - **Page versions:** Enable version history
   - **Templates:** Create page templates

---

## PART 4: PROJECT DETAILS & METADATA

### Step 4.1: Update Project Icon

1. Go to **Project Settings → Overview**
2. Click on the project icon (circle with initials)
3. **Upload image** (PNG, JPG, max 2MB)
   - Use Odoo logo or custom icon
   - Recommended: 256x256px
4. Click **Save**

### Step 4.2: Configure Project Tags

1. **Project Settings → Overview**
2. **Tags section**
3. Add relevant tags:
   - `odoo`
   - `general-settings`
   - `configuration`
   - `sprint`
   - `microservices`

Tags help with organization-wide searching.

### Step 4.3: Set Project Process Template

1. **Project Settings → Overview**
2. **Process:** Should show "Agile" or "Scrum"
3. If not set correctly, contact Azure DevOps admin

### Step 4.4: Configure Team Settings

1. **Project Settings → Teams**
2. Select **Odoo-Dev Team**
3. Configure:
   - **Default area path:** Odoo-Dev
   - **Default iteration:** General settings
   - **Backlog navigation levels:** Stories
   - **Working days:** Monday-Friday

---

## PART 5: OVERVIEW TAB CUSTOMIZATION

### Step 5.1: Pin Important Items

You can pin items to Overview for quick access:

1. Navigate to a query, dashboard, or wiki page
2. Click **⋮** (More options)
3. Select **Add to Overview**
4. Items appear in "Pinned" section

**Recommended Pins:**
- Sprint Taskboard
- Active Items query
- Sprint Dashboard
- Team wiki home

### Step 5.2: Configure Team Welcome Message

1. Go to **Overview**
2. If there's a welcome section, click **Edit**
3. Add team message:

```
Welcome to Odoo-Dev! 

Quick Links:
• Sprint Taskboard: [link]
• Sprint Dashboard: [link]  
• Wiki: [link]

Current Sprint: General settings (4 weeks)
Sprint Goal: Complete General Settings Configuration Tracking

For help, contact your Scrum Master or @mention in team channel.
```

---

## PART 6: OVERVIEW BEST PRACTICES

### Daily Usage

**Morning:**
1. Check Overview for dashboard updates
2. Review pinned items
3. Check team announcements

**During Work:**
1. Reference wiki for guidelines
2. Monitor dashboard widgets
3. Track sprint progress

**End of Day:**
1. Update work items
2. Check dashboard for blockers
3. Review tomorrow's tasks

### Maintenance

**Weekly:**
- Update project README if major changes
- Review dashboard for outdated widgets
- Update wiki pages as needed

**Sprint End:**
- Update sprint metrics in README
- Archive completed sprint documentation
- Prepare for next sprint

**Monthly:**
- Review and update project description
- Audit wiki for outdated content
- Update team roster if changed

---

## 📋 OVERVIEW SETUP CHECKLIST

Copy this checklist to track your setup:

### Project Summary
- [ ] Project description updated
- [ ] Project README created and formatted
- [ ] Project icon uploaded
- [ ] Project tags added
- [ ] Visibility settings configured

### Dashboards
- [ ] Sprint dashboard created
- [ ] Sprint burndown widget added
- [ ] Capacity widget added
- [ ] Query result widgets added
- [ ] CFD widget added
- [ ] Velocity widget added
- [ ] Sprint goal widget added
- [ ] Team members widget added
- [ ] Dashboard layout arranged
- [ ] Set as default team dashboard

### Wiki
- [ ] Project wiki created
- [ ] Home page content updated
- [ ] Team Onboarding page created
- [ ] Sprint Planning page created
- [ ] Work Item Guidelines page created
- [ ] Definition of Done page created
- [ ] Development Setup page created
- [ ] Git Workflow page created
- [ ] Additional pages created as needed
- [ ] Wiki permissions configured

### Overview Tab
- [ ] Important items pinned
- [ ] Welcome message added
- [ ] Quick links verified
- [ ] Team settings configured

---

## 🎯 FINAL VERIFICATION

After completing all steps, verify:

1. **Navigate to Overview tab**
   - README displays correctly
   - Pinned items accessible
   - Welcome message visible

2. **Open Dashboards**
   - All widgets loading
   - Data displaying correctly
   - Dashboard is default for team

3. **Browse Wiki**
   - All pages accessible
   - Navigation works
   - Content formatted properly

4. **Check Project Settings**
   - Description accurate
   - Icon displays
   - Tags appropriate
   - Team settings correct

---

## 🔗 QUICK REFERENCE

### URLs
- **Overview:** https://dev.azure.com/Aries-Test/Odoo-Dev/_dashboards
- **Dashboards:** https://dev.azure.com/Aries-Test/Odoo-Dev/_dashboards
- **Wiki:** https://dev.azure.com/Aries-Test/Odoo-Dev/_wiki
- **Project Settings:** https://dev.azure.com/Aries-Test/Odoo-Dev/_settings

### Keyboard Shortcuts
- `?` - Show keyboard shortcuts
- `g + h` - Go to project home
- `g + w` - Go to wiki
- `g + d` - Go to dashboards

---

## 📞 Support

If you encounter issues:
1. Check Azure DevOps documentation
2. Contact your Azure DevOps administrator
3. Refer to [AZURE_DEVOPS_PROFESSIONAL_SETUP.md](AZURE_DEVOPS_PROFESSIONAL_SETUP.md)

---

**Document Version:** 1.0  
**Last Updated:** December 28, 2025  
**Status:** Ready to implement  
**Completion Time:** ~2-3 hours for full setup
