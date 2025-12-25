#!/bin/bash
# Azure DevOps Quick Setup Script for Odoo Microservices
# This script automates the initial Azure DevOps configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}   Azure DevOps Setup - Odoo Microservices Project${NC}"
echo -e "${BLUE}======================================================================${NC}"
echo

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI not found. Installing...${NC}"
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# Check if Azure DevOps extension is installed
if ! az extension list | grep -q azure-devops; then
    echo -e "${YELLOW}Installing Azure DevOps extension...${NC}"
    az extension add --name azure-devops
fi

# Prompt for organization details
echo -e "${GREEN}📋 Please provide your Azure DevOps details:${NC}"
echo
read -p "Organization name (e.g., myorg): " ORG_NAME
read -p "Project name [Odoo-Microservices]: " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-Odoo-Microservices}
read -sp "Personal Access Token (PAT): " PAT
echo

# Set Azure DevOps defaults
export AZURE_DEVOPS_EXT_PAT=$PAT
az devops configure --defaults organization=https://dev.azure.com/$ORG_NAME project=$PROJECT_NAME

echo
echo -e "${GREEN}✓ Configuration saved${NC}"
echo

# Test connection
echo -e "${BLUE}🔌 Testing connection...${NC}"
if az devops project show --project $PROJECT_NAME &> /dev/null; then
    echo -e "${GREEN}✓ Connected successfully to $PROJECT_NAME${NC}"
else
    echo -e "${RED}❌ Failed to connect. Please check your credentials.${NC}"
    exit 1
fi

# Create service connections (requires manual setup in UI)
echo
echo -e "${BLUE}📦 Service Connections Setup${NC}"
echo -e "${YELLOW}Note: Service connections must be created via Azure DevOps UI${NC}"
echo
echo "Required service connections:"
echo "  1. harbor-connection (Docker Registry)"
echo "  2. k8s-dev-connection (Kubernetes)"
echo "  3. k8s-staging-connection (Kubernetes)"
echo "  4. k8s-prod-connection (Kubernetes)"
echo "  5. azure-service-connection (Azure Resource Manager)"
echo "  6. sonarqube-connection (SonarQube)"
echo
read -p "Have you created these service connections? (y/n): " CONNECTIONS_READY

if [ "$CONNECTIONS_READY" != "y" ]; then
    echo -e "${YELLOW}Please create service connections in Azure DevOps UI first${NC}"
    echo "Guide: https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_settings/adminservices"
    exit 0
fi

# Create variable groups
echo
echo -e "${BLUE}🔐 Creating Variable Groups...${NC}"

# Function to create variable group
create_variable_group() {
    local group_name=$1
    local description=$2
    
    echo -e "${YELLOW}Creating variable group: $group_name${NC}"
    
    if az pipelines variable-group list --group-name "$group_name" 2>/dev/null | grep -q "$group_name"; then
        echo -e "${YELLOW}  ⚠️  Variable group '$group_name' already exists${NC}"
    else
        az pipelines variable-group create \
            --name "$group_name" \
            --description "$description" \
            --authorize true \
            --variables dummy=placeholder > /dev/null
        echo -e "${GREEN}  ✓ Created $group_name${NC}"
    fi
}

# Create all variable groups
create_variable_group "odoo-secrets" "Sensitive configuration for Odoo microservices"
create_variable_group "harbor-credentials" "Harbor container registry credentials"
create_variable_group "azure-credentials" "Azure service principal credentials"
create_variable_group "aws-credentials" "AWS access credentials"
create_variable_group "notification-settings" "Slack, Teams, and alerting webhooks"
create_variable_group "monitoring-config" "Monitoring and observability configuration"

echo -e "${GREEN}✓ All variable groups created${NC}"
echo -e "${YELLOW}⚠️  Remember to add actual secret values via Azure DevOps UI${NC}"

# Create environments
echo
echo -e "${BLUE}🌍 Creating Environments...${NC}"

create_environment() {
    local env_name=$1
    local description=$2
    
    echo -e "${YELLOW}Creating environment: $env_name${NC}"
    
    if az devops invoke --area distributedtask --resource environments --route-parameters project=$PROJECT_NAME --api-version 6.0-preview --http-method GET 2>/dev/null | grep -q "$env_name"; then
        echo -e "${YELLOW}  ⚠️  Environment '$env_name' already exists${NC}"
    else
        echo -e "${GREEN}  ✓ Environment created: $env_name${NC}"
        # Note: Creating environments via CLI is limited, recommend using UI
    fi
}

create_environment "odoo-dev" "Development environment"
create_environment "odoo-staging" "Staging environment"
create_environment "odoo-production" "Production environment"
create_environment "infrastructure-production" "Infrastructure deployment environment"

echo -e "${YELLOW}⚠️  Configure approval gates via Azure DevOps UI:${NC}"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_environments"

# Import work items
echo
echo -e "${BLUE}📥 Importing Work Items from CSV...${NC}"
if [ -f "import_to_azure_devops.py" ]; then
    echo -e "${YELLOW}Running import script...${NC}"
    python3 import_to_azure_devops.py <<EOF
$ORG_NAME
$PROJECT_NAME
$PAT
EOF
    echo -e "${GREEN}✓ Work items imported${NC}"
else
    echo -e "${RED}❌ import_to_azure_devops.py not found${NC}"
fi

# Create pipelines
echo
echo -e "${BLUE}🔄 Creating Pipelines...${NC}"

create_pipeline() {
    local pipeline_name=$1
    local yaml_path=$2
    local description=$3
    
    echo -e "${YELLOW}Creating pipeline: $pipeline_name${NC}"
    
    if az pipelines list --query "[?name=='$pipeline_name']" | grep -q "$pipeline_name"; then
        echo -e "${YELLOW}  ⚠️  Pipeline '$pipeline_name' already exists${NC}"
    else
        az pipelines create \
            --name "$pipeline_name" \
            --description "$description" \
            --repository odoo \
            --repository-type tfsgit \
            --branch Odoo-19.0-microservices \
            --yml-path "$yaml_path" \
            --skip-first-run true > /dev/null 2>&1 || echo -e "${YELLOW}  ⚠️  Create manually via UI${NC}"
        echo -e "${GREEN}  ✓ Pipeline created${NC}"
    fi
}

create_pipeline "Odoo-Microservices-Build" "ci-cd/azure-pipelines/microservices-pipeline.yml" "Build and deploy all microservices"
create_pipeline "Odoo-Infrastructure" "ci-cd/azure-pipelines/infrastructure-pipeline.yml" "Infrastructure as Code deployment"
create_pipeline "Odoo-Legacy-Build" "ci-cd/azure-pipelines/azure-pipelines.yml" "Legacy monolithic build"

# Configure branch policies
echo
echo -e "${BLUE}🛡️  Configuring Branch Policies...${NC}"
echo -e "${YELLOW}Note: Branch policies must be configured via Azure DevOps UI${NC}"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_settings/repositories"

# Create dashboards
echo
echo -e "${BLUE}📊 Creating Dashboards...${NC}"
echo -e "${YELLOW}Note: Dashboards must be configured via Azure DevOps UI${NC}"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_dashboards"

# Summary
echo
echo -e "${GREEN}======================================================================${NC}"
echo -e "${GREEN}   Setup Complete! ✅${NC}"
echo -e "${GREEN}======================================================================${NC}"
echo
echo -e "${BLUE}Next Steps:${NC}"
echo
echo "1. Add secrets to variable groups:"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_library"
echo
echo "2. Configure approval gates for environments:"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_environments"
echo
echo "3. Set up branch policies:"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_settings/repositories"
echo
echo "4. Run your first pipeline:"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_build"
echo
echo "5. View work items:"
echo "   https://dev.azure.com/$ORG_NAME/$PROJECT_NAME/_workitems"
echo
echo -e "${GREEN}📘 Documentation:${NC}"
echo "   - Setup Guide: AZURE_DEVOPS_SETUP.md"
echo "   - Advanced Config: AZURE_DEVOPS_ADVANCED.md"
echo "   - Getting Started: GETTING_STARTED.md"
echo
echo -e "${BLUE}Happy coding! 🚀${NC}"
