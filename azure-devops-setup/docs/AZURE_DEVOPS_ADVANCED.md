# Azure DevOps Advanced Configuration Guide
# Extended setup for Odoo Microservices Project

## Table of Contents
1. [Service Connections Setup](#service-connections-setup)
2. [Variable Groups Configuration](#variable-groups-configuration)
3. [Environments Setup](#environments-setup)
4. [Branch Policies](#branch-policies)
5. [Pull Request Templates](#pull-request-templates)
6. [Work Item Automation](#work-item-automation)
7. [Dashboard Configuration](#dashboard-configuration)
8. [Integration with External Tools](#integration-with-external-tools)

---

## 1. Service Connections Setup

### 1.1 Harbor Container Registry Connection

1. Go to **Project Settings** → **Service connections** → **New service connection**
2. Select **Docker Registry**
3. Configure:
   ```
   Registry type: Others
   Docker Registry: https://harbor.example.com
   Docker ID: admin (or your Harbor username)
   Docker Password: <your-harbor-password>
   Service connection name: harbor-connection
   ```
4. Check **Grant access permission to all pipelines**
5. Click **Verify and save**

### 1.2 Kubernetes Cluster Connections

**Development Cluster:**
1. **Service connection type:** Kubernetes
2. **Authentication method:** Service Account
3. **Server URL:** `https://dev-k8s-cluster.example.com`
4. **Service Account Certificate:** (paste dev cluster certificate)
5. **Connection name:** `k8s-dev-connection`

**Staging Cluster:**
- Same steps, use staging cluster credentials
- Connection name: `k8s-staging-connection`

**Production Cluster:**
- Same steps, use production cluster credentials
- Connection name: `k8s-prod-connection`

### 1.3 Azure Service Connection (for AKS/ACR)

1. Go to **Service connections** → **New service connection**
2. Select **Azure Resource Manager**
3. **Authentication method:** Service principal (automatic)
4. **Scope level:** Subscription
5. **Subscription:** Select your Azure subscription
6. **Service connection name:** `azure-service-connection`
7. Click **Save**

### 1.4 AWS Service Connection (Optional)

```bash
# Create IAM user for Azure DevOps
aws iam create-user --user-name azure-devops-odoo
aws iam attach-user-policy --user-name azure-devops-odoo --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
aws iam create-access-key --user-name azure-devops-odoo
```

In Azure DevOps:
1. **Service connection type:** AWS
2. **Access Key ID:** (from above)
3. **Secret Access Key:** (from above)
4. **Connection name:** `aws-service-connection`

### 1.5 SonarQube Connection

1. Get SonarQube token:
   ```bash
   # From SonarQube: Administration → Security → Users → Tokens
   # Generate token for Azure DevOps
   ```
2. In Azure DevOps:
   - **Type:** SonarQube
   - **Server URL:** `https://sonarqube.example.com`
   - **Token:** (paste token)
   - **Connection name:** `sonarqube-connection`

---

## 2. Variable Groups Configuration

### 2.1 Create Variable Groups

Go to **Pipelines** → **Library** → **+ Variable group**

#### Group 1: `odoo-secrets`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `POSTGRES_PASSWORD` | `<strong-password>` | ✅ |
| `RABBITMQ_PASSWORD` | `<rabbitmq-password>` | ✅ |
| `REDIS_PASSWORD` | `<redis-password>` | ✅ |
| `ODOO_ADMIN_PASSWORD` | `<admin-password>` | ✅ |
| `JWT_SECRET_KEY` | `<jwt-secret>` | ✅ |
| `ENCRYPTION_KEY` | `<encryption-key>` | ✅ |

#### Group 2: `harbor-credentials`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `HARBOR_USERNAME` | `admin` | ❌ |
| `HARBOR_PASSWORD` | `<harbor-password>` | ✅ |
| `HARBOR_URL` | `harbor.example.com` | ❌ |
| `HARBOR_PROJECT` | `odoo-microservices` | ❌ |

#### Group 3: `azure-credentials`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `ARM_CLIENT_ID` | `<azure-client-id>` | ✅ |
| `ARM_CLIENT_SECRET` | `<azure-client-secret>` | ✅ |
| `ARM_SUBSCRIPTION_ID` | `<subscription-id>` | ❌ |
| `ARM_TENANT_ID` | `<tenant-id>` | ❌ |
| `TF_STATE_STORAGE_ACCOUNT` | `odooterraformstate` | ❌ |
| `TF_STATE_CONTAINER` | `terraform-state` | ❌ |
| `TF_STATE_ACCESS_KEY` | `<storage-access-key>` | ✅ |

#### Group 4: `aws-credentials`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `AWS_ACCESS_KEY_ID` | `<aws-access-key>` | ✅ |
| `AWS_SECRET_ACCESS_KEY` | `<aws-secret-key>` | ✅ |
| `AWS_REGION` | `us-east-1` | ❌ |
| `EKS_CLUSTER_NAME` | `odoo-prod-cluster` | ❌ |

#### Group 5: `notification-settings`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `SLACK_WEBHOOK_URL` | `https://hooks.slack.com/...` | ✅ |
| `TEAMS_WEBHOOK_URL` | `https://outlook.office.com/...` | ✅ |
| `STATUS_PAGE_ID` | `<statuspage-id>` | ❌ |
| `STATUS_PAGE_TOKEN` | `<statuspage-token>` | ✅ |
| `PAGERDUTY_INTEGRATION_KEY` | `<pagerduty-key>` | ✅ |

#### Group 6: `monitoring-config`

| Variable Name | Value | Secret? |
|--------------|-------|---------|
| `GRAFANA_ADMIN_PASSWORD` | `<grafana-password>` | ✅ |
| `PROMETHEUS_RETENTION` | `30d` | ❌ |
| `LOKI_RETENTION` | `14d` | ❌ |
| `DATADOG_API_KEY` | `<datadog-key>` | ✅ |
| `NEWRELIC_LICENSE_KEY` | `<newrelic-key>` | ✅ |

### 2.2 Link Variable Groups to Pipelines

In each pipeline YAML file, reference variable groups:

```yaml
variables:
  - group: odoo-secrets
  - group: harbor-credentials
  - group: azure-credentials
```

---

## 3. Environments Setup

### 3.1 Create Environments

Go to **Pipelines** → **Environments** → **New environment**

#### Environment: `odoo-dev`
- **Name:** `odoo-dev`
- **Description:** Development environment for testing
- **Resources:** Add Kubernetes namespace `odoo-dev`
- **Approvals:** None
- **Checks:** None

#### Environment: `odoo-staging`
- **Name:** `odoo-staging`
- **Description:** Staging environment for pre-production testing
- **Resources:** Add Kubernetes namespace `odoo-staging`
- **Approvals:** 
  - Add approver: Team Lead
  - Timeout: 24 hours
- **Checks:**
  - Invoke Azure Function: `staging-readiness-check`
  - Business hours: Only allow during 9 AM - 5 PM

#### Environment: `odoo-production`
- **Name:** `odoo-production`
- **Description:** Production environment
- **Resources:** Add Kubernetes namespace `odoo-prod`
- **Approvals:**
  - Add approvers: Lead Developer, DevOps Manager
  - Timeout: 48 hours
  - Instructions: "Review deployment plan and test results before approval"
- **Checks:**
  - Query Azure Monitor
  - Invoke REST API: `production-health-check`
  - Business hours: Only allow deployments on Tue-Thu, 10 AM - 2 PM

#### Environment: `infrastructure-production`
- **Name:** `infrastructure-production`
- **Description:** Infrastructure changes (Terraform/Helm)
- **Approvals:**
  - Add approvers: Infrastructure Team, Security Team
  - Timeout: 72 hours
- **Checks:**
  - Cost threshold: <$1000/month increase
  - Security scan: Must pass Terraform security checks

---

## 4. Branch Policies

### 4.1 Configure Branch Protection

Go to **Repos** → **Branches** → Select branch → **Branch policies**

#### Main Branch (`main`)
```yaml
Policies:
  - Require a minimum number of reviewers: 2
  - Allow requestors to approve their own changes: ❌
  - Prohibit the most recent pusher from approving: ✅
  - Reset code reviewer votes when there are new changes: ✅
  - Require comment resolution: ✅
  
Build Validation:
  - Build pipeline: microservices-pipeline.yml
  - Trigger: Automatic
  - Policy requirement: Required
  - Build expiration: 12 hours
  
Status Checks:
  - All tests passed
  - Security scan completed
  - Code coverage > 80%
```

#### Develop Branch (`develop`)
```yaml
Policies:
  - Require a minimum number of reviewers: 1
  - Allow requestors to approve their own changes: ❌
  - Reset code reviewer votes when there are new changes: ✅
  
Build Validation:
  - Build pipeline: microservices-pipeline.yml
  - Trigger: Automatic
  - Policy requirement: Required
```

#### Release Branches (`release/*`)
```yaml
Policies:
  - Require a minimum number of reviewers: 2
  - Prohibit the most recent pusher from approving: ✅
  - Require comment resolution: ✅
  - Limit merge types: Squash merge only
  
Build Validation:
  - Build pipeline: microservices-pipeline.yml
  - E2E tests: Required
```

### 4.2 Branch Naming Conventions

Enforce branch naming policy:
```
feature/*  - New features
bugfix/*   - Bug fixes
hotfix/*   - Urgent production fixes
release/*  - Release candidates
```

---

## 5. Pull Request Templates

### 5.1 Create PR Template

Create `.azuredevops/pull_request_template.md`:

```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Work Items
<!-- Link work items: Fixes #123 -->
Fixes #

## Microservices Affected
- [ ] auth-service
- [ ] core-erp-service
- [ ] accounting-service
- [ ] inventory-service
- [ ] crm-service
- [ ] hr-service
- [ ] sales-service
- [ ] reporting-service
- [ ] workflow-service
- [ ] notification-service
- [ ] file-storage-service

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Security implications reviewed
- [ ] Performance impact assessed

## Screenshots (if applicable)
<!-- Add screenshots -->

## Deployment Notes
<!-- Special deployment instructions -->
```

---

## 6. Work Item Automation

### 6.1 Auto-Link Commits to Work Items

1. Go to **Project Settings** → **Repositories** → **Policies**
2. Enable **"Automatically create links for work items mentioned in commit messages"**
3. Use format in commits:
   ```bash
   git commit -m "feat: implement JWT auth #123"
   git commit -m "fix: resolve database connection issue #456"
   ```

### 6.2 Auto-Transition Work Items

Create automation rules:

#### Rule 1: Start Work Item on Branch Creation
```yaml
When: Branch created matching pattern feature/*, bugfix/*
Then: 
  - Move work item to "Doing" state
  - Add comment: "Development started"
  - Assign to branch creator
```

#### Rule 2: Move to Review on PR Creation
```yaml
When: Pull request created
Then:
  - Move linked work items to "In Review"
  - Add comment: "PR created: {{PR.URL}}"
```

#### Rule 3: Complete on PR Merge
```yaml
When: Pull request completed (merged)
Then:
  - Move linked work items to "Done"
  - Add comment: "Merged in {{PR.TargetBranch}}"
  - Close work item
```

### 6.3 Create Custom Work Item Templates

**Bug Template:**
```yaml
Title: [BUG] <brief description>
Fields:
  - Repro Steps
  - Expected Behavior
  - Actual Behavior
  - Environment (Dev/Staging/Prod)
  - Affected Service
  - Severity
Tags: Bug, <service-name>
```

**Feature Template:**
```yaml
Title: [FEATURE] <feature name>
Fields:
  - User Story
  - Acceptance Criteria
  - Technical Approach
  - Dependencies
  - Estimated Days
Tags: Feature, <phase>, <service-name>
```

---

## 7. Dashboard Configuration

### 7.1 Create Project Dashboard

Go to **Overview** → **Dashboards** → **New Dashboard**

**Dashboard Name:** "Odoo Microservices - Overview"

#### Widgets to Add:

1. **Sprint Burndown**
   - Type: Sprint Burndown
   - Team: Odoo Microservices Team
   - Size: 3x2

2. **Work Item Progress**
   - Type: Work items
   - Query: All work items grouped by state
   - Size: 2x2

3. **Build Pipeline Status**
   - Type: Build history
   - Pipeline: microservices-pipeline.yml
   - Size: 3x2

4. **Test Results Trend**
   - Type: Test results trend
   - Pipeline: microservices-pipeline.yml
   - Size: 2x2

5. **Code Coverage**
   - Type: Code coverage
   - Build: Latest
   - Size: 2x1

6. **Deployment Status**
   - Type: Release pipeline overview
   - Environments: Dev, Staging, Production
   - Size: 3x2

7. **Work by Priority**
   - Type: Chart for work items
   - Query: By Priority
   - Chart type: Pie chart
   - Size: 2x2

8. **Phase Progress**
   - Type: Query tile
   - Query: Tasks by Phase
   - Size: 4x1

9. **Velocity**
   - Type: Velocity
   - Team: Odoo Microservices Team
   - Iterations: Last 6 sprints
   - Size: 3x2

10. **Pull Request Status**
    - Type: Pull request
    - Repository: odoo
    - Size: 2x2

### 7.2 Create Service-Specific Dashboards

Create separate dashboards for each microservice:

```
Dashboard: "Auth Service Status"
Widgets:
- Build history (auth-service)
- Test results
- Code coverage
- Security vulnerabilities
- Response time metrics
- Error rate
```

---

## 8. Integration with External Tools

### 8.1 Slack Integration

1. Go to **Project Settings** → **Service hooks**
2. Click **Create subscription**
3. Select **Slack**
4. Configure:
   ```
   Webhook URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   Trigger: Build completed
   Filters: Only failed builds
   Channel: #odoo-deployments
   ```

Create subscriptions for:
- Build failures → `#odoo-deployments`
- PR created → `#code-reviews`
- Work item assigned → `#team-notifications`
- Release created → `#releases`

### 8.2 Microsoft Teams Integration

Similar to Slack, create webhooks:
```
Team: Development Team
Channel: Odoo Microservices
Webhook: https://outlook.office.com/webhook/...
```

### 8.3 Jira Integration (if needed)

1. Install **Azure DevOps Integration for Jira**
2. Configure:
   ```
   Azure DevOps URL: https://dev.azure.com/your-org
   PAT Token: <your-pat>
   Project: Odoo-Microservices
   ```
3. Enable two-way sync:
   - Jira Issue → Azure Work Item
   - Azure Work Item → Jira Issue

### 8.4 GitHub Integration

1. Go to **Project Settings** → **GitHub connections**
2. Connect to `odoo/odoo` repository
3. Enable:
   - Auto-link work items
   - Import GitHub issues
   - GitHub Actions integration

### 8.5 Datadog/New Relic Integration

**Datadog:**
```bash
# Add Datadog task to pipeline
- task: PublishToDatadog@1
  inputs:
    apiKey: $(DATADOG_API_KEY)
    metrics:
      - name: 'deployment.count'
        value: 1
        tags: ['env:production', 'service:odoo']
```

**New Relic:**
```bash
# Add deployment marker
- script: |
    curl -X POST 'https://api.newrelic.com/v2/applications/$(NEW_RELIC_APP_ID)/deployments.json' \
      -H 'X-Api-Key:$(NEWRELIC_API_KEY)' \
      -H 'Content-Type: application/json' \
      -d '{
        "deployment": {
          "revision": "$(Build.BuildId)",
          "description": "Odoo Microservices Deployment"
        }
      }'
```

---

## 9. Security & Compliance

### 9.1 Enable Credential Scanning

```yaml
# Add to pipeline
- task: CredScan@3
  displayName: 'Scan for credentials'
  inputs:
    outputFormat: 'sarif'
    debugMode: false
```

### 9.2 Compliance Automation

```yaml
# Add compliance checks
- task: ComponentGovernanceComponentDetection@0
  displayName: 'Component Detection'
  inputs:
    scanType: 'Register'
    verbosity: 'Verbose'
    alertWarningLevel: 'High'
```

### 9.3 Audit Logging

Enable in **Organization Settings**:
- Audit log retention: 90 days
- Export to Azure Monitor
- Alert on sensitive operations

---

## 10. Performance Optimization

### 10.1 Pipeline Caching

```yaml
# Add to pipelines
- task: Cache@2
  displayName: 'Cache pip packages'
  inputs:
    key: 'python | "$(Agent.OS)" | requirements.txt'
    path: $(PIP_CACHE_DIR)

- task: Cache@2
  displayName: 'Cache Docker layers'
  inputs:
    key: 'docker | "$(Agent.OS)" | **/Dockerfile'
    path: /var/lib/docker
```

### 10.2 Parallel Jobs

Enable in **Organization Settings** → **Parallel jobs**:
- Microsoft-hosted: 10 parallel jobs
- Self-hosted: Unlimited

### 10.3 Self-Hosted Agents

For better performance, set up self-hosted agents:
```bash
# Install agent
mkdir /opt/azuredevops-agent && cd /opt/azuredevops-agent
wget https://vstsagentpackage.azureedge.net/agent/2.217.0/vsts-agent-linux-x64-2.217.0.tar.gz
tar zxvf vsts-agent-linux-x64-2.217.0.tar.gz
./config.sh
./svc.sh install
./svc.sh start
```

---

## Quick Reference

### Essential Commands

```bash
# Login to Azure DevOps CLI
az devops login --organization https://dev.azure.com/YOUR_ORG

# List pipelines
az pipelines list --organization https://dev.azure.com/YOUR_ORG --project Odoo-Microservices

# Run pipeline
az pipelines run --name microservices-pipeline.yml --organization https://dev.azure.com/YOUR_ORG --project Odoo-Microservices

# List work items
az boards work-item list --project Odoo-Microservices

# Create work item
az boards work-item create --title "New Task" --type Task --project Odoo-Microservices
```

### Troubleshooting

**Pipeline fails to start:**
```bash
# Check service connections
az devops service-endpoint list --organization https://dev.azure.com/YOUR_ORG --project Odoo-Microservices

# Verify variable groups
az pipelines variable-group list --organization https://dev.azure.com/YOUR_ORG --project Odoo-Microservices
```

**Cannot connect to Kubernetes:**
```bash
# Test connection
kubectl config use-context dev-cluster
kubectl cluster-info
kubectl get nodes
```

---

## Next Steps

1. ✅ Complete service connections setup
2. ✅ Configure all variable groups
3. ✅ Create and configure environments
4. ✅ Set up branch policies
5. ✅ Create custom dashboards
6. ✅ Configure external integrations
7. ✅ Run first pipeline
8. ✅ Monitor and optimize

**Documentation:** Keep this guide updated as your setup evolves.
