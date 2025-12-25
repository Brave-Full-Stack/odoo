# 🎯 Azure Boards Configuration Guide - Step-by-Step

This guide will help you organize your 298 imported work items using the structure from CHECKLIST.md with Epics, User Stories, and Tasks per phase.

---

## 📋 Table of Contents

1. [Create Epics for Each Phase](#step-1-create-epics-for-each-phase)
2. [Create User Stories (Feature Groups)](#step-2-create-user-stories-feature-groups)
3. [Link Tasks to User Stories](#step-3-link-tasks-to-user-stories)
4. [Configure Board Columns](#step-4-configure-board-columns)
5. [Create Custom Queries](#step-5-create-custom-queries)
6. [Set Up Sprint Planning](#step-6-set-up-sprint-planning)
7. [Configure Dashboards](#step-7-configure-dashboards)
8. [Enable Dependencies Visualization](#step-8-enable-dependencies-visualization)

---

## Step 1: Create Epics for Each Phase

### Why Epics?
Epics represent major phases of work. Each phase in your CHECKLIST.md will become an Epic.

### 1.1 Navigate to Work Items
1. Open Azure DevOps: https://dev.azure.com/Aries-Test/Odoo-Microservices
2. Click **Boards** → **Work items**
3. Click **+ New Work Item** → Select **Epic**

### 1.2 Create Phase 0 Epic
Fill in the details:
- **Title:** `Phase 0: Microservices Design (Days 1-5)`
- **Description:**
  ```
  ## Phase 0: Microservices Design
  
  Design and architecture phase for Odoo microservices system.
  
  ### Objectives:
  - Domain-Driven Design
  - Database Per Service Pattern
  - Inter-Service Communication
  - Service Directory Structure
  - Define Service APIs
  - Service Dependencies Matrix
  
  ### Duration: 5 days
  ### Deliverables: Complete architecture documentation and service boundaries
  ```
- **Priority:** 1
- **Tags:** `Phase-0`, `Design`, `Architecture`
- **Iteration:** Sprint 1
- Click **Save & Close**

### 1.3 Create Remaining Epics
Repeat for all phases with these titles:

| Epic | Title | Tags | Sprint |
|------|-------|------|--------|
| **Phase 0** | Phase 0: Microservices Design (Days 1-5) | Phase-0, Design, Architecture | Sprint 1 |
| **Phase 1** | Phase 1: Service Mesh Setup (Days 6-10) | Phase-1, Istio, Infrastructure | Sprint 1 |
| **Phase 2** | Phase 2: Core Services Development (Days 11-18) | Phase-2, Development, MVP | Sprint 2 |
| **Phase 3** | Phase 3: Event Bus & Messaging (Days 19-22) | Phase-3, Messaging, RabbitMQ | Sprint 3 |
| **Phase 4** | Phase 4: Observability Stack (Days 23-26) | Phase-4, Monitoring, Logging | Sprint 3 |
| **Phase 5** | Phase 5: API Gateway & Security (Days 27-30) | Phase-5, Gateway, Security | Sprint 4 |
| **Phase 6** | Phase 6: Container Registry (Days 31-32) | Phase-6, Harbor, Registry | Sprint 4 |
| **Phase 7** | Phase 7: GitOps with ArgoCD (Days 33-35) | Phase-7, GitOps, ArgoCD | Sprint 5 |
| **Phase 8** | Phase 8: CI/CD Pipeline (Days 36-38) | Phase-8, CICD, Automation | Sprint 5 |
| **Phase 9** | Phase 9: Cloud Infrastructure (Days 39-45) | Phase-9, AWS, Production | Sprint 6 |

**Quick Tip:** Open each Epic and note its ID (e.g., Epic #299, #300, etc.) - you'll need these for linking.

---

## Step 2: Create User Stories (Feature Groups)

### Why User Stories?
User Stories represent feature groups within each phase. Each section (0.1, 0.2, etc.) from CHECKLIST.md becomes a User Story.

### 2.1 Navigate to Backlogs
1. Click **Boards** → **Backlogs**
2. You should see your Epics on the left

### 2.2 Create User Stories for Phase 0

Click **+ New Work Item** → Select **User Story**

#### User Story 1: Domain-Driven Design
- **Title:** `0.1 Domain-Driven Design`
- **Description:**
  ```
  As an architect, I need to define service boundaries using domain-driven design principles.
  
  ### Tasks:
  - Document 11 microservices
  - Create service boundary diagram
  - Define service responsibilities
  ```
- **Parent Link:** Link to "Phase 0: Microservices Design" Epic (use the Epic ID)
- **Priority:** 1
- **Tags:** `Phase-0`, `0.1`, `Design`
- **Story Points:** 3
- Click **Save & Close**

#### User Story 2: Database Per Service Pattern
- **Title:** `0.2 Database Per Service Pattern`
- **Description:**
  ```
  As an architect, I need to design database schemas for each microservice following the database-per-service pattern.
  
  ### Tasks:
  - Design auth-db schema
  - Design core-erp-db schema
  - Design accounting-db schema
  - Design inventory-db schema
  - Design crm-db schema
  ```
- **Parent Link:** Link to "Phase 0" Epic
- **Priority:** 1
- **Tags:** `Phase-0`, `0.2`, `Database`
- **Story Points:** 5
- Click **Save & Close**

#### Continue for all Phase 0 User Stories:
- `0.3 Inter-Service Communication` (Story Points: 3)
- `0.4 Service Directory Structure` (Story Points: 2)
- `0.5 Define Service APIs` (Story Points: 5)
- `0.6 Service Dependencies Matrix` (Story Points: 3)

### 2.3 Create User Stories for Phase 1

#### Phase 1 User Stories:
- `1.1 Install Istio` (Story Points: 3)
- `1.2 Install Kiali Dashboard` (Story Points: 3)
- `1.3 Configure Traffic Management` (Story Points: 5)
- `1.4 Configure Resilience` (Story Points: 3)
- `1.5 mTLS Configuration` (Story Points: 3)
- `1.6 Service Mesh Testing` (Story Points: 2)

### 2.4 Complete User Stories for All Phases

Use this reference for remaining phases:

<details>
<summary><strong>Phase 2 User Stories (Click to expand)</strong></summary>

- `2.1 Auth Service` (Story Points: 8)
- `2.2 Core ERP Service` (Story Points: 8)
- `2.3 Accounting Service` (Story Points: 8)
- `2.4 Inventory Service` (Story Points: 8)
- `2.5 CRM Service` (Story Points: 8)

</details>

<details>
<summary><strong>Phase 3 User Stories (Click to expand)</strong></summary>

- `3.1 RabbitMQ Installation` (Story Points: 3)
- `3.2 Event Schema Definition` (Story Points: 3)
- `3.3 Event Publishers` (Story Points: 5)
- `3.4 Event Consumers` (Story Points: 5)
- `3.5 Event Testing` (Story Points: 2)

</details>

<details>
<summary><strong>Phase 4 User Stories (Click to expand)</strong></summary>

- `4.1 Prometheus Setup` (Story Points: 3)
- `4.2 Grafana Dashboards` (Story Points: 5)
- `4.3 Jaeger Tracing` (Story Points: 3)
- `4.4 OpenTelemetry Integration` (Story Points: 5)
- `4.5 EFK Stack` (Story Points: 5)

</details>

<details>
<summary><strong>Phase 5 User Stories (Click to expand)</strong></summary>

- `5.1 Kong Installation` (Story Points: 3)
- `5.2 OAuth2 Plugin` (Story Points: 3)
- `5.3 Rate Limiting` (Story Points: 3)
- `5.4 CORS Configuration` (Story Points: 2)
- `5.5 API Documentation` (Story Points: 3)
- `5.6 Load Testing` (Story Points: 3)

</details>

<details>
<summary><strong>Phase 6 User Stories (Click to expand)</strong></summary>

- `6.1 Harbor Installation` (Story Points: 3)
- `6.2 Vulnerability Scanning` (Story Points: 3)
- `6.3 Image Replication` (Story Points: 3)
- `6.4 Push Service Images` (Story Points: 5)

</details>

<details>
<summary><strong>Phase 7 User Stories (Click to expand)</strong></summary>

- `7.1 ArgoCD Installation` (Story Points: 3)
- `7.2 Repository Structure` (Story Points: 2)
- `7.3 Application Definitions` (Story Points: 5)
- `7.4 Sync Policies` (Story Points: 2)
- `7.5 Multi-Environment` (Story Points: 3)

</details>

<details>
<summary><strong>Phase 8 User Stories (Click to expand)</strong></summary>

- `8.1 GitHub Actions - Build` (Story Points: 3)
- `8.2 GitHub Actions - Test` (Story Points: 3)
- `8.3 Security Scanning` (Story Points: 3)
- `8.4 Docker Build & Push` (Story Points: 3)
- `8.5 ArgoCD Sync` (Story Points: 3)
- `8.6 Rollback Strategy` (Story Points: 2)

</details>

<details>
<summary><strong>Phase 9 User Stories (Click to expand)</strong></summary>

- `9.1 AWS Account Setup` (Story Points: 2)
- `9.2 Terraform VPC` (Story Points: 5)
- `9.3 EKS Cluster` (Story Points: 5)
- `9.4 RDS PostgreSQL` (Story Points: 5)
- `9.5 ElastiCache Redis` (Story Points: 3)
- `9.6 S3 Buckets` (Story Points: 2)
- `9.7 ALB Load Balancer` (Story Points: 3)
- `9.8 Route53 DNS` (Story Points: 2)
- `9.9 Deploy to EKS` (Story Points: 5)
- `9.10 Production Testing` (Story Points: 3)

</details>

<details>
<summary><strong>Additional Phases User Stories (Click to expand)</strong></summary>

**Testing Phase:**
- `T.1 Unit Tests - All Services` (Story Points: 8)
- `T.2 Integration Tests` (Story Points: 5)
- `T.3 E2E Testing` (Story Points: 5)
- `T.4 Performance Testing` (Story Points: 3)
- `T.5 Security Testing` (Story Points: 3)

**Final Validation:**
- `FV Final Validation` (Story Points: 8)

**Additional Services:**
- `A.1 HR Service` (Story Points: 8)
- `A.2 Sales Service` (Story Points: 8)
- `A.3 Reporting Service` (Story Points: 8)
- `A.4 Notification Service` (Story Points: 8)
- `A.5 File Storage Service` (Story Points: 8)
- `A.6 Workflow Service` (Story Points: 8)

</details>

---

## Step 3: Link Tasks to User Stories

Now you'll link the 298 imported tasks to their respective User Stories.

### 3.1 Use Bulk Edit for Efficiency

1. Go to **Boards** → **Work Items**
2. Create a filter:
   - **Work Item Type** = `Task`
   - **Tags** `Contains` `Phase-0`
3. Select all Phase 0 tasks

### 3.2 Link Tasks to User Story 0.1

**Filter for tasks 0.1.x:**
1. Add filter: **Title** `Contains` `0.1.`
2. Results should show:
   - `0.1.1 - Documented 11 microservices`
   - `0.1.2 - Created service boundary diagram`
   - `0.1.3 - Defined service responsibilities`

3. Select all three tasks (Ctrl+Click)
4. Click **⋯** (More actions) → **Change parent**
5. Search for User Story: `0.1 Domain-Driven Design`
6. Click **Save**

### 3.3 Repeat for All User Stories

Use these filters to link tasks efficiently:

| User Story | Filter | Task IDs |
|------------|--------|----------|
| 0.1 Domain-Driven Design | Title Contains "0.1." | 0.1.1 - 0.1.3 |
| 0.2 Database Per Service | Title Contains "0.2." | 0.2.1 - 0.2.5 |
| 0.3 Inter-Service Communication | Title Contains "0.3." | 0.3.1 - 0.3.3 |
| 0.4 Service Directory Structure | Title Contains "0.4." | 0.4.1 - 0.4.3 |
| 0.5 Define Service APIs | Title Contains "0.5." | 0.5.1 - 0.5.5 |
| 0.6 Service Dependencies Matrix | Title Contains "0.6." | 0.6.1 - 0.6.5 |

**Continue this pattern for all phases 1-9, T, FV, and A.**

### 3.4 Automated Linking Script (Optional)

If manual linking is too time-consuming, I can create a Python script to automatically link all tasks to their user stories based on task ID patterns.

---

## Step 4: Configure Board Columns

### 4.1 Navigate to Board Settings
1. Go to **Boards** → **Boards**
2. Click **⚙️ Board settings** (top right)
3. Select **Columns** tab

### 4.2 Configure Columns

Set up these columns to match your workflow:

| Column Name | States | WIP Limit |
|-------------|--------|-----------|
| **To Do** | New | - |
| **In Progress** | Active | 5 |
| **Review** | Active | 3 |
| **Done** | Closed, Removed | - |

### 4.3 Map States to Columns

1. **To Do Column:**
   - Drag "New" state into this column
   
2. **In Progress Column:**
   - Drag "Active" state into this column
   - Set WIP limit: 5 (helps focus)

3. **Review Column** (Optional):
   - Also uses "Active" state
   - Set WIP limit: 3
   - Use for tasks awaiting testing/review

4. **Done Column:**
   - Drag "Closed" state
   - Drag "Removed" state

5. Click **Save and close**

### 4.4 Customize Swimlanes (Optional)

1. Click **⚙️ Board settings** → **Swimlanes**
2. Add swimlanes by:
   - **Epics** (recommended for phase separation)
   - **People** (good for team collaboration)
   - **Stories** (detailed view)

---

## Step 5: Create Custom Queries

### 5.1 Query: Tasks by Phase

1. Go to **Boards** → **Queries**
2. Click **+ New query**
3. Configure:
   ```
   Work Item Type = Task
   Tags Contains Phase-0
   ```
4. **Save query** as: `Phase 0 Tasks`
5. **Folder:** Shared Queries → Microservices

Repeat for Phase-1 through Phase-9, Testing, Final Validation, and Additional Services.

### 5.2 Query: Current Sprint Tasks

1. Click **+ New query**
2. Configure:
   ```
   Work Item Type = Task
   Iteration Path = @CurrentIteration
   State <> Closed
   ```
3. **Save as:** `Current Sprint - Active Tasks`

### 5.3 Query: My Active Tasks

1. Click **+ New query**
2. Configure:
   ```
   Work Item Type = Task
   Assigned To = @Me
   State = Active
   ```
3. **Save as:** `My Active Tasks`

### 5.4 Query: Blocked Tasks

1. Click **+ New query**
2. Configure:
   ```
   Work Item Type = Task
   Tags Contains Blocked
   State <> Closed
   ```
3. **Save as:** `Blocked Tasks`

### 5.5 Query: High Priority Items

1. Click **+ New query**
2. Configure:
   ```
   Work Item Type = Task OR User Story OR Epic
   Priority = 1
   State <> Closed
   ```
3. **Save as:** `High Priority Items`

### 5.6 Create Query Folder Structure

Organize queries in folders:
```
📁 Shared Queries
  📁 Microservices Project
    📁 By Phase
      - Phase 0 Tasks
      - Phase 1 Tasks
      - Phase 2 Tasks
      ...
    📁 By Status
      - Current Sprint - Active Tasks
      - My Active Tasks
      - Blocked Tasks
      - High Priority Items
    📁 By Service
      - Auth Service Tasks
      - Core ERP Tasks
      - Accounting Tasks
      ...
```

---

## Step 6: Set Up Sprint Planning

### 6.1 Navigate to Sprints
1. Go to **Boards** → **Sprints**
2. Click **Set team iterations**

### 6.2 Create Iteration Path Structure

1. Go to **Project Settings** → **Project configuration** → **Iterations**
2. Click **+ New child**
3. Create this structure:

```
📅 Odoo-Microservices
  📅 Sprint 1 (Weeks 1-2)
    - Start: [Your Date]
    - End: +14 days
  📅 Sprint 2 (Weeks 2-3)
    - Start: Sprint 1 End + 1 day
    - End: +7 days
  📅 Sprint 3 (Weeks 3-4)
    - Start: Sprint 2 End + 1 day
    - End: +7 days
  📅 Sprint 4 (Weeks 4-5)
    - Start: Sprint 3 End + 1 day
    - End: +7 days
  📅 Sprint 5 (Weeks 5-6)
    - Start: Sprint 4 End + 1 day
    - End: +7 days
  📅 Sprint 6 (Week 6+)
    - Start: Sprint 5 End + 1 day
    - End: +7 days
```

### 6.3 Assign Work Items to Sprints

**Sprint 1:** Phase 0 + Phase 1
1. Go to **Boards** → **Backlogs**
2. Drag **Phase 0 Epic** to **Sprint 1**
3. Drag **Phase 1 Epic** to **Sprint 1**
4. All child work items will move automatically

**Sprint 2:** Phase 2 (MVP)
- Drag **Phase 2 Epic** to **Sprint 2**

**Sprint 3:** Phase 3 + Phase 4
- Drag **Phase 3 Epic** to **Sprint 3**
- Drag **Phase 4 Epic** to **Sprint 3**

**Sprint 4:** Phase 5 + Phase 6
- Drag **Phase 5 Epic** to **Sprint 4**
- Drag **Phase 6 Epic** to **Sprint 4**

**Sprint 5:** Phase 7 + Phase 8
- Drag **Phase 7 Epic** to **Sprint 5**
- Drag **Phase 8 Epic** to **Sprint 5**

**Sprint 6:** Phase 9 + Testing + Additional
- Drag **Phase 9 Epic** to **Sprint 6**
- Drag **Testing** User Stories to **Sprint 6**
- Drag **Additional Services** to **Sprint 6**

### 6.4 Set Sprint Capacity

1. Go to **Boards** → **Sprints**
2. Select **Sprint 1**
3. Click **Capacity**
4. Add your team members:
   - **Name:** [Your Name]
   - **Activity:** Development
   - **Capacity per day:** 6 hours (adjust based on your availability)
5. Click **Save**

---

## Step 7: Configure Dashboards

### 7.1 Create Main Dashboard

1. Go to **Overview** → **Dashboards**
2. Click **+ New Dashboard**
3. **Name:** `Odoo Microservices - Project Dashboard`
4. Click **Create**

### 7.2 Add Sprint Burndown Widget

1. Click **+ Add Widget**
2. Search for **Sprint Burndown**
3. Click **Add**
4. Configure:
   - **Team:** Your team
   - **Iteration:** @CurrentIteration
5. Click **Save**

### 7.3 Add Work Item Chart - By State

1. Click **+ Add Widget**
2. Search for **Chart for Work Items**
3. Click **Add**
4. Configure:
   - **Title:** Tasks by State
   - **Query:** Shared Queries/All Work Items
   - **Chart type:** Pie chart
   - **Group by:** State
5. Click **Save**

### 7.4 Add Work Item Chart - By Priority

1. Click **+ Add Widget**
2. Search for **Chart for Work Items**
3. Configure:
   - **Title:** Tasks by Priority
   - **Query:** Shared Queries/All Work Items
   - **Chart type:** Bar chart
   - **Group by:** Priority
5. Click **Save**

### 7.5 Add Velocity Widget

1. Click **+ Add Widget**
2. Search for **Velocity**
3. Configure:
   - **Team:** Your team
   - **Iterations:** 6 (to show all sprints)
5. Click **Save**

### 7.6 Add Cumulative Flow Diagram

1. Click **+ Add Widget**
2. Search for **Cumulative Flow Diagram**
3. Configure:
   - **Team:** Your team
   - **Time period:** Last 30 days
5. Click **Save**

### 7.7 Add Query Results Widgets

Add widgets for each phase:

1. **Phase 0 Progress**
   - Widget: Query Results
   - Query: Phase 0 Tasks
   - Display: Count by state

2. **Current Sprint Progress**
   - Widget: Query Results
   - Query: Current Sprint - Active Tasks
   - Display: List

3. **Blocked Items**
   - Widget: Query Results
   - Query: Blocked Tasks
   - Display: List with alerts

### 7.8 Arrange Dashboard Layout

Organize widgets in a logical layout:

```
┌─────────────────────────────────────────────────────────┐
│  Sprint Burndown           │  Velocity                  │
├─────────────────────────────────────────────────────────┤
│  Tasks by State            │  Tasks by Priority         │
├─────────────────────────────────────────────────────────┤
│  Cumulative Flow Diagram                                │
├─────────────────────────────────────────────────────────┤
│  Phase 0 Progress  │  Current Sprint  │  Blocked Items  │
└─────────────────────────────────────────────────────────┘
```

---

## Step 8: Enable Dependencies Visualization

### 8.1 Enable Dependency Tracking

1. Go to **Boards** → **Backlogs**
2. Click **View options** (top right)
3. Enable:
   - ✅ **Show parents**
   - ✅ **Show predecessors**
   - ✅ **Forecast**

### 8.2 View Dependencies on Board

1. Go to **Boards** → **Board**
2. Click on any task card
3. You'll see:
   - **Parent:** The User Story it belongs to
   - **Predecessor:** Tasks that must be completed first
   - **Successor:** Tasks that depend on this one

### 8.3 Create Delivery Plan

1. Go to **Boards** → **Delivery Plans**
2. Click **+ New plan**
3. Configure:
   - **Name:** Odoo Microservices - Phase Timeline
   - **Description:** Complete timeline showing all phases and dependencies
4. Click **Create**

5. Add your backlog:
   - Click **+ Add team**
   - Select your team
   - Choose backlog level: **Epics**

6. Configure timeline:
   - **Start date:** Your project start date
   - **End date:** +45 days
   - **Iterations:** Show all 6 sprints

7. **View dependencies:**
   - Click **Settings** → Enable **Show dependencies**
   - Dependencies will appear as lines connecting related work items

### 8.4 Use Dependency Tracker Extension (Optional)

For advanced dependency visualization:

1. Go to **Extensions** → Browse Marketplace
2. Search for **Dependency Tracker**
3. Install the extension
4. Access via **Boards** → **Dependency Tracker**

---

## 📊 Your Board Structure (Final View)

After completing all steps, your Azure Boards structure will look like this:

```
📊 Azure Boards Hierarchy

📌 Epic: Phase 0: Microservices Design (Days 1-5)
  📖 User Story: 0.1 Domain-Driven Design
    ✅ Task: 0.1.1 - Documented 11 microservices
    ✅ Task: 0.1.2 - Created service boundary diagram
    ✅ Task: 0.1.3 - Defined service responsibilities
  📖 User Story: 0.2 Database Per Service Pattern
    ✅ Task: 0.2.1 - Designed auth-db schema
    ✅ Task: 0.2.2 - Designed core-erp-db schema
    ✅ Task: 0.2.3 - Designed accounting-db schema
    ✅ Task: 0.2.4 - Designed inventory-db schema
    ✅ Task: 0.2.5 - Designed crm-db schema
  📖 User Story: 0.3 Inter-Service Communication
  📖 User Story: 0.4 Service Directory Structure
  📖 User Story: 0.5 Define Service APIs
  📖 User Story: 0.6 Service Dependencies Matrix

📌 Epic: Phase 1: Service Mesh Setup (Days 6-10)
  📖 User Story: 1.1 Install Istio
  📖 User Story: 1.2 Install Kiali Dashboard
  📖 User Story: 1.3 Configure Traffic Management
  📖 User Story: 1.4 Configure Resilience
  📖 User Story: 1.5 mTLS Configuration
  📖 User Story: 1.6 Service Mesh Testing

📌 Epic: Phase 2: Core Services Development (Days 11-18)
  [... and so on for all phases ...]
```

---

## ✅ Daily Workflow Guide

### Morning (15 minutes)
1. Open **Odoo Microservices - Project Dashboard**
2. Review **Sprint Burndown** - Are you on track?
3. Check **Blocked Items** - Any impediments?
4. Open **Current Sprint - Active Tasks**
5. Select 1-3 tasks to work on today
6. Move tasks from **To Do** → **In Progress**

### During Work
1. Open task in Azure DevOps
2. Click **Add link** → **New linked item**
3. Link related commits:
   ```bash
   git commit -m "Implement JWT auth for auth-service #47"
   # #47 = Task ID
   ```
4. Add comments with:
   - Progress notes
   - Technical decisions
   - Blockers discovered
5. Update **Remaining Work** hours

### End of Day (10 minutes)
1. Update **Completed Work** hours on tasks
2. Move finished tasks to **Done**
3. Add tomorrow's tasks to **Sprint Backlog**
4. Update CHECKLIST.md locally (keep in sync)
5. Take a screenshot of burndown chart

### Weekly Review (Friday, 30 minutes)
1. Export progress to Excel
2. Review **Velocity** chart
3. Update sprint capacity for next week
4. Groom backlog for upcoming sprint
5. Share dashboard screenshot with team/stakeholders

---

## 🎯 Quick Reference Commands

### Filter Shortcuts in Work Items
- **My tasks:** `@Me` in Assigned To
- **This sprint:** `@CurrentIteration` in Iteration Path
- **High priority:** `Priority = 1`
- **Phase 0:** `Tags Contains Phase-0`
- **Blocked:** `Tags Contains Blocked`

### Keyboard Shortcuts
- `Ctrl + Shift + F` - Search work items
- `Ctrl + K` - Quick command search
- `N` - New work item
- `Ctrl + S` - Save work item
- `Ctrl + Enter` - Save and close

### Link Types
- **Parent/Child:** Organizes hierarchy (Epic → Story → Task)
- **Predecessor/Successor:** Shows dependencies (must finish before)
- **Related:** Shows connected work items

---

## 🚀 Next Steps

1. ✅ **Create all Epics** (10 phases)
2. ✅ **Create User Stories** (~60 stories)
3. ✅ **Link 298 Tasks** to User Stories
4. ✅ **Configure Board Columns**
5. ✅ **Set up Queries**
6. ✅ **Create Sprint Plan**
7. ✅ **Build Dashboard**
8. ✅ **Enable Dependencies**

**Estimated Time to Complete:** 3-4 hours

**Pro Tip:** Do this in 2 sessions:
- **Session 1 (2 hours):** Steps 1-3 (Create structure)
- **Session 2 (1-2 hours):** Steps 4-8 (Configure views)

---

## 📚 Additional Resources

- [Azure Boards Documentation](https://docs.microsoft.com/azure/devops/boards/)
- [Agile Best Practices](https://docs.microsoft.com/azure/devops/boards/best-practices-agile-project-management)
- [Query Examples](https://docs.microsoft.com/azure/devops/boards/queries/wiql-syntax)

---

**Questions?** Check the [AZURE_DEVOPS_SETUP.md](AZURE_DEVOPS_SETUP.md) troubleshooting section or ask for help!

**Last Updated:** December 25, 2025
