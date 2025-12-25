#!/usr/bin/env python3
"""
Link existing tasks to their parent User Stories in Azure DevOps.
This script assumes Epics and User Stories have already been created.
"""

import os
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List


class TaskLinker:
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.auth = HTTPBasicAuth('', pat)
        self.api_version = "7.0"
    
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
                return False
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def get_existing_tasks(self) -> Dict[str, int]:
        """Fetch all existing tasks and map task title to work_item_id."""
        print("\n📥 Fetching existing tasks...")
        
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
                        tasks_map[title] = work_item_id
                    
                    time.sleep(0.1)
                
                print(f"✓ Mapped {len(tasks_map)} tasks by title")
            
            return tasks_map
            
        except Exception as e:
            print(f"✗ Error fetching tasks: {e}")
            return {}
    
    def get_existing_user_stories(self) -> Dict[str, int]:
        """Fetch all existing user stories and map by title."""
        print("\n📥 Fetching existing user stories...")
        
        url = f"{self.base_url}/wit/wiql?api-version={self.api_version}"
        query = {
            "query": """
                SELECT [System.Id], [System.Title]
                FROM WorkItems
                WHERE [System.WorkItemType] = 'User Story'
                AND [System.TeamProject] = @project
                ORDER BY [System.Id]
            """
        }
        
        try:
            response = requests.post(url, json=query, auth=self.auth)
            response.raise_for_status()
            
            work_items = response.json().get('workItems', [])
            print(f"✓ Found {len(work_items)} user stories")
            
            stories_map = {}
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
                        # Extract story ID from title (e.g., "0.1 Domain-Driven Design" -> "0.1")
                        story_id = title.split()[0]
                        stories_map[story_id] = work_item_id
                    
                    time.sleep(0.1)
                
                print(f"✓ Mapped {len(stories_map)} user stories by ID")
            
            return stories_map
            
        except Exception as e:
            print(f"✗ Error fetching user stories: {e}")
            return {}
    
    def link_work_item(self, source_id: int, target_id: int) -> bool:
        """Link a task to its parent user story."""
        url = f"{self.base_url}/wit/workitems/{source_id}?api-version={self.api_version}"
        
        operations = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/workItems/{target_id}",
                    "attributes": {
                        "comment": "Linked by automation script"
                    }
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
            # Phase 0
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
            
            # Phase 1
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
            
            # Phase 2
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
            
            # Phase 3
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
            
            # Phase 4
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
            
            # Phase 5
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
            
            # Phase 6
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
            
            # Phase 7
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
            
            # Phase 8
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
            
            # Phase 9
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
            
            # Testing
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
    
    def get_story_to_tasks_mapping(self) -> Dict[str, List[str]]:
        """Return mapping of story IDs to their task IDs."""
        return {
            "0.1": ["0.1.1", "0.1.2", "0.1.3"],
            "0.2": ["0.2.1", "0.2.2", "0.2.3", "0.2.4", "0.2.5"],
            "0.3": ["0.3.1", "0.3.2", "0.3.3"],
            "0.4": ["0.4.1", "0.4.2", "0.4.3"],
            "0.5": ["0.5.1", "0.5.2", "0.5.3", "0.5.4", "0.5.5"],
            "0.6": ["0.6.1", "0.6.2", "0.6.3", "0.6.4", "0.6.5"],
            
            "1.1": ["1.1.1", "1.1.2", "1.1.3", "1.1.4"],
            "1.2": ["1.2.1", "1.2.2", "1.2.3", "1.2.4", "1.2.5"],
            "1.3": ["1.3.1", "1.3.2", "1.3.3", "1.3.4"],
            "1.4": ["1.4.1", "1.4.2", "1.4.3"],
            "1.5": ["1.5.1", "1.5.2", "1.5.3"],
            "1.6": ["1.6.1", "1.6.2", "1.6.3"],
            
            "2.1": ["2.1.1", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7", "2.1.8", "2.1.9"],
            "2.2": ["2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6", "2.2.7", "2.2.8", "2.2.9"],
            "2.3": ["2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.3.8", "2.3.9"],
            "2.4": ["2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.4.5", "2.4.6", "2.4.7", "2.4.8", "2.4.9"],
            "2.5": ["2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.5", "2.5.6", "2.5.7", "2.5.8"],
            
            "3.1": ["3.1.1", "3.1.2", "3.1.3", "3.1.4"],
            "3.2": ["3.2.1", "3.2.2", "3.2.3", "3.2.4", "3.2.5"],
            "3.3": ["3.3.1", "3.3.2", "3.3.3", "3.3.4"],
            "3.4": ["3.4.1", "3.4.2", "3.4.3", "3.4.4"],
            "3.5": ["3.5.1", "3.5.2", "3.5.3"],
            
            "4.1": ["4.1.1", "4.1.2", "4.1.3", "4.1.4"],
            "4.2": ["4.2.1", "4.2.2", "4.2.3", "4.2.4", "4.2.5", "4.2.6"],
            "4.3": ["4.3.1", "4.3.2", "4.3.3"],
            "4.4": ["4.4.1", "4.4.2", "4.4.3", "4.4.4"],
            "4.5": ["4.5.1", "4.5.2", "4.5.3", "4.5.4", "4.5.5"],
            
            "5.1": ["5.1.1", "5.1.2", "5.1.3"],
            "5.2": ["5.2.1", "5.2.2", "5.2.3"],
            "5.3": ["5.3.1", "5.3.2", "5.3.3"],
            "5.4": ["5.4.1", "5.4.2", "5.4.3"],
            "5.5": ["5.5.1", "5.5.2", "5.5.3"],
            "5.6": ["5.6.1", "5.6.2", "5.6.3", "5.6.4"],
            
            "6.1": ["6.1.1", "6.1.2", "6.1.3"],
            "6.2": ["6.2.1", "6.2.2", "6.2.3"],
            "6.3": ["6.3.1", "6.3.2", "6.3.3"],
            "6.4": ["6.4.1", "6.4.2", "6.4.3", "6.4.4", "6.4.5"],
            
            "7.1": ["7.1.1", "7.1.2", "7.1.3"],
            "7.2": ["7.2.1", "7.2.2", "7.2.3"],
            "7.3": ["7.3.1", "7.3.2", "7.3.3", "7.3.4"],
            "7.4": ["7.4.1", "7.4.2", "7.4.3"],
            "7.5": ["7.5.1", "7.5.2", "7.5.3"],
            
            "8.1": ["8.1.1", "8.1.2", "8.1.3"],
            "8.2": ["8.2.1", "8.2.2", "8.2.3"],
            "8.3": ["8.3.1", "8.3.2", "8.3.3"],
            "8.4": ["8.4.1", "8.4.2", "8.4.3"],
            "8.5": ["8.5.1", "8.5.2", "8.5.3"],
            "8.6": ["8.6.1", "8.6.2", "8.6.3"],
            
            "9.1": ["9.1.1", "9.1.2", "9.1.3"],
            "9.2": ["9.2.1", "9.2.2", "9.2.3", "9.2.4"],
            "9.3": ["9.3.1", "9.3.2", "9.3.3", "9.3.4"],
            "9.4": ["9.4.1", "9.4.2", "9.4.3", "9.4.4"],
            "9.5": ["9.5.1", "9.5.2", "9.5.3"],
            "9.6": ["9.6.1", "9.6.2", "9.6.3"],
            "9.7": ["9.7.1", "9.7.2", "9.7.3"],
            "9.8": ["9.8.1", "9.8.2", "9.8.3"],
            "9.9": ["9.9.1", "9.9.2", "9.9.3"],
            "9.10": ["9.10.1", "9.10.2", "9.10.3"],
            
            "T.1": ["T.1"],
            "T.2": ["T.2"],
            "T.3": ["T.3.1", "T.3.2", "T.3.3"],
            "T.4": ["T.4.1", "T.4.2", "T.4.3"],
            "T.5": ["T.5.1", "T.5.2", "T.5.3"],
            
            "FV": ["FV.1", "FV.2", "FV.3", "FV.4", "FV.5", "FV.6", "FV.7", "FV.8", "FV.9", 
                   "FV.10", "FV.11", "FV.12", "FV.13", "FV.14", "FV.15", "FV.16", "FV.17", "FV.18", "FV.19"],
            
            "A.1": ["A.1.1", "A.1.2", "A.1.3", "A.1.4", "A.1.5", "A.1.6"],
            "A.2": ["A.2.1", "A.2.2", "A.2.3", "A.2.4", "A.2.5", "A.2.6"],
            "A.3": ["A.3.1", "A.3.2", "A.3.3", "A.3.4", "A.3.5", "A.3.6"],
            "A.4": ["A.4.1", "A.4.2", "A.4.3", "A.4.4", "A.4.5", "A.4.6"],
            "A.5": ["A.5.1", "A.5.2", "A.5.3", "A.5.4", "A.5.5", "A.5.6"],
            "A.6": ["A.6.1", "A.6.2", "A.6.3", "A.6.4", "A.6.5", "A.6.6"],
        }
    
    def link_tasks(self):
        """Main method to link tasks to user stories."""
        print("\n🔗 Starting task linking process...")
        
        # Get existing tasks and user stories
        tasks_map = self.get_existing_tasks()
        stories_map = self.get_existing_user_stories()
        
        # Get mappings
        task_id_to_title = self.get_task_id_to_title_mapping()
        story_to_tasks = self.get_story_to_tasks_mapping()
        
        total_linked = 0
        total_failed = 0
        total_not_found = 0
        
        # Link tasks to stories
        for story_id, task_ids in story_to_tasks.items():
            if story_id not in stories_map:
                print(f"⚠️  Story '{story_id}' not found in Azure DevOps")
                continue
            
            story_work_item_id = stories_map[story_id]
            print(f"\n📝 Linking tasks to story: {story_id} (ID: {story_work_item_id})")
            
            for task_id in task_ids:
                # Convert task ID to task title
                task_title = task_id_to_title.get(task_id)
                if not task_title:
                    print(f"  ⚠️  No title found for task ID: {task_id}")
                    total_not_found += 1
                    continue
                
                # Get task work item ID
                if task_title not in tasks_map:
                    print(f"  ⚠️  Task not found in Azure DevOps: {task_title}")
                    total_not_found += 1
                    continue
                
                task_work_item_id = tasks_map[task_title]
                
                # Link the task to the story
                success = self.link_work_item(task_work_item_id, story_work_item_id)
                if success:
                    print(f"  ✓ Linked: {task_id} - {task_title}")
                    total_linked += 1
                else:
                    total_failed += 1
                
                time.sleep(0.1)  # Rate limiting
        
        print(f"\n{'='*60}")
        print(f"✅ Task linking complete!")
        print(f"{'='*60}")
        print(f"✓ Successfully linked: {total_linked} tasks")
        print(f"⚠️  Failed to link: {total_failed} tasks")
        print(f"⚠️  Tasks not found: {total_not_found}")
        print(f"{'='*60}\n")


def main():
    # Load environment variables
    org = os.getenv('AZURE_DEVOPS_ORG')
    project = os.getenv('AZURE_DEVOPS_PROJECT')
    pat = os.getenv('AZURE_DEVOPS_PAT')
    
    if not all([org, project, pat]):
        print("❌ Missing required environment variables:")
        print("  - AZURE_DEVOPS_ORG")
        print("  - AZURE_DEVOPS_PROJECT")
        print("  - AZURE_DEVOPS_PAT")
        print("\nMake sure .azure_devops.env is properly configured.")
        sys.exit(1)
    
    linker = TaskLinker(org, project, pat)
    
    if not linker.test_connection():
        print("❌ Failed to connect to Azure DevOps")
        sys.exit(1)
    
    # Link tasks
    linker.link_tasks()


if __name__ == "__main__":
    main()
