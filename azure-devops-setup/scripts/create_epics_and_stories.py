#!/usr/bin/env python3
"""
Azure DevOps - Epics and User Stories Creator
==============================================
This script creates Epics and User Stories for the Odoo Microservices project
and links them to existing tasks.

Usage:
    python3 create_epics_and_stories.py

Prerequisites:
    - Tasks already imported (298 tasks)
    - Environment variables set in .azure_devops.env
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Optional
import time

class AzureDevOpsStructureCreator:
    """Creates and manages Azure DevOps work item hierarchy."""
    
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.auth = HTTPBasicAuth('', pat)
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.api_version = "7.0"
        
        # Storage for created work item IDs
        self.epics = {}  # {phase_id: epic_work_item_id}
        self.stories = {}  # {story_id: story_work_item_id}
        self.tasks = {}  # {task_id: task_work_item_id}
    
    def test_connection(self) -> bool:
        """Test connection to Azure DevOps."""
        url = f"https://dev.azure.com/{self.organization}/_apis/projects?api-version={self.api_version}"
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                print(f"✓ Connected to Azure DevOps organization: {self.organization}")
                return True
            else:
                print(f"✗ Connection failed: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def get_existing_tasks(self) -> Dict[str, int]:
        """Fetch all existing tasks and map task title to work_item_id."""
        print("\n📥 Fetching existing tasks...")
        
        # Use WIQL (Work Item Query Language) to get all tasks
        url = f"{self.base_url}/wit/wiql?api-version={self.api_version}"
        
        query = {
            "query": """
                SELECT [System.Id], [System.Title]
                FROM WorkItems
                WHERE [System.WorkItemType] = 'Task'
                AND [System.TeamProject] = @project
                ORDER BY [System.Id]
            """
        }
        
        try:
            response = requests.post(url, json=query, auth=self.auth)
            response.raise_for_status()
            
            work_items = response.json().get('workItems', [])
            print(f"✓ Found {len(work_items)} tasks")
            
            # Fetch details in batches of 50 to avoid URL length issues
            tasks_map = {}
            if work_items:
                batch_size = 50
                for i in range(0, len(work_items), batch_size):
                    batch = work_items[i:i + batch_size]
                    ids = ','.join([str(wi['id']) for wi in batch])
                    details_url = f"{self.base_url}/wit/workitems?ids={ids}&api-version={self.api_version}"
                    
                    details_response = requests.get(details_url, auth=self.auth)
                    details_response.raise_for_status()
                    
                    for item in details_response.json().get('value', []):
                        title = item['fields']['System.Title']
                        work_item_id = item['id']
                        
                        # Map by exact title (tasks were imported without IDs in title)
                        tasks_map[title] = work_item_id
                    
                    time.sleep(0.1)  # Rate limiting
                
                print(f"✓ Mapped {len(tasks_map)} tasks by title")
            
            return tasks_map
            
        except Exception as e:
            print(f"✗ Error fetching tasks: {e}")
            return {}
    
    def create_epic(self, title: str, description: str, tags: List[str], 
                    priority: int = 1, iteration: str = None) -> Optional[int]:
        """Create an Epic work item."""
        # Agile template uses "Epic", Basic uses "Epic", Scrum uses "Epic"
        url = f"{self.base_url}/wit/workitems/$Epic?api-version={self.api_version}"
        
        operations = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/System.Description", "value": description},
            {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority},
            {"op": "add", "path": "/fields/System.Tags", "value": ";".join(tags)},
        ]
        
        # Skip iteration for now - can be set manually later
        # if iteration:
        #     operations.append({
        #         "op": "add",
        #         "path": "/fields/System.IterationPath",
        #         "value": f"{self.project}\\{iteration}"
        #     })
        
        try:
            response = requests.post(
                url, 
                json=operations,
                auth=self.auth,
                headers={"Content-Type": "application/json-patch+json"}
            )
            response.raise_for_status()
            work_item_id = response.json()['id']
            print(f"  ✓ Created Epic: {title} (ID: {work_item_id})")
            return work_item_id
        except Exception as e:
            print(f"  ✗ Failed to create Epic '{title}': {e}")
            if hasattr(e, 'response') and e.response:
                print(f"    Response: {e.response.text}")
            return None
    
    def create_user_story(self, title: str, description: str, parent_id: int,
                         tags: List[str], story_points: int = 3, 
                         priority: int = 2) -> Optional[int]:
        """Create a User Story work item."""
        url = f"{self.base_url}/wit/workitems/$User Story?api-version={self.api_version}"
        
        operations = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/System.Description", "value": description},
            {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints", "value": story_points},
            {"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority},
            {"op": "add", "path": "/fields/System.Tags", "value": ";".join(tags)},
        ]
        
        try:
            response = requests.post(
                url,
                json=operations,
                auth=self.auth,
                headers={"Content-Type": "application/json-patch+json"}
            )
            response.raise_for_status()
            story_id = response.json()['id']
            
            # Link to parent Epic
            self.link_work_items(story_id, parent_id, "System.LinkTypes.Hierarchy-Reverse")
            
            print(f"    ✓ Created Story: {title} (ID: {story_id})")
            return story_id
        except Exception as e:
            print(f"    ✗ Failed to create Story '{title}': {e}")
            if hasattr(e, 'response') and e.response:
                print(f"      Response: {e.response.text}")
            return None
    
    def link_work_items(self, source_id: int, target_id: int, link_type: str) -> bool:
        """Link two work items together."""
        url = f"{self.base_url}/wit/workitems/{source_id}?api-version={self.api_version}"
        
        operations = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": link_type,
                    "url": f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workItems/{target_id}"
                }
            }
        ]
        
        try:
            response = requests.patch(
                url,
                json=operations,
                auth=self.auth,
                headers={"Content-Type": "application/json-patch+json"}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            # Silently fail for already linked items
            return False
    
    def get_task_id_to_title_mapping(self) -> Dict[str, str]:
        """Map task IDs (e.g., '0.1.1') to their actual titles from CHECKLIST.md."""
        return {
            # Phase 0: Microservices Design
            "0.1.1": "Documented 11 microservices",
            "0.1.2": "Created service boundary diagram",
            "0.1.3": "Defined service responsibilities",
            
            "0.2.1": "Designed auth-db schema",
            "0.2.2": "Designed core-erp-db schema",
            "0.2.3": "Designed accounting-db schema",
            "0.2.4": "Designed inventory-db schema",
            "0.2.5": "Designed crm-db schema",
            
            "0.3.1": "Chose REST for synchronous calls",
            "0.3.2": "Chose RabbitMQ for async events",
            "0.3.3": "Defined event types list",
            
            "0.4.1": "Created microservices/ directory",
            "0.4.2": "Created subdirectories for all 11 services",
            "0.4.3": "Created shared/ library directory",
            
            "0.5.1": "Created auth-service OpenAPI spec",
            "0.5.2": "Created core-erp OpenAPI spec",
            "0.5.3": "Created accounting OpenAPI spec",
            "0.5.4": "Created inventory OpenAPI spec",
            "0.5.5": "Created crm OpenAPI spec",
            
            "0.6.1": "Documented auth-service dependencies",
            "0.6.2": "Documented core-erp dependencies",
            "0.6.3": "Documented accounting dependencies",
            "0.6.4": "Documented inventory dependencies",
            "0.6.5": "Created dependency diagram",
            
            # Phase 1: Service Mesh Setup
            "1.1.1": "Downloaded Istio 1.20+",
            "1.1.2": "Installed istioctl CLI",
            "1.1.3": "Ran istio install --set profile=demo",
            "1.1.4": "Verified installation with kubectl",
            
            "1.2.1": "Installed Prometheus",
            "1.2.2": "Installed Grafana",
            "1.2.3": "Installed Jaeger",
            "1.2.4": "Installed Kiali",
            "1.2.5": "Accessed Kiali dashboard",
            
            "1.3.1": "Created VirtualService for auth",
            "1.3.2": "Created VirtualService for core-erp",
            "1.3.3": "Created VirtualService for accounting",
            "1.3.4": "Created Gateway configuration",
            
            "1.4.1": "Created DestinationRule for circuit breakers",
            "1.4.2": "Configured retry policies",
            "1.4.3": "Configured timeout policies",
            
            "1.5.1": "Enabled strict mTLS",
            "1.5.2": "Verified mTLS is working",
            "1.5.3": "Tested service-to-service encryption",
            
            "1.6.1": "Deployed test services",
            "1.6.2": "Verified routing works",
            "1.6.3": "Checked Kiali for service topology",
            
            # Phase 2: Core Services Development
            "2.1.1": "Created FastAPI app structure",
            "2.1.2": "Implemented JWT authentication",
            "2.1.3": "Implemented OAuth2 login endpoint",
            "2.1.4": "Created auth-db PostgreSQL",
            "2.1.5": "Ran database migrations",
            "2.1.6": "Created Dockerfile",
            "2.1.7": "Built Docker image",
            "2.1.8": "Tested locally with curl",
            "2.1.9": "Added to docker-compose.yml",
            
            "2.2.1": "Created FastAPI app structure",
            "2.2.2": "Implemented partner management",
            "2.2.3": "Implemented company management",
            "2.2.4": "Implemented user management",
            "2.2.5": "Created core-erp-db PostgreSQL",
            "2.2.6": "Ran database migrations",
            "2.2.7": "Created Dockerfile",
            "2.2.8": "Built Docker image",
            "2.2.9": "Integrated with auth-service",
            
            "2.3.1": "Created FastAPI app structure",
            "2.3.2": "Implemented invoice endpoints",
            "2.3.3": "Implemented payment endpoints",
            "2.3.4": "Implemented journal entries",
            "2.3.5": "Created accounting-db PostgreSQL",
            "2.3.6": "Ran database migrations",
            "2.3.7": "Created Dockerfile",
            "2.3.8": "Built Docker image",
            "2.3.9": "Connected to event bus",
            
            "2.4.1": "Created FastAPI app structure",
            "2.4.2": "Implemented product endpoints",
            "2.4.3": "Implemented stock management",
            "2.4.4": "Implemented warehouse endpoints",
            "2.4.5": "Created inventory-db PostgreSQL",
            "2.4.6": "Ran database migrations",
            "2.4.7": "Created Dockerfile",
            "2.4.8": "Built Docker image",
            "2.4.9": "Connected to event bus",
            
            "2.5.1": "Created FastAPI app structure",
            "2.5.2": "Implemented lead endpoints",
            "2.5.3": "Implemented opportunity endpoints",
            "2.5.4": "Implemented pipeline views",
            "2.5.5": "Created crm-db PostgreSQL",
            "2.5.6": "Ran database migrations",
            "2.5.7": "Created Dockerfile",
            "2.5.8": "Built Docker image",
            
            # Phase 3: Event Bus & Messaging
            "3.1.1": "Installed RabbitMQ container",
            "3.1.2": "Configured management UI",
            "3.1.3": "Created exchanges and queues",
            "3.1.4": "Tested connection",
            
            "3.2.1": "Defined UserCreated event",
            "3.2.2": "Defined OrderPlaced event",
            "3.2.3": "Defined InvoiceGenerated event",
            "3.2.4": "Defined InventoryUpdated event",
            "3.2.5": "Defined PaymentReceived event",
            
            "3.3.1": "Implemented publisher in auth-service",
            "3.3.2": "Implemented publisher in accounting-service",
            "3.3.3": "Implemented publisher in inventory-service",
            "3.3.4": "Tested event publishing",
            
            "3.4.1": "Implemented consumer in accounting-service",
            "3.4.2": "Implemented consumer in inventory-service",
            "3.4.3": "Implemented consumer in notification-service",
            "3.4.4": "Tested event consumption",
            
            "3.5.1": "End-to-end event flow test",
            "3.5.2": "Checked RabbitMQ logs",
            "3.5.3": "Verified event delivery",
            
            # Phase 4: Observability Stack
            "4.1.1": "Installed Prometheus",
            "4.1.2": "Configured service discovery",
            "4.1.3": "Added scrape configs for all services",
            "4.1.4": "Tested metrics collection",
            
            "4.2.1": "Installed Grafana",
            "4.2.2": "Connected to Prometheus",
            "4.2.3": "Created auth-service dashboard",
            "4.2.4": "Created accounting-service dashboard",
            "4.2.5": "Created inventory-service dashboard",
            "4.2.6": "Set up alert rules",
            
            "4.3.1": "Installed Jaeger",
            "4.3.2": "Configured tracing endpoints",
            "4.3.3": "Tested trace collection",
            
            "4.4.1": "Added OpenTelemetry to auth-service",
            "4.4.2": "Added OpenTelemetry to core-erp",
            "4.4.3": "Added OpenTelemetry to accounting",
            "4.4.4": "Verified distributed traces",
            
            "4.5.1": "Installed Fluentd",
            "4.5.2": "Installed Elasticsearch",
            "4.5.3": "Installed Kibana",
            "4.5.4": "Configured log aggregation",
            "4.5.5": "Created log dashboards",
            
            # Phase 5: API Gateway & Security
            "5.1.1": "Installed Kong API Gateway",
            "5.1.2": "Configured Kong Admin API",
            "5.1.3": "Created service routes",
            
            "5.2.1": "Installed OAuth2 plugin",
            "5.2.2": "Configured with auth-service",
            "5.2.3": "Tested token validation",
            
            "5.3.1": "Configured rate limits per service",
            "5.3.2": "Tested rate limiting",
            "5.3.3": "Set up different tiers",
            
            "5.4.1": "Enabled CORS",
            "5.4.2": "Configured allowed origins",
            "5.4.3": "Tested CORS headers",
            
            "5.5.1": "Set up Kong Dev Portal",
            "5.5.2": "Uploaded OpenAPI specs",
            "5.5.3": "Published documentation",
            
            "5.6.1": "Installed Locust",
            "5.6.2": "Created load test scenarios",
            "5.6.3": "Ran performance tests",
            "5.6.4": "Analyzed results",
            
            # Phase 6: Container Registry
            "6.1.1": "Installed Harbor",
            "6.1.2": "Configured HTTPS",
            "6.1.3": "Created project repositories",
            
            "6.2.1": "Enabled Trivy scanner",
            "6.2.2": "Scanned all images",
            "6.2.3": "Fixed critical vulnerabilities",
            
            "6.3.1": "Configured replication rules",
            "6.3.2": "Set up multi-region replication",
            "6.3.3": "Tested replication",
            
            "6.4.1": "Pushed auth-service image",
            "6.4.2": "Pushed core-erp image",
            "6.4.3": "Pushed accounting image",
            "6.4.4": "Pushed inventory image",
            "6.4.5": "Pushed crm image",
            
            # Phase 7: GitOps with ArgoCD
            "7.1.1": "Installed ArgoCD",
            "7.1.2": "Accessed ArgoCD UI",
            "7.1.3": "Changed admin password",
            
            "7.2.1": "Created k8s-manifests repo",
            "7.2.2": "Organized by environment",
            "7.2.3": "Created kustomization files",
            
            "7.3.1": "Created ArgoCD app for auth-service",
            "7.3.2": "Created ArgoCD app for core-erp",
            "7.3.3": "Created ArgoCD app for accounting",
            "7.3.4": "Created ArgoCD app for inventory",
            
            "7.4.1": "Enabled auto-sync",
            "7.4.2": "Configured pruning",
            "7.4.3": "Set up self-heal",
            
            "7.5.1": "Created dev environment",
            "7.5.2": "Created staging environment",
            "7.5.3": "Created prod environment",
            
            # Phase 8: CI/CD Pipeline
            "8.1.1": "Created workflow file",
            "8.1.2": "Configured multi-service build",
            "8.1.3": "Tested build pipeline",
            
            "8.2.1": "Added unit test step",
            "8.2.2": "Added integration test step",
            "8.2.3": "Configured test reporting",
            
            "8.3.1": "Integrated Trivy scanning",
            "8.3.2": "Integrated SonarQube",
            "8.3.3": "Configured security gates",
            
            "8.4.1": "Build images on merge",
            "8.4.2": "Push to Harbor registry",
            "8.4.3": "Tag with version + SHA",
            
            "8.5.1": "Trigger ArgoCD sync after push",
            "8.5.2": "Wait for deployment health",
            "8.5.3": "Send notifications",
            
            "8.6.1": "Configured auto-rollback",
            "8.6.2": "Tested rollback scenario",
            "8.6.3": "Documented rollback process",
            
            # Phase 9: Cloud Infrastructure
            "9.1.1": "Created/configured AWS account",
            "9.1.2": "Set up IAM roles",
            "9.1.3": "Configured billing alerts",
            
            "9.2.1": "Created VPC with Terraform",
            "9.2.2": "Configured subnets",
            "9.2.3": "Set up NAT Gateway",
            "9.2.4": "Configured security groups",
            
            "9.3.1": "Created EKS cluster with Terraform",
            "9.3.2": "Configured 3-node node group",
            "9.3.3": "Installed cluster autoscaler",
            "9.3.4": "Configured kubectl access",
            
            "9.4.1": "Created RDS instances for services",
            "9.4.2": "Configured Multi-AZ",
            "9.4.3": "Set up automated backups",
            "9.4.4": "Configured security groups",
            
            "9.5.1": "Created Redis cluster",
            "9.5.2": "Configured cluster mode",
            "9.5.3": "Set up security groups",
            
            "9.6.1": "Created S3 buckets for file storage",
            "9.6.2": "Configured bucket policies",
            "9.6.3": "Enabled versioning",
            
            "9.7.1": "Created Application Load Balancer",
            "9.7.2": "Configured target groups",
            "9.7.3": "Set up health checks",
            
            "9.8.1": "Configured DNS records",
            "9.8.2": "Set up SSL certificates",
            "9.8.3": "Configured HTTPS",
            
            "9.9.1": "Deployed all services to EKS",
            "9.9.2": "Verified all pods running",
            "9.9.3": "Checked service connectivity",
            
            "9.10.1": "Full system smoke test",
            "9.10.2": "Load testing in production",
            "9.10.3": "Security validation",
            
            # Testing & Validation
            "T.1": "Unit Tests - All Services",
            "T.2": "Integration Tests",
            "T.3.1": "Login workflow test",
            "T.3.2": "Invoice creation workflow test",
            "T.3.3": "Inventory workflow test",
            "T.4.1": "Baseline performance test",
            "T.4.2": "Load test with 100 concurrent users",
            "T.4.3": "Stress test to find limits",
            "T.5.1": "API security scan",
            "T.5.2": "Network security audit",
            "T.5.3": "Penetration test",
            
            # Final Validation
            "FV.1": "Users can login via auth-service",
            "FV.2": "Can create partners in core-erp",
            "FV.3": "Can create invoices in accounting",
            "FV.4": "Can manage products in inventory",
            "FV.5": "All databases storing data",
            "FV.6": "Services communicate via REST",
            "FV.7": "Events flowing through RabbitMQ",
            "FV.8": "API Gateway routing correctly",
            "FV.9": "Prometheus collecting metrics",
            "FV.10": "Grafana showing dashboards",
            "FV.11": "Distributed tracing working",
            "FV.12": "Istio mTLS enabled",
            "FV.13": "Services auto-restart on failure",
            "FV.14": "Load balancer distributing traffic",
            "FV.15": "All images in Harbor",
            "FV.16": "Services deployed to Kubernetes",
            "FV.17": "ArgoCD auto-syncing",
            "FV.18": "CI/CD pipeline working",
            "FV.19": "Can rollback deployments",
            
            # Additional Services
            "A.1.1": "Created FastAPI app structure for HR",
            "A.1.2": "Implemented employee endpoints",
            "A.1.3": "Implemented payroll endpoints",
            "A.1.4": "Implemented attendance tracking",
            "A.1.5": "Created hr-db PostgreSQL",
            "A.1.6": "Created Dockerfile and deployed",
            
            "A.2.1": "Created FastAPI app structure for Sales",
            "A.2.2": "Implemented order endpoints",
            "A.2.3": "Implemented quotation endpoints",
            "A.2.4": "Implemented customer management",
            "A.2.5": "Created sales-db PostgreSQL",
            "A.2.6": "Created Dockerfile and deployed",
            
            "A.3.1": "Created FastAPI app structure for Reporting",
            "A.3.2": "Implemented analytics endpoints",
            "A.3.3": "Implemented dashboard endpoints",
            "A.3.4": "Implemented report generation",
            "A.3.5": "Integrated with Pandas",
            "A.3.6": "Created Dockerfile and deployed",
            
            "A.4.1": "Created FastAPI app structure for Notification",
            "A.4.2": "Implemented email notification",
            "A.4.3": "Implemented SMS notification",
            "A.4.4": "Implemented push notification",
            "A.4.5": "Connected to event bus",
            "A.4.6": "Created Dockerfile and deployed",
            
            "A.5.1": "Created FastAPI app structure for File Storage",
            "A.5.2": "Implemented file upload endpoints",
            "A.5.3": "Implemented S3 integration",
            "A.5.4": "Implemented file retrieval",
            "A.5.5": "Implemented file deletion",
            "A.5.6": "Created Dockerfile and deployed",
            
            "A.6.1": "Created FastAPI app structure for Workflow",
            "A.6.2": "Implemented cron job scheduler",
            "A.6.3": "Implemented automation rules",
            "A.6.4": "Implemented workflow engine",
            "A.6.5": "Integrated with all services",
            "A.6.6": "Created Dockerfile and deployed",
        }
    
    def link_tasks_to_story(self, story_id: int, task_ids: List[str], 
                           tasks_map: Dict[str, int]) -> int:
        """Link tasks to a user story using task ID to title mapping."""
        # Map task IDs to actual task titles from CHECKLIST.md
        task_id_to_title = self.get_task_id_to_title_mapping()
        
        linked_count = 0
        for task_id in task_ids:
            # Convert task ID (e.g., "0.1.1") to task title
            task_title = task_id_to_title.get(task_id)
            if task_title and task_title in tasks_map:
                task_work_item_id = tasks_map[task_title]
                if self.link_work_items(task_work_item_id, story_id, 
                                       "System.LinkTypes.Hierarchy-Reverse"):
                    linked_count += 1
                time.sleep(0.1)  # Rate limiting
        return linked_count
    
    def create_all_epics(self) -> Dict[str, int]:
        """Create all phase Epics."""
        print("\n🔨 Creating Epics...")
        
        epics_data = [
            {
                "id": "Phase-0",
                "title": "Phase 0: Microservices Design (Days 1-5)",
                "description": """<h2>Phase 0: Microservices Design</h2>
<p>Design and architecture phase for Odoo microservices system.</p>
<h3>Objectives:</h3>
<ul>
<li>Domain-Driven Design</li>
<li>Database Per Service Pattern</li>
<li>Inter-Service Communication</li>
<li>Service Directory Structure</li>
<li>Define Service APIs</li>
<li>Service Dependencies Matrix</li>
</ul>
<p><strong>Duration:</strong> 5 days</p>
<p><strong>Deliverables:</strong> Complete architecture documentation and service boundaries</p>""",
                "tags": ["Phase-0", "Design", "Architecture"],
                "iteration": "Sprint 1"
            },
            {
                "id": "Phase-1",
                "title": "Phase 1: Service Mesh Setup (Days 6-10)",
                "description": """<h2>Phase 1: Service Mesh Setup</h2>
<p>Set up Istio service mesh for microservices communication.</p>
<h3>Objectives:</h3>
<ul>
<li>Install Istio</li>
<li>Install Kiali Dashboard</li>
<li>Configure Traffic Management</li>
<li>Configure Resilience</li>
<li>mTLS Configuration</li>
<li>Service Mesh Testing</li>
</ul>
<p><strong>Duration:</strong> 5 days</p>""",
                "tags": ["Phase-1", "Istio", "Infrastructure"],
                "iteration": "Sprint 1"
            },
            {
                "id": "Phase-2",
                "title": "Phase 2: Core Services Development (Days 11-18)",
                "description": """<h2>Phase 2: Core Services Development</h2>
<p>Develop the 5 core microservices that form the MVP.</p>
<h3>Services:</h3>
<ul>
<li>Auth Service</li>
<li>Core ERP Service</li>
<li>Accounting Service</li>
<li>Inventory Service</li>
<li>CRM Service</li>
</ul>
<p><strong>Duration:</strong> 8 days</p>
<p><strong>Goal:</strong> MVP Ready</p>""",
                "tags": ["Phase-2", "Development", "MVP"],
                "iteration": "Sprint 2"
            },
            {
                "id": "Phase-3",
                "title": "Phase 3: Event Bus & Messaging (Days 19-22)",
                "description": """<h2>Phase 3: Event Bus & Messaging</h2>
<p>Implement asynchronous communication using RabbitMQ.</p>
<h3>Components:</h3>
<ul>
<li>RabbitMQ Installation</li>
<li>Event Schema Definition</li>
<li>Event Publishers</li>
<li>Event Consumers</li>
<li>Event Testing</li>
</ul>
<p><strong>Duration:</strong> 4 days</p>""",
                "tags": ["Phase-3", "Messaging", "RabbitMQ"],
                "iteration": "Sprint 3"
            },
            {
                "id": "Phase-4",
                "title": "Phase 4: Observability Stack (Days 23-26)",
                "description": """<h2>Phase 4: Observability Stack</h2>
<p>Set up monitoring, logging, and tracing infrastructure.</p>
<h3>Components:</h3>
<ul>
<li>Prometheus for metrics</li>
<li>Grafana for dashboards</li>
<li>Jaeger for tracing</li>
<li>OpenTelemetry integration</li>
<li>EFK Stack (Elasticsearch, Fluentd, Kibana)</li>
</ul>
<p><strong>Duration:</strong> 4 days</p>""",
                "tags": ["Phase-4", "Monitoring", "Observability"],
                "iteration": "Sprint 3"
            },
            {
                "id": "Phase-5",
                "title": "Phase 5: API Gateway & Security (Days 27-30)",
                "description": """<h2>Phase 5: API Gateway & Security</h2>
<p>Implement Kong API Gateway with security features.</p>
<h3>Features:</h3>
<ul>
<li>Kong Installation</li>
<li>OAuth2 Plugin</li>
<li>Rate Limiting</li>
<li>CORS Configuration</li>
<li>API Documentation</li>
<li>Load Testing</li>
</ul>
<p><strong>Duration:</strong> 4 days</p>""",
                "tags": ["Phase-5", "Gateway", "Security"],
                "iteration": "Sprint 4"
            },
            {
                "id": "Phase-6",
                "title": "Phase 6: Container Registry (Days 31-32)",
                "description": """<h2>Phase 6: Container Registry</h2>
<p>Set up Harbor container registry with security scanning.</p>
<h3>Tasks:</h3>
<ul>
<li>Harbor Installation</li>
<li>Vulnerability Scanning</li>
<li>Image Replication</li>
<li>Push Service Images</li>
</ul>
<p><strong>Duration:</strong> 2 days</p>""",
                "tags": ["Phase-6", "Harbor", "Registry"],
                "iteration": "Sprint 4"
            },
            {
                "id": "Phase-7",
                "title": "Phase 7: GitOps with ArgoCD (Days 33-35)",
                "description": """<h2>Phase 7: GitOps with ArgoCD</h2>
<p>Implement GitOps deployment strategy using ArgoCD.</p>
<h3>Components:</h3>
<ul>
<li>ArgoCD Installation</li>
<li>Repository Structure</li>
<li>Application Definitions</li>
<li>Sync Policies</li>
<li>Multi-Environment Setup</li>
</ul>
<p><strong>Duration:</strong> 3 days</p>""",
                "tags": ["Phase-7", "GitOps", "ArgoCD"],
                "iteration": "Sprint 5"
            },
            {
                "id": "Phase-8",
                "title": "Phase 8: CI/CD Pipeline (Days 36-38)",
                "description": """<h2>Phase 8: CI/CD Pipeline</h2>
<p>Implement automated CI/CD pipeline using GitHub Actions.</p>
<h3>Pipeline Stages:</h3>
<ul>
<li>Build</li>
<li>Test</li>
<li>Security Scanning</li>
<li>Docker Build & Push</li>
<li>ArgoCD Sync</li>
<li>Rollback Strategy</li>
</ul>
<p><strong>Duration:</strong> 3 days</p>""",
                "tags": ["Phase-8", "CICD", "Automation"],
                "iteration": "Sprint 5"
            },
            {
                "id": "Phase-9",
                "title": "Phase 9: Cloud Infrastructure (Days 39-45)",
                "description": """<h2>Phase 9: Cloud Infrastructure</h2>
<p>Deploy to AWS cloud with production-grade infrastructure.</p>
<h3>Infrastructure:</h3>
<ul>
<li>AWS Account Setup</li>
<li>Terraform VPC</li>
<li>EKS Cluster</li>
<li>RDS PostgreSQL</li>
<li>ElastiCache Redis</li>
<li>S3 Buckets</li>
<li>ALB Load Balancer</li>
<li>Route53 DNS</li>
<li>Production Deployment</li>
</ul>
<p><strong>Duration:</strong> 7 days</p>""",
                "tags": ["Phase-9", "AWS", "Production"],
                "iteration": "Sprint 6"
            }
        ]
        
        epics = {}
        for epic_data in epics_data:
            epic_id = self.create_epic(
                title=epic_data["title"],
                description=epic_data["description"],
                tags=epic_data["tags"],
                iteration=epic_data["iteration"]
            )
            if epic_id:
                epics[epic_data["id"]] = epic_id
            time.sleep(0.2)  # Rate limiting
        
        print(f"\n✓ Created {len(epics)} Epics")
        return epics
    
    def create_all_user_stories(self, epics: Dict[str, int], 
                                tasks_map: Dict[str, int]) -> Dict[str, int]:
        """Create all User Stories and link tasks."""
        print("\n🔨 Creating User Stories and linking tasks...")
        
        stories_data = self.get_stories_data()
        stories = {}
        total_linked = 0
        
        for story_data in stories_data:
            phase_key = story_data["phase"]
            if phase_key not in epics:
                print(f"  ⚠ Warning: Epic not found for {phase_key}")
                continue
            
            story_id = self.create_user_story(
                title=story_data["title"],
                description=story_data["description"],
                parent_id=epics[phase_key],
                tags=story_data["tags"],
                story_points=story_data.get("story_points", 3),
                priority=story_data.get("priority", 2)
            )
            
            if story_id:
                stories[story_data["id"]] = story_id
                
                # Link tasks to this story
                if "tasks" in story_data:
                    linked = self.link_tasks_to_story(
                        story_id, 
                        story_data["tasks"],
                        tasks_map
                    )
                    total_linked += linked
                    if linked > 0:
                        print(f"      → Linked {linked} tasks")
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"\n✓ Created {len(stories)} User Stories")
        print(f"✓ Linked {total_linked} tasks to their stories")
        return stories
    
    def get_stories_data(self) -> List[Dict]:
        """Return the complete list of user stories with metadata."""
        return [
            # Phase 0 Stories
            {
                "id": "0.1", "phase": "Phase-0",
                "title": "0.1 Domain-Driven Design",
                "description": "<p>Define service boundaries using domain-driven design principles.</p>",
                "tags": ["Phase-0", "0.1", "Design"],
                "story_points": 3,
                "tasks": ["0.1.1", "0.1.2", "0.1.3"]
            },
            {
                "id": "0.2", "phase": "Phase-0",
                "title": "0.2 Database Per Service Pattern",
                "description": "<p>Design database schemas for each microservice.</p>",
                "tags": ["Phase-0", "0.2", "Database"],
                "story_points": 5,
                "tasks": ["0.2.1", "0.2.2", "0.2.3", "0.2.4", "0.2.5"]
            },
            {
                "id": "0.3", "phase": "Phase-0",
                "title": "0.3 Inter-Service Communication",
                "description": "<p>Define communication patterns between services.</p>",
                "tags": ["Phase-0", "0.3", "Communication"],
                "story_points": 3,
                "tasks": ["0.3.1", "0.3.2", "0.3.3"]
            },
            {
                "id": "0.4", "phase": "Phase-0",
                "title": "0.4 Service Directory Structure",
                "description": "<p>Create project directory structure for all services.</p>",
                "tags": ["Phase-0", "0.4", "Structure"],
                "story_points": 2,
                "tasks": ["0.4.1", "0.4.2", "0.4.3"]
            },
            {
                "id": "0.5", "phase": "Phase-0",
                "title": "0.5 Define Service APIs",
                "description": "<p>Create OpenAPI specifications for all services.</p>",
                "tags": ["Phase-0", "0.5", "API"],
                "story_points": 5,
                "tasks": ["0.5.1", "0.5.2", "0.5.3", "0.5.4", "0.5.5"]
            },
            {
                "id": "0.6", "phase": "Phase-0",
                "title": "0.6 Service Dependencies Matrix",
                "description": "<p>Document dependencies between services.</p>",
                "tags": ["Phase-0", "0.6", "Dependencies"],
                "story_points": 3,
                "tasks": ["0.6.1", "0.6.2", "0.6.3", "0.6.4", "0.6.5"]
            },
            
            # Phase 1 Stories
            {
                "id": "1.1", "phase": "Phase-1",
                "title": "1.1 Install Istio",
                "description": "<p>Install and configure Istio service mesh.</p>",
                "tags": ["Phase-1", "1.1", "Istio"],
                "story_points": 3,
                "tasks": ["1.1.1", "1.1.2", "1.1.3", "1.1.4"]
            },
            {
                "id": "1.2", "phase": "Phase-1",
                "title": "1.2 Install Kiali Dashboard",
                "description": "<p>Set up observability dashboards for service mesh.</p>",
                "tags": ["Phase-1", "1.2", "Kiali"],
                "story_points": 3,
                "tasks": ["1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5"]
            },
            {
                "id": "1.3", "phase": "Phase-1",
                "title": "1.3 Configure Traffic Management",
                "description": "<p>Configure routing and traffic splitting.</p>",
                "tags": ["Phase-1", "1.3", "Traffic"],
                "story_points": 5,
                "tasks": ["1.3.1", "1.3.2", "1.3.3", "1.3.4"]
            },
            {
                "id": "1.4", "phase": "Phase-1",
                "title": "1.4 Configure Resilience",
                "description": "<p>Set up circuit breakers, retries, and timeouts.</p>",
                "tags": ["Phase-1", "1.4", "Resilience"],
                "story_points": 3,
                "tasks": ["1.4.1", "1.4.2", "1.4.3"]
            },
            {
                "id": "1.5", "phase": "Phase-1",
                "title": "1.5 mTLS Configuration",
                "description": "<p>Enable mutual TLS for service-to-service encryption.</p>",
                "tags": ["Phase-1", "1.5", "Security"],
                "story_points": 3,
                "tasks": ["1.5.1", "1.5.2", "1.5.3"]
            },
            {
                "id": "1.6", "phase": "Phase-1",
                "title": "1.6 Service Mesh Testing",
                "description": "<p>Test service mesh functionality.</p>",
                "tags": ["Phase-1", "1.6", "Testing"],
                "story_points": 2,
                "tasks": ["1.6.1", "1.6.2", "1.6.3"]
            },
            
            # Phase 2 Stories
            {
                "id": "2.1", "phase": "Phase-2",
                "title": "2.1 Auth Service",
                "description": "<p>Develop authentication and authorization service.</p>",
                "tags": ["Phase-2", "2.1", "Auth"],
                "story_points": 8,
                "tasks": ["2.1.1", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7", "2.1.8", "2.1.9"]
            },
            {
                "id": "2.2", "phase": "Phase-2",
                "title": "2.2 Core ERP Service",
                "description": "<p>Develop core ERP functionality (partners, companies, users).</p>",
                "tags": ["Phase-2", "2.2", "Core-ERP"],
                "story_points": 8,
                "tasks": ["2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6", "2.2.7", "2.2.8", "2.2.9"]
            },
            {
                "id": "2.3", "phase": "Phase-2",
                "title": "2.3 Accounting Service",
                "description": "<p>Develop accounting and financial management service.</p>",
                "tags": ["Phase-2", "2.3", "Accounting"],
                "story_points": 8,
                "tasks": ["2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.3.8", "2.3.9"]
            },
            {
                "id": "2.4", "phase": "Phase-2",
                "title": "2.4 Inventory Service",
                "description": "<p>Develop inventory and warehouse management service.</p>",
                "tags": ["Phase-2", "2.4", "Inventory"],
                "story_points": 8,
                "tasks": ["2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.4.5", "2.4.6", "2.4.7", "2.4.8", "2.4.9"]
            },
            {
                "id": "2.5", "phase": "Phase-2",
                "title": "2.5 CRM Service",
                "description": "<p>Develop customer relationship management service.</p>",
                "tags": ["Phase-2", "2.5", "CRM"],
                "story_points": 8,
                "tasks": ["2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.5", "2.5.6", "2.5.7", "2.5.8"]
            },
            
            # Phase 3 Stories
            {
                "id": "3.1", "phase": "Phase-3",
                "title": "3.1 RabbitMQ Installation",
                "description": "<p>Install and configure RabbitMQ message broker.</p>",
                "tags": ["Phase-3", "3.1", "RabbitMQ"],
                "story_points": 3,
                "tasks": ["3.1.1", "3.1.2", "3.1.3", "3.1.4"]
            },
            {
                "id": "3.2", "phase": "Phase-3",
                "title": "3.2 Event Schema Definition",
                "description": "<p>Define event schemas for inter-service communication.</p>",
                "tags": ["Phase-3", "3.2", "Events"],
                "story_points": 3,
                "tasks": ["3.2.1", "3.2.2", "3.2.3", "3.2.4", "3.2.5"]
            },
            {
                "id": "3.3", "phase": "Phase-3",
                "title": "3.3 Event Publishers",
                "description": "<p>Implement event publishing in services.</p>",
                "tags": ["Phase-3", "3.3", "Publishers"],
                "story_points": 5,
                "tasks": ["3.3.1", "3.3.2", "3.3.3", "3.3.4"]
            },
            {
                "id": "3.4", "phase": "Phase-3",
                "title": "3.4 Event Consumers",
                "description": "<p>Implement event consumption in services.</p>",
                "tags": ["Phase-3", "3.4", "Consumers"],
                "story_points": 5,
                "tasks": ["3.4.1", "3.4.2", "3.4.3", "3.4.4"]
            },
            {
                "id": "3.5", "phase": "Phase-3",
                "title": "3.5 Event Testing",
                "description": "<p>Test end-to-end event flows.</p>",
                "tags": ["Phase-3", "3.5", "Testing"],
                "story_points": 2,
                "tasks": ["3.5.1", "3.5.2", "3.5.3"]
            },
            
            # Phase 4 Stories
            {
                "id": "4.1", "phase": "Phase-4",
                "title": "4.1 Prometheus Setup",
                "description": "<p>Set up Prometheus for metrics collection.</p>",
                "tags": ["Phase-4", "4.1", "Prometheus"],
                "story_points": 3,
                "tasks": ["4.1.1", "4.1.2", "4.1.3", "4.1.4"]
            },
            {
                "id": "4.2", "phase": "Phase-4",
                "title": "4.2 Grafana Dashboards",
                "description": "<p>Create monitoring dashboards in Grafana.</p>",
                "tags": ["Phase-4", "4.2", "Grafana"],
                "story_points": 5,
                "tasks": ["4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5", "4.2.6"]
            },
            {
                "id": "4.3", "phase": "Phase-4",
                "title": "4.3 Jaeger Tracing",
                "description": "<p>Set up distributed tracing with Jaeger.</p>",
                "tags": ["Phase-4", "4.3", "Jaeger"],
                "story_points": 3,
                "tasks": ["4.3.1", "4.3.2", "4.3.3"]
            },
            {
                "id": "4.4", "phase": "Phase-4",
                "title": "4.4 OpenTelemetry Integration",
                "description": "<p>Integrate OpenTelemetry in all services.</p>",
                "tags": ["Phase-4", "4.4", "OpenTelemetry"],
                "story_points": 5,
                "tasks": ["4.4.1", "4.4.2", "4.4.3", "4.4.4"]
            },
            {
                "id": "4.5", "phase": "Phase-4",
                "title": "4.5 EFK Stack",
                "description": "<p>Set up centralized logging with EFK stack.</p>",
                "tags": ["Phase-4", "4.5", "Logging"],
                "story_points": 5,
                "tasks": ["4.5.1", "4.5.2", "4.5.3", "4.5.4", "4.5.5"]
            },
            
            # Phase 5 Stories
            {
                "id": "5.1", "phase": "Phase-5",
                "title": "5.1 Kong Installation",
                "description": "<p>Install and configure Kong API Gateway.</p>",
                "tags": ["Phase-5", "5.1", "Kong"],
                "story_points": 3,
                "tasks": ["5.1.1", "5.1.2", "5.1.3"]
            },
            {
                "id": "5.2", "phase": "Phase-5",
                "title": "5.2 OAuth2 Plugin",
                "description": "<p>Configure OAuth2 authentication plugin.</p>",
                "tags": ["Phase-5", "5.2", "OAuth2"],
                "story_points": 3,
                "tasks": ["5.2.1", "5.2.2", "5.2.3"]
            },
            {
                "id": "5.3", "phase": "Phase-5",
                "title": "5.3 Rate Limiting",
                "description": "<p>Implement rate limiting policies.</p>",
                "tags": ["Phase-5", "5.3", "RateLimit"],
                "story_points": 3,
                "tasks": ["5.3.1", "5.3.2", "5.3.3"]
            },
            {
                "id": "5.4", "phase": "Phase-5",
                "title": "5.4 CORS Configuration",
                "description": "<p>Configure CORS for API access.</p>",
                "tags": ["Phase-5", "5.4", "CORS"],
                "story_points": 2,
                "tasks": ["5.4.1", "5.4.2", "5.4.3"]
            },
            {
                "id": "5.5", "phase": "Phase-5",
                "title": "5.5 API Documentation",
                "description": "<p>Set up API documentation portal.</p>",
                "tags": ["Phase-5", "5.5", "Documentation"],
                "story_points": 3,
                "tasks": ["5.5.1", "5.5.2", "5.5.3"]
            },
            {
                "id": "5.6", "phase": "Phase-5",
                "title": "5.6 Load Testing",
                "description": "<p>Perform load testing on API Gateway.</p>",
                "tags": ["Phase-5", "5.6", "Testing"],
                "story_points": 3,
                "tasks": ["5.6.1", "5.6.2", "5.6.3", "5.6.4"]
            },
            
            # Phase 6 Stories
            {
                "id": "6.1", "phase": "Phase-6",
                "title": "6.1 Harbor Installation",
                "description": "<p>Install Harbor container registry.</p>",
                "tags": ["Phase-6", "6.1", "Harbor"],
                "story_points": 3,
                "tasks": ["6.1.1", "6.1.2", "6.1.3"]
            },
            {
                "id": "6.2", "phase": "Phase-6",
                "title": "6.2 Vulnerability Scanning",
                "description": "<p>Enable security scanning for container images.</p>",
                "tags": ["Phase-6", "6.2", "Security"],
                "story_points": 3,
                "tasks": ["6.2.1", "6.2.2", "6.2.3"]
            },
            {
                "id": "6.3", "phase": "Phase-6",
                "title": "6.3 Image Replication",
                "description": "<p>Configure multi-region image replication.</p>",
                "tags": ["Phase-6", "6.3", "Replication"],
                "story_points": 3,
                "tasks": ["6.3.1", "6.3.2", "6.3.3"]
            },
            {
                "id": "6.4", "phase": "Phase-6",
                "title": "6.4 Push Service Images",
                "description": "<p>Push all service images to Harbor.</p>",
                "tags": ["Phase-6", "6.4", "Images"],
                "story_points": 5,
                "tasks": ["6.4.1", "6.4.2", "6.4.3", "6.4.4", "6.4.5"]
            },
            
            # Phase 7 Stories
            {
                "id": "7.1", "phase": "Phase-7",
                "title": "7.1 ArgoCD Installation",
                "description": "<p>Install ArgoCD for GitOps deployment.</p>",
                "tags": ["Phase-7", "7.1", "ArgoCD"],
                "story_points": 3,
                "tasks": ["7.1.1", "7.1.2", "7.1.3"]
            },
            {
                "id": "7.2", "phase": "Phase-7",
                "title": "7.2 Repository Structure",
                "description": "<p>Set up Git repository structure for manifests.</p>",
                "tags": ["Phase-7", "7.2", "Repository"],
                "story_points": 2,
                "tasks": ["7.2.1", "7.2.2", "7.2.3"]
            },
            {
                "id": "7.3", "phase": "Phase-7",
                "title": "7.3 Application Definitions",
                "description": "<p>Create ArgoCD applications for all services.</p>",
                "tags": ["Phase-7", "7.3", "Applications"],
                "story_points": 5,
                "tasks": ["7.3.1", "7.3.2", "7.3.3", "7.3.4"]
            },
            {
                "id": "7.4", "phase": "Phase-7",
                "title": "7.4 Sync Policies",
                "description": "<p>Configure auto-sync and self-heal policies.</p>",
                "tags": ["Phase-7", "7.4", "Policies"],
                "story_points": 2,
                "tasks": ["7.4.1", "7.4.2", "7.4.3"]
            },
            {
                "id": "7.5", "phase": "Phase-7",
                "title": "7.5 Multi-Environment",
                "description": "<p>Set up dev, staging, and prod environments.</p>",
                "tags": ["Phase-7", "7.5", "Environments"],
                "story_points": 3,
                "tasks": ["7.5.1", "7.5.2", "7.5.3"]
            },
            
            # Phase 8 Stories
            {
                "id": "8.1", "phase": "Phase-8",
                "title": "8.1 GitHub Actions - Build",
                "description": "<p>Set up build workflow in GitHub Actions.</p>",
                "tags": ["Phase-8", "8.1", "Build"],
                "story_points": 3,
                "tasks": ["8.1.1", "8.1.2", "8.1.3"]
            },
            {
                "id": "8.2", "phase": "Phase-8",
                "title": "8.2 GitHub Actions - Test",
                "description": "<p>Add testing stages to CI pipeline.</p>",
                "tags": ["Phase-8", "8.2", "Testing"],
                "story_points": 3,
                "tasks": ["8.2.1", "8.2.2", "8.2.3"]
            },
            {
                "id": "8.3", "phase": "Phase-8",
                "title": "8.3 Security Scanning",
                "description": "<p>Integrate security scanning tools.</p>",
                "tags": ["Phase-8", "8.3", "Security"],
                "story_points": 3,
                "tasks": ["8.3.1", "8.3.2", "8.3.3"]
            },
            {
                "id": "8.4", "phase": "Phase-8",
                "title": "8.4 Docker Build & Push",
                "description": "<p>Automate Docker image building and pushing.</p>",
                "tags": ["Phase-8", "8.4", "Docker"],
                "story_points": 3,
                "tasks": ["8.4.1", "8.4.2", "8.4.3"]
            },
            {
                "id": "8.5", "phase": "Phase-8",
                "title": "8.5 ArgoCD Sync",
                "description": "<p>Integrate ArgoCD sync in CD pipeline.</p>",
                "tags": ["Phase-8", "8.5", "Deployment"],
                "story_points": 3,
                "tasks": ["8.5.1", "8.5.2", "8.5.3"]
            },
            {
                "id": "8.6", "phase": "Phase-8",
                "title": "8.6 Rollback Strategy",
                "description": "<p>Implement automated rollback mechanism.</p>",
                "tags": ["Phase-8", "8.6", "Rollback"],
                "story_points": 2,
                "tasks": ["8.6.1", "8.6.2", "8.6.3"]
            },
            
            # Phase 9 Stories
            {
                "id": "9.1", "phase": "Phase-9",
                "title": "9.1 AWS Account Setup",
                "description": "<p>Set up AWS account and IAM roles.</p>",
                "tags": ["Phase-9", "9.1", "AWS"],
                "story_points": 2,
                "tasks": ["9.1.1", "9.1.2", "9.1.3"]
            },
            {
                "id": "9.2", "phase": "Phase-9",
                "title": "9.2 Terraform VPC",
                "description": "<p>Create VPC infrastructure with Terraform.</p>",
                "tags": ["Phase-9", "9.2", "VPC"],
                "story_points": 5,
                "tasks": ["9.2.1", "9.2.2", "9.2.3", "9.2.4"]
            },
            {
                "id": "9.3", "phase": "Phase-9",
                "title": "9.3 EKS Cluster",
                "description": "<p>Create EKS Kubernetes cluster.</p>",
                "tags": ["Phase-9", "9.3", "EKS"],
                "story_points": 5,
                "tasks": ["9.3.1", "9.3.2", "9.3.3", "9.3.4"]
            },
            {
                "id": "9.4", "phase": "Phase-9",
                "title": "9.4 RDS PostgreSQL",
                "description": "<p>Set up RDS PostgreSQL databases.</p>",
                "tags": ["Phase-9", "9.4", "RDS"],
                "story_points": 5,
                "tasks": ["9.4.1", "9.4.2", "9.4.3", "9.4.4"]
            },
            {
                "id": "9.5", "phase": "Phase-9",
                "title": "9.5 ElastiCache Redis",
                "description": "<p>Set up ElastiCache Redis cluster.</p>",
                "tags": ["Phase-9", "9.5", "Redis"],
                "story_points": 3,
                "tasks": ["9.5.1", "9.5.2", "9.5.3"]
            },
            {
                "id": "9.6", "phase": "Phase-9",
                "title": "9.6 S3 Buckets",
                "description": "<p>Create S3 buckets for file storage.</p>",
                "tags": ["Phase-9", "9.6", "S3"],
                "story_points": 2,
                "tasks": ["9.6.1", "9.6.2", "9.6.3"]
            },
            {
                "id": "9.7", "phase": "Phase-9",
                "title": "9.7 ALB Load Balancer",
                "description": "<p>Set up Application Load Balancer.</p>",
                "tags": ["Phase-9", "9.7", "ALB"],
                "story_points": 3,
                "tasks": ["9.7.1", "9.7.2", "9.7.3"]
            },
            {
                "id": "9.8", "phase": "Phase-9",
                "title": "9.8 Route53 DNS",
                "description": "<p>Configure DNS and SSL certificates.</p>",
                "tags": ["Phase-9", "9.8", "DNS"],
                "story_points": 2,
                "tasks": ["9.8.1", "9.8.2", "9.8.3"]
            },
            {
                "id": "9.9", "phase": "Phase-9",
                "title": "9.9 Deploy to EKS",
                "description": "<p>Deploy all services to production EKS.</p>",
                "tags": ["Phase-9", "9.9", "Deployment"],
                "story_points": 5,
                "tasks": ["9.9.1", "9.9.2", "9.9.3"]
            },
            {
                "id": "9.10", "phase": "Phase-9",
                "title": "9.10 Production Testing",
                "description": "<p>Perform production smoke and load tests.</p>",
                "tags": ["Phase-9", "9.10", "Testing"],
                "story_points": 3,
                "tasks": ["9.10.1", "9.10.2", "9.10.3"]
            },
            
            # Testing Phase Stories
            {
                "id": "T.1", "phase": "Phase-9",
                "title": "T.1 Unit Tests - All Services",
                "description": "<p>Comprehensive unit testing for all services.</p>",
                "tags": ["Testing", "T.1", "Unit"],
                "story_points": 8,
                "tasks": ["T.1"]
            },
            {
                "id": "T.2", "phase": "Phase-9",
                "title": "T.2 Integration Tests",
                "description": "<p>Integration testing between services.</p>",
                "tags": ["Testing", "T.2", "Integration"],
                "story_points": 5,
                "tasks": ["T.2"]
            },
            {
                "id": "T.3", "phase": "Phase-9",
                "title": "T.3 E2E Testing",
                "description": "<p>End-to-end workflow testing.</p>",
                "tags": ["Testing", "T.3", "E2E"],
                "story_points": 5,
                "tasks": ["T.3.1", "T.3.2", "T.3.3"]
            },
            {
                "id": "T.4", "phase": "Phase-9",
                "title": "T.4 Performance Testing",
                "description": "<p>Load and stress testing.</p>",
                "tags": ["Testing", "T.4", "Performance"],
                "story_points": 3,
                "tasks": ["T.4.1", "T.4.2", "T.4.3"]
            },
            {
                "id": "T.5", "phase": "Phase-9",
                "title": "T.5 Security Testing",
                "description": "<p>Security audits and penetration testing.</p>",
                "tags": ["Testing", "T.5", "Security"],
                "story_points": 3,
                "tasks": ["T.5.1", "T.5.2", "T.5.3"]
            },
            
            # Final Validation Stories
            {
                "id": "FV", "phase": "Phase-9",
                "title": "FV Final Validation",
                "description": "<p>Complete system validation and MVP criteria check.</p>",
                "tags": ["Validation", "FV", "MVP"],
                "story_points": 8,
                "tasks": [f"FV.{i}" for i in range(1, 20)]
            },
            
            # Additional Services Stories
            {
                "id": "A.1", "phase": "Phase-9",
                "title": "A.1 HR Service",
                "description": "<p>Develop HR management service.</p>",
                "tags": ["Additional", "A.1", "HR"],
                "story_points": 8,
                "tasks": ["A.1.1", "A.1.2", "A.1.3", "A.1.4", "A.1.5", "A.1.6"]
            },
            {
                "id": "A.2", "phase": "Phase-9",
                "title": "A.2 Sales Service",
                "description": "<p>Develop sales management service.</p>",
                "tags": ["Additional", "A.2", "Sales"],
                "story_points": 8,
                "tasks": ["A.2.1", "A.2.2", "A.2.3", "A.2.4", "A.2.5", "A.2.6"]
            },
            {
                "id": "A.3", "phase": "Phase-9",
                "title": "A.3 Reporting Service",
                "description": "<p>Develop reporting and analytics service.</p>",
                "tags": ["Additional", "A.3", "Reporting"],
                "story_points": 8,
                "tasks": ["A.3.1", "A.3.2", "A.3.3", "A.3.4", "A.3.5", "A.3.6"]
            },
            {
                "id": "A.4", "phase": "Phase-9",
                "title": "A.4 Notification Service",
                "description": "<p>Develop notification service.</p>",
                "tags": ["Additional", "A.4", "Notifications"],
                "story_points": 8,
                "tasks": ["A.4.1", "A.4.2", "A.4.3", "A.4.4", "A.4.5", "A.4.6"]
            },
            {
                "id": "A.5", "phase": "Phase-9",
                "title": "A.5 File Storage Service",
                "description": "<p>Develop file storage service.</p>",
                "tags": ["Additional", "A.5", "Storage"],
                "story_points": 8,
                "tasks": ["A.5.1", "A.5.2", "A.5.3", "A.5.4", "A.5.5", "A.5.6"]
            },
            {
                "id": "A.6", "phase": "Phase-9",
                "title": "A.6 Workflow Service",
                "description": "<p>Develop workflow automation service.</p>",
                "tags": ["Additional", "A.6", "Workflow"],
                "story_points": 8,
                "tasks": ["A.6.1", "A.6.2", "A.6.3", "A.6.4", "A.6.5", "A.6.6"]
            }
        ]


def main():
    """Main execution function."""
    print("=" * 70)
    print("Azure DevOps - Epics and User Stories Creator")
    print("Odoo Microservices Project")
    print("=" * 70)
    
    # Get credentials from environment or prompt
    organization = os.getenv('AZURE_DEVOPS_ORG')
    project = os.getenv('AZURE_DEVOPS_PROJECT')
    pat = os.getenv('AZURE_DEVOPS_PAT')
    
    if not all([organization, project, pat]):
        print("\n⚠️  Environment variables not found. Please provide credentials:")
        organization = organization or input("Enter Azure DevOps Organization: ")
        project = project or input("Enter Project Name: ")
        pat = pat or input("Enter Personal Access Token: ")
    
    # Create instance
    creator = AzureDevOpsStructureCreator(organization, project, pat)
    
    # Test connection
    print("\n🔌 Testing connection...")
    if not creator.test_connection():
        print("\n❌ Connection test failed. Please check your credentials.")
        sys.exit(1)
    
    # Fetch existing tasks
    tasks_map = creator.get_existing_tasks()
    if not tasks_map:
        print("\n⚠️  Warning: No tasks found. Make sure you've imported tasks first.")
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            sys.exit(0)
    
    # Confirm before proceeding
    print("\n" + "=" * 70)
    print(f"⚠️  This will create:")
    print(f"   • 10 Epics (Phases 0-9)")
    print(f"   • ~60 User Stories (feature groups)")
    print(f"   • Link {len(tasks_map)} existing tasks to stories")
    print("=" * 70)
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        sys.exit(0)
    
    # Create Epics
    epics = creator.create_all_epics()
    
    # Create User Stories and link tasks
    stories = creator.create_all_user_stories(epics, tasks_map)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Epics created:        {len(epics)}")
    print(f"User Stories created: {len(stories)}")
    print(f"Tasks linked:         {len(tasks_map)}")
    print("=" * 70)
    
    print(f"\n✅ Setup complete! View at:")
    print(f"   https://dev.azure.com/{organization}/{project}/_boards/board")
    print("\nNext steps:")
    print("   1. Review Epics in Boards → Backlogs")
    print("   2. Follow AZURE_BOARDS_CONFIGURATION_GUIDE.md for queries and dashboards")
    print("   3. Start working on Phase 0 tasks!")


if __name__ == "__main__":
    main()
