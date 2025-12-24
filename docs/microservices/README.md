# Odoo Microservices Architecture

This directory contains the complete microservices setup for Odoo 19.0 with Kubernetes, CI/CD, and cloud infrastructure.

## 📁 Directory Structure

```
├── k8s/                      # Kubernetes manifests
│   ├── base/                 # Base configurations
│   └── overlays/             # Environment-specific overlays
│       ├── dev/
│       ├── staging/
│       └── production/
├── ci-cd/                    # CI/CD pipelines
│   ├── github-actions/       # GitHub Actions workflows
│   ├── azure-pipelines/      # Azure DevOps pipelines
│   └── aws-codepipeline/     # AWS CodePipeline configs
├── helm/                     # Helm charts
│   └── odoo/                 # Odoo Helm chart
├── terraform/                # Infrastructure as Code
│   ├── aws-eks/              # AWS EKS cluster
│   └── azure-aks/            # Azure AKS cluster
├── monitoring/               # Observability stack
└── docs/                     # Documentation
```

## 🚀 Quick Start

### Prerequisites

- kubectl (v1.28+)
- helm (v3.12+)
- terraform (v1.5+)
- Docker (v24+)
- Access to Kubernetes cluster
- Harbor registry credentials

### 1. Deploy to Kubernetes (Kustomize)

```bash
# Development
kubectl apply -k k8s/overlays/dev

# Production
kubectl apply -k k8s/overlays/production
```

### 2. Deploy with Helm

```bash
# Add Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install Odoo
helm install odoo ./helm/odoo \
  --namespace odoo \
  --create-namespace \
  --values helm/odoo/values.yaml

# Upgrade
helm upgrade odoo ./helm/odoo \
  --namespace odoo \
  --values helm/odoo/values.yaml
```

### 3. Provision Infrastructure

#### AWS EKS

```bash
cd terraform/aws-eks

# Initialize
terraform init

# Plan
terraform plan -var="environment=production" \
  -var="cluster_name=odoo-prod" \
  -out=tfplan

# Apply
terraform apply tfplan

# Get kubeconfig
aws eks update-kubeconfig \
  --region us-east-1 \
  --name odoo-prod
```

#### Azure AKS

```bash
cd terraform/azure-aks

# Initialize
terraform init

# Plan
terraform plan -var="environment=production" \
  -var="cluster_name=odoo-prod" \
  -out=tfplan

# Apply
terraform apply tfplan

# Get kubeconfig
az aks get-credentials \
  --resource-group odoo-prod-rg \
  --name odoo-prod
```

## 🔐 Security Configuration

### 1. Create Kubernetes Secrets

```bash
# PostgreSQL credentials
kubectl create secret generic odoo-secrets \
  --from-literal=POSTGRES_PASSWORD='your-password' \
  --from-literal=DB_PASSWORD='your-password' \
  --from-literal=ODOO_ADMIN_PASSWORD='admin-password' \
  --namespace=odoo

# Harbor registry credentials
kubectl create secret docker-registry harbor-registry \
  --docker-server=harbor.example.com \
  --docker-username=robot\$odoo \
  --docker-password='your-token' \
  --namespace=odoo
```

### 2. Update ConfigMaps

```bash
kubectl edit configmap odoo-config -n odoo
```

## 🐳 Harbor Registry Setup

### Push Images to Harbor

```bash
# Login
docker login harbor.example.com

# Build and tag
docker build -t harbor.example.com/odoo/odoo:19.0 .

# Push
docker push harbor.example.com/odoo/odoo:19.0
```

### Configure Robot Account

1. Go to Harbor UI
2. Create robot account: `robot$odoo`
3. Grant push/pull permissions to `odoo` project
4. Use token in Kubernetes secret

## 📊 Monitoring

### Install Prometheus Stack

```bash
helm repo add prometheus-community \
  https://prometheus-community.github.io/helm-charts

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### Access Dashboards

```bash
# Port forward Grafana
kubectl port-forward -n monitoring \
  svc/prometheus-grafana 3000:80

# Access: http://localhost:3000
# Default credentials: admin/prom-operator
```

## 🔄 CI/CD Setup

### GitHub Actions

1. Add secrets to GitHub repository:
   - `HARBOR_USERNAME`
   - `HARBOR_PASSWORD`
   - `KUBE_CONFIG_DEV`
   - `KUBE_CONFIG_PROD`

2. Push to trigger workflow:
```bash
git push origin develop  # Deploys to dev
git push origin main     # Deploys to production
```

### Azure DevOps

1. Create service connections:
   - Harbor registry
   - Kubernetes clusters
   - Azure subscription

2. Import pipeline:
   - Use `ci-cd/azure-pipelines/azure-pipelines.yml`

## 📈 Scaling

### Manual Scaling

```bash
# Scale Odoo deployment
kubectl scale deployment odoo \
  --replicas=5 \
  --namespace=odoo
```

### Auto-scaling

HPA (Horizontal Pod Autoscaler) is configured in `k8s/base/hpa.yaml`:
- Min replicas: 2
- Max replicas: 10
- Target CPU: 70%
- Target Memory: 80%

## 🔍 Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n odoo
kubectl describe pod <pod-name> -n odoo
kubectl logs <pod-name> -n odoo --tail=100
```

### Check Services

```bash
kubectl get svc -n odoo
kubectl get ingress -n odoo
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
kubectl exec -it deployment/postgres -n odoo -- \
  psql -U odoo -d postgres
```

## 📚 Additional Documentation

- [Kubernetes Deployment Guide](./microservices/kubernetes-guide.md)
- [Helm Chart Documentation](./microservices/helm-guide.md)
- [CI/CD Pipeline Setup](./microservices/cicd-guide.md)
- [Harbor Integration](./microservices/harbor-guide.md)
- [Monitoring Setup](./microservices/monitoring-guide.md)

## 🤝 Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## 📝 License

See LICENSE file for details.
