#!/usr/bin/env python3
"""
Manual Team Sprint Configuration - Web Portal Instructions
Since the API has restrictions, here's how to manually configure the sprints
"""

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  MANUAL CONFIGURATION: Add Sprints to Team                            ║
╚═══════════════════════════════════════════════════════════════════════╝

The sprints exist in your project but need to be added to your team.
This is a one-time manual setup in the Azure DevOps portal.

📋 STEP-BY-STEP INSTRUCTIONS:

1. Go to Azure DevOps Project Settings
   → https://dev.azure.com/Aries-Test/Odoo-Microservices/_settings/

2. In the left sidebar, click:
   └─ Boards
      └─ Team configuration
         └─ Click on "Odoo-Microservices Team"

3. Click on the "Iterations" tab

4. Click "+ Select iteration(s)" button

5. In the dialog that appears, you'll see a tree structure:
   
   ☐ Iteration
       ☑ Iteration 1  (already selected)
       ☑ Iteration 2  (already selected)
       ☑ Iteration 3  (already selected)
       ☐ Sprint 1     ← CHECK THIS
       ☐ Sprint 2     ← CHECK THIS
       ☐ Sprint 3     ← CHECK THIS
       ☐ Sprint 4     ← CHECK THIS
       ☐ Sprint 5     ← CHECK THIS
       ☐ Sprint 6     ← CHECK THIS

6. Check all Sprint 1-6 checkboxes

7. Click "Save and close"

✅ DONE! Now go to Boards → Sprints to see all your sprints!

═══════════════════════════════════════════════════════════════════════

📊 YOUR SPRINTS:

Sprint 1 (Dec 25 - Jan 4, 2026)  - Phase 0-1  - 2 Epics + 12 Stories
Sprint 2 (Jan 4 - Jan 14, 2026)  - Phase 2-3  - 2 Epics + 10 Stories  
Sprint 3 (Jan 14 - Jan 24, 2026) - Phase 4-5  - 2 Epics + 11 Stories
Sprint 4 (Jan 24 - Jan 29, 2026) - Phase 6-7  - 2 Epics + 9 Stories
Sprint 5 (Jan 29 - Feb 3, 2026)  - Phase 8    - 1 Epic + 6 Stories
Sprint 6 (Feb 3 - Feb 8, 2026)   - Phase 9    - 1 Epic + 22 Stories

═══════════════════════════════════════════════════════════════════════

🔗 QUICK LINKS:

• Team Settings: 
  https://dev.azure.com/Aries-Test/Odoo-Microservices/_settings/work

• After configuration, view sprints at:
  https://dev.azure.com/Aries-Test/Odoo-Microservices/_sprints

═══════════════════════════════════════════════════════════════════════
""")
