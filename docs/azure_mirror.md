# GitHub → Azure DevOps (one-way mirror)

This document explains the one-way mirroring setup implemented in `.github/workflows/mirror-to-azure.yml`.

Overview
- GitHub is the primary source of truth.
- A GitHub Actions workflow runs on pushes to selected branches and pushes the branch and tags to an Azure Repos repository using an authenticated remote URL.

Required secrets (set in the GitHub repository settings → Secrets):
- `AZURE_USER` — any username for HTTP auth (commonly your Azure DevOps username or `git`).
- `AZURE_DEVOPS_PAT` — Personal Access Token for Azure DevOps with `Code (read & write)` scope.
- `AZURE_REPO_HOST_AND_PATH` — host and path portion of the Azure repo URL, for example:
  `dev.azure.com/ORG/PROJECT/_git/REPO`  
  (the workflow will prepend `https://${AZURE_USER}:${AZURE_DEVOPS_PAT}@` when pushing)

Notes and safety
- The workflow pushes only the branch that triggered the action (or the `branch` input when manually triggered) and pushes tags.
- This is a one-way mirror: do not push directly to Azure Repos — it will cause divergence.
- Protect `main`/`develop` in GitHub and require CI checks there. Consider limiting the branches mirrored by editing the workflow trigger list.

How to create an Azure DevOps PAT
1. In Azure DevOps, open User Settings → Personal access tokens → New token.
2. Give it a descriptive name, expiry and select `Code (read & write)` scope.
3. Copy the token and add it to GitHub secrets as `AZURE_DEVOPS_PAT`.

How to get `AZURE_REPO_HOST_AND_PATH`
1. In Azure DevOps, open the target repo and click `Clone` → `HTTPS`.
2. The full URL looks like `https://dev.azure.com/ORG/PROJECT/_git/REPO` — drop the `https://` prefix and use `dev.azure.com/ORG/PROJECT/_git/REPO` as the secret value.

Manual run
- From Actions → Mirror to Azure Repos → Run workflow → provide `branch` input to push a specific branch.

Troubleshooting
- If the action fails with auth errors, verify the PAT scopes and that `AZURE_USER` name is valid.
- To mirror additional branches, add them to the `on.push.branches` list in the workflow.

Security reminder
- Keep the PAT scoped and rotate periodically. Do not store PATs in files — use GitHub Secrets.
