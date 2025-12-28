# User Stories Documentation

This folder contains implementation documentation for all user stories worked on in this project.

## Structure

Each user story (or group of related user stories) has its own folder with documentation files.

```
user-stories/
├── README.md (this file)
├── US-381-382-383-apps-modules/
│   └── IMPLEMENTATION.md
└── [future user stories]/
    └── IMPLEMENTATION.md
```

## Folder Naming Convention

- Format: `US-[numbers]-[brief-description]/`
- Example: `US-381-382-383-apps-modules/`
- Use hyphens for spaces
- Use lowercase for descriptions
- Group related user stories together

## File Naming Convention

- **IMPLEMENTATION.md** - Main implementation documentation
- **TESTING.md** - Test cases and results (if separate from implementation)
- **NOTES.md** - Development notes, decisions, blockers
- **SCREENSHOTS/** - Supporting images or screenshots

## Index of User Stories

### Completed
- ✅ **US-381-382-383**: Apps & Modules Management
  - US 381: Install & Configure Apps (CRM)
  - US 382: Upgrade Applications
  - US 383: Uninstall Applications (Point of Sale)
  - **Location:** `user-stories/US-381-382-383-apps-modules/`
  - **Branch:** feature/US-381-383-apps-modules
  - **Status:** Merged to Odoo-19.0-local-dev

### In Progress
- (None currently)

### Planned
- (Add future user stories here)

## Usage

When starting a new user story:

1. Create a folder: `user-stories/US-[number]-[description]/`
2. Add `IMPLEMENTATION.md` to document your work
3. Commit regularly as you make progress
4. Update this README with the user story status
5. Link to the feature branch and PR when created

## Best Practices

- ✅ Document as you work, not after
- ✅ Include technical details, not just business descriptions
- ✅ Add test results and verification steps
- ✅ Reference related work items, PRs, and branches
- ✅ Include any blockers or challenges faced
- ✅ Update the index in this README when completing stories
