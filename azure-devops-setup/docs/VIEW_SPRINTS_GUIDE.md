# 📋 How to View Work Items by Sprint in Azure DevOps

## 🎯 The Issue

When you go to `Boards` → `Work Items`, everything appears in one list in the "New" column. This makes it hard to see which items belong to which sprint.

## ✅ Solution: Use the Sprints View

### Step 1: Navigate to Sprints View

1. Go to: https://dev.azure.com/Aries-Test/Odoo-Microservices
2. Click **`Boards`** in the left menu
3. Click **`Sprints`** (not "Work Items" or "Boards")
4. You'll see a dropdown showing all your sprints

### Step 2: Select a Sprint

In the Sprints view, you'll see a dropdown at the top:
- **Sprint 1** (Dec 25 - Jan 4) - Phase 0-1
- **Sprint 2** (Jan 4 - Jan 14) - Phase 2-3  
- **Sprint 3** (Jan 14 - Jan 24) - Phase 4-5
- **Sprint 4** (Jan 24 - Jan 29) - Phase 6-7
- **Sprint 5** (Jan 29 - Feb 3) - Phase 8
- **Sprint 6** (Feb 3 - Feb 8) - Phase 9 + Testing

Click on any sprint to see only its work items!

### Step 3: View Sprint Board

Once you select a sprint, you'll see:
- **Backlog tab**: List of all work items in this sprint
- **Board tab**: Kanban board with columns (New, Active, Resolved, Closed)
- **Capacity tab**: Team capacity planning
- **Taskboard tab**: Detailed task view

## 🚀 Activate Sprint 1 (Recommended)

To start working on Sprint 1:

1. In the Sprints view, select **Sprint 1**
2. Click the **"Set sprint dates"** button (if not already set)
3. Verify dates: Dec 25, 2025 - Jan 4, 2026
4. Click **"Start sprint"** button
5. The sprint is now active!

### What "Activating" Does:

- Makes it the current/active sprint
- Shows on the team's sprint board
- Enables burndown charts
- Allows capacity planning

## 📊 Organize Work Items on the Board

### Move Items Across Columns

Work items start in "New" column. To organize them:

1. Select a sprint in the Sprints view
2. Click the **Board** tab
3. Drag and drop cards between columns:
   - **New** → Planning/not started
   - **Active** → Currently working
   - **Resolved** → Code complete, needs review
   - **Closed** → Fully done

### Filter by Work Item Type

Use the filters at the top of the board:
- Show only **Epics**
- Show only **User Stories**
- Show only **Tasks**

## 🔍 Alternative Views

### View by Sprint in Backlog

1. Go to `Boards` → `Backlogs`
2. On the right side, expand the **sprint nodes**:
   - Sprint 1 (with its Epics and Stories)
   - Sprint 2 (with its Epics and Stories)
   - etc.
3. You'll see a hierarchical view of all sprints

### Query for Specific Sprint

1. Go to `Boards` → `Queries`
2. Click **"+ New query"**
3. Add filter:
   ```
   Iteration Path = Odoo-Microservices\Sprint 1
   ```
4. Save and run the query

## 📈 View Sprint-Specific Metrics

Once Sprint 1 is activated:

1. Go to `Boards` → `Sprints` → Select **Sprint 1**
2. Click **Analytics** tab (or **Charts**)
3. You'll see:
   - **Burndown chart** - Remaining work over time
   - **Velocity** - Story points completed
   - **Cumulative flow** - Work item states over time

## 🎨 Customize Board Columns

If you want different columns (not just New/Active/Resolved/Closed):

1. Go to `Project Settings` (bottom left)
2. Click `Team configuration` → Select your team
3. Click `Board` → `Columns`
4. Add/rename/remove columns as needed

Common columns:
- **To Do** (New)
- **In Progress** (Active)
- **Code Review** (custom)
- **Testing** (custom)
- **Done** (Closed)

## 🔄 Quick Sprint Navigation

### Keyboard Shortcuts

- `Ctrl + Shift + ,` - Previous sprint
- `Ctrl + Shift + .` - Next sprint
- `Ctrl + Shift + H` - Go to sprint home

### Sprint Selector

At the top of the Sprints view, use the dropdown to quickly jump between sprints:
```
Current: Sprint 1 ▼
  └─ Sprint 1 (Dec 25 - Jan 4)
  └─ Sprint 2 (Jan 4 - Jan 14)
  └─ Sprint 3 (Jan 14 - Jan 24)
  └─ Sprint 4 (Jan 24 - Jan 29)
  └─ Sprint 5 (Jan 29 - Feb 3)
  └─ Sprint 6 (Feb 3 - Feb 8)
```

## ✅ Summary

**To see work items organized by sprint:**

1. ✅ Use **`Boards → Sprints`** view (not "Work Items")
2. ✅ Select sprint from dropdown at top
3. ✅ View **Board tab** to see Kanban board
4. ✅ Activate Sprint 1 to start tracking progress
5. ✅ Drag items across columns as work progresses

**Current Sprint Assignments:**

- Sprint 1: 2 Epics + 12 User Stories
- Sprint 2: 2 Epics + 10 User Stories
- Sprint 3: 2 Epics + 11 User Stories
- Sprint 4: 2 Epics + 9 User Stories
- Sprint 5: 1 Epic + 6 User Stories
- Sprint 6: 1 Epic + 22 User Stories

All 298 tasks are linked to their parent User Stories and will automatically appear under the correct sprint! 🎯

---

**Need Help?**
- 📊 View local dashboard: `xdg-open azure-devops-setup/sprint-dashboard.html`
- 🌐 Azure DevOps: https://dev.azure.com/Aries-Test/Odoo-Microservices
- 📚 Main docs: [azure-devops-setup/README.md](../README.md)
