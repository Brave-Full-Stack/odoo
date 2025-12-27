#!/usr/bin/env python3
"""
Azure DevOps Repository Integration Setup
Configures repository linking, branch policies, and PR automation
"""

import requests
from base64 import b64encode
import json
import os

# Configuration
ORG_URL = "https://dev.azure.com/Aries-Test"
PROJECT = "Odoo-Dev"
REPO_NAME = "odoo"  # Will be created if doesn't exist
GITHUB_REPO = "Brave-Full-Stack/odoo"
BRANCH = "Odoo-19.0-local-dev"
PAT = os.environ.get('AZURE_DEVOPS_PAT') or input('Enter your Azure DevOps PAT: ').strip()

# Create auth header
auth_string = f":{PAT}"
auth_b64 = b64encode(auth_string.encode('ascii')).decode('ascii')
headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def check_repo_exists():
    """Check if repository exists in Azure DevOps"""
    print("\n🔍 Checking for existing repositories...")
    url = f"{ORG_URL}/{PROJECT}/_apis/git/repositories?api-version=7.1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos = response.json().get('value', [])
        
        print(f"   ✓ Found {len(repos)} repositories")
        for repo in repos:
            print(f"      • {repo['name']}")
        
        return repos
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Error: {e}")
        return []

def get_branch_policies_instructions():
    """Generate instructions for setting up branch policies"""
    return """
╔══════════════════════════════════════════════════════════════════════════╗
║         BRANCH POLICY CONFIGURATION INSTRUCTIONS                         ║
╚══════════════════════════════════════════════════════════════════════════╝

Branch policies protect important branches and ensure code quality.

📝 Manual Setup Required (Web UI):

1. Navigate to: Repos → Branches
   URL: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/repositories

2. Find branch: Odoo-19.0-local-dev

3. Click the "⋮" menu → Branch policies

4. Configure the following policies:

   ✅ REQUIRE A MINIMUM NUMBER OF REVIEWERS
      • Minimum reviewers: 1
      • ☑ Allow requestors to approve their own changes: NO
      • ☑ Prohibit the most recent pusher from approving: YES
      • ☑ Allow completion even if some reviewers vote to wait or reject: NO

   ✅ CHECK FOR LINKED WORK ITEMS
      • ☑ Required
      • This ensures every PR is associated with a work item

   ✅ CHECK FOR COMMENT RESOLUTION
      • ☑ Required
      • All comments must be resolved before merging

   ✅ LIMIT MERGE TYPES
      • ☑ Basic merge (no fast-forward): ALLOWED
      • ☑ Squash merge: ALLOWED
      • ☑ Rebase and fast-forward: ALLOWED
      • ☑ Rebase with merge commit: DISABLED

   ✅ BUILD VALIDATION (After CI pipeline setup)
      • Add build policy
      • Select build pipeline
      • Policy requirement: Required
      • Build expiration: Immediately

   ✅ AUTOMATICALLY INCLUDE CODE REVIEWERS
      • Add reviewers who should always be notified
      • Example: Tech leads, architects

5. Save changes

═══════════════════════════════════════════════════════════════════════════

🔗 Quick Access:
   Branch Policies: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/repositories?_a=policiesMid&repoId={repo_id}

💡 Benefits:
   • Prevents direct commits to main branch
   • Ensures code review before merge
   • Maintains work item traceability
   • Enforces quality gates
"""

def get_pr_template():
    """Generate PR template content"""
    return """# Pull Request Template

## 📋 Description
<!-- Provide a brief description of the changes -->

## 🔗 Related Work Items
<!-- Link to User Story or Task -->
Fixes #[work-item-id]
Related to #[work-item-id]

## 🎯 Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🔧 Configuration change
- [ ] 🎨 Code style update (formatting, renaming)
- [ ] ♻️ Code refactoring
- [ ] ⚡ Performance improvement

## 🧪 Testing
<!-- Describe the tests you ran to verify your changes -->

### Test Configuration
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

### Test Results
```
# Paste test results here
```

## 📸 Screenshots (if applicable)
<!-- Add screenshots to help explain your changes -->

## ✅ Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## 📊 Impact Analysis
<!-- Describe potential impacts of this change -->

### Areas Affected
- [ ] User Interface
- [ ] API
- [ ] Database
- [ ] Configuration
- [ ] Dependencies

### Risk Level
- [ ] 🟢 Low - Minor changes, well tested
- [ ] 🟡 Medium - Moderate changes, some testing
- [ ] 🔴 High - Major changes, needs extensive testing

## 📝 Additional Notes
<!-- Any additional information that reviewers should know -->

---

**Deployed To:** 
- [ ] Development
- [ ] Staging  
- [ ] Production

**Reviewer:** @mention
**Merge Type:** Squash and merge
"""

def create_pr_template_file():
    """Create PR template file in repository"""
    template_path = "../.azuredevops/pull_request_template.md"
    
    print("\n📄 Creating Pull Request Template...")
    
    try:
        os.makedirs("../.azuredevops", exist_ok=True)
        
        with open(template_path, 'w') as f:
            f.write(get_pr_template())
        
        print(f"   ✓ Template created: {template_path}")
        print("   ℹ Commit this file to repository for automatic PR template")
        return True
    except Exception as e:
        print(f"   ✗ Error creating template: {e}")
        return False

def get_github_integration_guide():
    """Generate guide for GitHub integration"""
    return """
╔══════════════════════════════════════════════════════════════════════════╗
║            GITHUB REPOSITORY INTEGRATION GUIDE                           ║
╚══════════════════════════════════════════════════════════════════════════╝

Azure DevOps can integrate with external GitHub repositories.

📝 Setup Steps:

1. INSTALL AZURE PIPELINES APP ON GITHUB
   a. Go to: https://github.com/marketplace/azure-pipelines
   b. Click "Set up a plan"
   c. Choose "Free" plan
   d. Click "Install it for free"
   e. Select repositories: Brave-Full-Stack/odoo
   f. Authorize installation

2. CREATE SERVICE CONNECTION IN AZURE DEVOPS
   a. Go to: Project Settings → Service connections
   b. Click "New service connection"
   c. Select "GitHub"
   d. Choose authentication method: OAuth or Personal Access Token
   e. Authorize connection
   f. Name: "GitHub-Brave-Full-Stack"
   g. Grant access permission to all pipelines (optional)

3. LINK REPOSITORY TO AZURE REPOS (Optional)
   Note: You can use GitHub directly without mirroring
   
   a. If you want to mirror to Azure Repos:
      • Repos → Files → Import repository
      • Clone URL: https://github.com/Brave-Full-Stack/odoo.git
      • Requires authentication

4. ENABLE WORK ITEM LINKING
   a. Project Settings → GitHub connections
   b. Connect your GitHub repository
   c. Enable "Work item linking"
   
   This allows:
   • Commit messages to reference work items: "Fixes #381"
   • PRs to automatically link to work items
   • Work items to show related commits/PRs

5. COMMIT MESSAGE PATTERNS
   Use these patterns in commit messages to link work items:
   
   ✅ Fixes #381         - Closes work item when PR merges
   ✅ Resolves #381      - Closes work item when PR merges
   ✅ Closes #381        - Closes work item when PR merges
   ✅ Related to #381    - Links without closing
   ✅ #381               - Links without closing

   Example commit:
   ```
   git commit -m "feat: Add OAuth Facebook integration
   
   Implements authentication flow for Facebook OAuth provider.
   Includes token validation and user profile retrieval.
   
   Fixes #393
   Related to #384, #387"
   ```

═══════════════════════════════════════════════════════════════════════════

🔗 Useful Links:
   • Azure Pipelines GitHub App: https://github.com/marketplace/azure-pipelines
   • Service Connections: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/adminservices
   • GitHub Connections: https://dev.azure.com/Aries-Test/Odoo-Dev/_settings/sourcecontrol

💡 Benefits:
   • Automatic work item linking from commits
   • PR integration with Azure Boards
   • Build status in GitHub PRs
   • Unified tracking across platforms
"""

def print_repo_integration_summary():
    """Print comprehensive integration summary"""
    print("\n" + "=" * 78)
    print("📚 REPOSITORY INTEGRATION SETUP SUMMARY")
    print("=" * 78)
    
    print("\n✅ COMPLETED:")
    print("   • Pull Request template created")
    print("   • Integration guides generated")
    
    print("\n📋 MANUAL STEPS REQUIRED:")
    print("\n1. GITHUB INTEGRATION")
    print("   • Install Azure Pipelines app on GitHub")
    print("   • Create service connection in Azure DevOps")
    print("   • Enable work item linking")
    
    print("\n2. BRANCH POLICIES")
    print("   • Configure policies on Odoo-19.0-local-dev branch")
    print("   • Require minimum reviewers: 1")
    print("   • Require linked work items")
    print("   • Require comment resolution")
    
    print("\n3. PR TEMPLATE")
    print("   • Commit .azuredevops/pull_request_template.md to repository")
    print("   • Template will auto-populate new PRs")
    
    print("\n4. BUILD VALIDATION")
    print("   • Create CI pipeline first (see AZURE_DEVOPS_PROFESSIONAL_SETUP.md)")
    print("   • Add as branch policy requirement")
    
    print("\n" + "=" * 78)
    print("📖 DETAILED GUIDES AVAILABLE:")
    print("=" * 78)
    print("   • Branch Policies: See output above")
    print("   • GitHub Integration: See output above")
    print("   • Complete Setup: AZURE_DEVOPS_PROFESSIONAL_SETUP.md")
    
    print("\n🔗 QUICK ACCESS URLS:")
    print(f"   • Project Settings: {ORG_URL}/{PROJECT}/_settings/")
    print(f"   • Repositories: {ORG_URL}/{PROJECT}/_settings/repositories")
    print(f"   • Service Connections: {ORG_URL}/{PROJECT}/_settings/adminservices")
    print(f"   • GitHub Connections: {ORG_URL}/{PROJECT}/_settings/sourcecontrol")

def main():
    print("=" * 78)
    print("Azure DevOps Repository Integration Setup")
    print("=" * 78)
    print(f"Project: {PROJECT}")
    print(f"GitHub Repo: {GITHUB_REPO}")
    print(f"Branch: {BRANCH}")
    
    # Check existing repos
    repos = check_repo_exists()
    
    # Create PR template
    create_pr_template_file()
    
    # Print guides
    print(get_branch_policies_instructions())
    print(get_github_integration_guide())
    
    # Print summary
    print_repo_integration_summary()
    
    print("\n" + "=" * 78)
    print("✅ Repository Integration Setup Complete!")
    print("=" * 78)
    print("\n📝 Follow the guides above to complete manual configuration")
    print("💡 All changes to .azuredevops/ should be committed to git")
    
    return 0

if __name__ == "__main__":
    exit(main())
