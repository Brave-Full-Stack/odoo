# Odoo Microservices Architecture

[![Build Status](https://github.com/bravejongen/odoo/actions/workflows/microservices-ci-cd.yml/badge.svg)](https://github.com/bravejongen/odoo/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/bravejongen/odoo-auth-service)](https://hub.docker.com/u/bravejongen)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

> **Branch**: `Odoo-19.0-microservices`  
> **Architecture**: Cloud-Native Event-Driven Microservices  
> **Deployment**: Kubernetes + Istio Service Mesh + AWS EKS

Production-ready Odoo ERP system decomposed into independently deployable microservices with full observability, security, and scalability.

---

## 📊 Project Management & Tracking

This project uses **Azure DevOps Boards** for comprehensive sprint planning and task tracking. All Azure DevOps automation scripts, documentation, and dashboards are organized in the [`azure-devops-setup/`](./azure-devops-setup/) folder.

### Quick Links
- 📋 **[Azure DevOps Boards](https://dev.azure.com/Aries-Test/Odoo-Microservices)** - 378 Work Items (10 Epics, 70 User Stories, 298 Tasks)
- 📊 **[Sprint Dashboard](./azure-devops-setup/sprint-dashboard.html)** - Interactive HTML dashboard with metrics and charts
- 📖 **[Setup Documentation](./azure-devops-setup/README.md)** - Complete Azure DevOps setup guide
- 🚀 **[View Sprints Guide](./azure-devops-setup/docs/VIEW_SPRINTS_GUIDE.md)** - How to navigate sprints in Azure DevOps

### Project Stats
- ✅ **10 Epics** organized by project phases (0-9)
- ✅ **70 User Stories** distributed across 6 sprints
- ✅ **298 Tasks** linked to parent stories (90% success rate)
- ✅ **6 Sprints** with dates from Dec 25, 2025 to Feb 8, 2026
- ✅ **Automated scripts** for task management and dashboard generation

### Sprint Organization
| Sprint | Duration | Phases | Work Items | Dates |
|--------|----------|--------|------------|-------|
| Sprint 1 | 10 days | Phase 0-1 | 2 Epics, 12 Stories | Dec 25 - Jan 4 |
| Sprint 2 | 10 days | Phase 2-3 | 2 Epics, 10 Stories | Jan 4 - Jan 14 |
| Sprint 3 | 10 days | Phase 4-5 | 2 Epics, 11 Stories | Jan 14 - Jan 24 |
| Sprint 4 | 5 days | Phase 6-7 | 2 Epics, 9 Stories | Jan 24 - Jan 29 |
| Sprint 5 | 5 days | Phase 8 | 1 Epic, 6 Stories | Jan 29 - Feb 3 |
| Sprint 6 | 5 days | Phase 9 + Testing | 1 Epic, 22 Stories | Feb 3 - Feb 8 |

---

## 🏗️ Architecture Overview

### Microservices Components

```
┌─────────────────────────────────────────────────────────────┐
│            Kong API Gateway + OAuth2/JWT                     │
└────────────────┬────────────────────────────────────────────┘
                 │
    ┌────────────┼──────────┬───────────┬──────────────┐
    │            │          │           │              │
┌───▼───┐  ┌────▼────┐ ┌──▼──────┐ ┌──▼─────┐  ┌────▼─────┐
│ Auth  │  │  Core   │ │Accounting│ │Inventory│  │   CRM    │
│Service│  │   ERP   │ │ Service  │ │ Service │  │ Service  │
└───┬───┘  └────┬────┘ └──┬───────┘ └──┬──────┘  └────┬─────┘
    │           │          │            │              │
    └───────────┴──────────┴────────────┴──────────────┘
                           │
              ┌────────────┴────────────┐
              │    RabbitMQ Event Bus   │
              └─────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐     ┌───▼────┐
    │Auth DB  │      │Account DB │     │Inv DB  │
    │Postgres │      │ Postgres  │     │Postgres│
    └─────────┘      └───────────┘     └────────┘
```

### Core Services

| Service | Purpose | Technology Stack | Port |
|---------|---------|-----------------|------|
| **auth-service** | Authentication & Authorization | FastAPI + PostgreSQL + JWT | 8080 |
| **core-erp-service** | Core business logic & partners | FastAPI + PostgreSQL | 8080 |
| **accounting-service** | Invoices, payments, reports | FastAPI + PostgreSQL + Events | 8080 |
| **inventory-service** | Stock, warehouses, products | FastAPI + PostgreSQL + Events | 8080 |
| **crm-service** | Leads, opportunities, pipeline | FastAPI + PostgreSQL | 8080 |
| **hr-service** | Employees, payroll, attendance | FastAPI + PostgreSQL | 8080 |
| **sales-service** | Orders, quotations, customers | FastAPI + PostgreSQL + Events | 8080 |
| **reporting-service** | Analytics, dashboards, exports | FastAPI + Pandas + Redis | 8080 |
| **notification-service** | Email, SMS, push notifications | FastAPI + Celery + Redis | 8080 |
| **file-storage-service** | Attachments, documents, S3 | FastAPI + MinIO/S3 | 8080 |

---

## 🚀 Technology Stack

### Infrastructure
- **Container Orchestration**: Kubernetes (Kind/Minikube → AWS EKS)
- **Service Mesh**: Istio 1.20+ (mTLS, traffic management, observability)
- **API Gateway**: Kong 3.4+ (OAuth2, JWT, rate limiting, CORS)
- **Container Registry**: Harbor 2.9+ (vulnerability scanning, replication)
- **GitOps**: ArgoCD 2.9+ (automated deployments, sync policies)

### Backend Services
- **Framework**: FastAPI 0.104+ (async Python)
- **Databases**: PostgreSQL 15+ (one per service)
- **Connection Pooling**: PgBouncer
- **Message Queue**: RabbitMQ 3.12+ (event-driven architecture)
- **Cache**: Redis 7.0+ / AWS ElastiCache
- **Search**: Elasticsearch 8.x
- **Task Queue**: Celery 5.3+

### Observability
- **Metrics**: Prometheus + Grafana (service dashboards)
- **Tracing**: Jaeger + OpenTelemetry (distributed tracing)
- **Logging**: Fluentd + Elasticsearch + Kibana (EFK stack)
- **Service Mesh Dashboard**: Kiali

### CI/CD & IaC
- **CI/CD**: GitHub Actions (multi-service pipelines)
- **IaC**: Terraform 1.6+ (AWS EKS, VPC, RDS, ElastiCache)
- **Package Manager**: Helm 3.13+
- **Security Scanning**: Trivy, SonarQube
- **Load Testing**: Locust

### Security
- **mTLS**: Istio PeerAuthentication (strict mode)
- **Secrets Management**: Kubernetes Secrets + AWS Secrets Manager
- **Network Policies**: Kubernetes NetworkPolicy
- **Policy Enforcement**: OPA Gatekeeper
- **Pod Security**: Pod Security Standards (restricted)

---

## 📋 Deployment Phases

### Phase 0: Microservices Design (Days 1-10)
**Tools**: Domain-Driven Design, Event Storming, OpenAPI
- Define service boundaries using DDD
- Design event schemas (Pydantic models)
- Create OpenAPI specs for each service
- Database-per-service pattern
- API versioning strategy (/api/v1/)

### Phase 1: Service Mesh Setup (Days 11-18)
**Tools**: Istio, Kiali, Prometheus, Grafana, Jaeger
```bash
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```
- Install Istio service mesh
- Configure mTLS (strict mode)
- Set up VirtualServices & DestinationRules
- Deploy Kiali for visualization
- Circuit breakers & retry policies

### Phase 2: Core Services Development (Days 11-18)
**Tools**: FastAPI, SQLAlchemy, Alembic, pytest, Docker
```bash
# Build and test services
cd microservices/auth-service
pytest tests/ -v --cov=.
docker build -t bravejongen/odoo-auth:latest .
```
- Develop FastAPI microservices
- Implement JWT authentication
- Create database models & migrations
- Unit & integration tests (>80% coverage)
- Containerize all services

### Phase 3: Event Bus & Messaging (Days 19-22)
**Tools**: RabbitMQ, aio-pika, Pydantic
```bash
# Install RabbitMQ with Helm
helm install rabbitmq bitnami/rabbitmq \
  --set auth.username=odoo \
  --set persistence.enabled=true
```
- Deploy RabbitMQ cluster
- Define event schemas (InvoiceCreated, PaymentReceived, etc.)
- Implement publisher/consumer patterns
- Event replay & dead-letter queues
- Event versioning strategy

### Phase 4: Observability Stack (Days 23-26)
**Tools**: Prometheus, Grafana, Jaeger, EFK Stack
```bash
# Access dashboards
istioctl dashboard prometheus
istioctl dashboard grafana
istioctl dashboard jaeger
kubectl port-forward -n logging svc/kibana-kibana 5601:5601
```
- Prometheus metrics collection
- Grafana dashboards (service performance, infrastructure)
- Jaeger distributed tracing
- EFK centralized logging
- Custom application metrics

### Phase 5: API Gateway & Security (Days 27-30)
**Tools**: Kong, OAuth2, JWT, cert-manager
```bash
# Install Kong
helm install kong kong/kong \
  --namespace kong --create-namespace \
  --set ingressController.installCRDs=false
```
- Kong API Gateway deployment
- OAuth2 & JWT plugins
- Rate limiting (per-consumer, per-endpoint)
- CORS & security headers
- Request validation (OpenAPI)

### Phase 6: Container Registry (Days 31-32)
**Tools**: Harbor, Trivy
```bash
# Install Harbor
helm install harbor harbor/harbor \
  --set persistence.enabled=true \
  --set trivy.enabled=true
```
- Harbor registry deployment
- Vulnerability scanning (Trivy)
- Robot accounts for CI/CD
- Image replication policies
- Retention policies

### Phase 7: GitOps with ArgoCD (Days 33-35)
**Tools**: ArgoCD, Kustomize
```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
- ArgoCD installation & configuration
- Connect Git repository
- App-of-Apps pattern
- Automated sync policies
- Multi-environment management (dev, staging, prod)

### Phase 8: CI/CD Pipeline (Days 36-38)
**Tools**: GitHub Actions, Docker, ArgoCD CLI
```yaml
# .github/workflows/microservices-ci-cd.yml
- Build & test each service
- Security scanning (Trivy, Snyk)
- Push to Harbor
- Update K8s manifests
- Trigger ArgoCD sync
```
- Multi-service pipeline (path-based triggers)
- Automated testing (unit, integration, E2E)
- Code quality (Black, Flake8, mypy)
- Image scanning & signing
- Blue-green deployments

### Phase 9: AWS EKS Production (Days 39-45)
**Tools**: Terraform, AWS EKS, RDS, ElastiCache, AWS Load Balancer Controller
```bash
# Deploy with Terraform
cd terraform/aws-eks
terraform init
terraform apply
aws eks update-kubeconfig --region eu-west-1 --name odoo-eks
```
- EKS cluster (3 node groups: system, apps, data)
- RDS PostgreSQL (Multi-AZ)
- ElastiCache Redis (cluster mode)
- VPC & networking (3 AZs)
- AWS Load Balancer Controller
- External DNS (Route53)
- Cert-manager (ACM integration)

### Phase 10: Production Optimization (Days 46-50)
**Tools**: HPA, Cluster Autoscaler, Velero, Kubecost, Locust
```bash
# Load testing
locust -f tests/performance/locustfile.py \
  --headless -u 1000 -r 100 --run-time 30m
```
- Horizontal Pod Autoscaler (HPA)
- Cluster Autoscaler
- PgBouncer connection pooling
- Redis caching layer
- Network Policies
- Backup & DR (Velero)
- Cost optimization (Kubecost)
- Load testing (1000+ concurrent users)

---

## � System Requirements

### Resource Analysis (Your VM)
```
✅ CPU: 8 cores (Excellent - enough for full stack)
⚠️  RAM: 8.5 GB total, 3.2 GB available
   - Currently using: 5.4 GB (Odoo local-dev + PostgreSQL running)
   - Minimum needed: 6 GB for microservices (tight)
   - Recommended: 12-16 GB for comfortable development
⚠️  Disk: 207 GB available (Good, but monitor Docker images)
✅ Swap: 2 GB (Helps, but not ideal for production workloads)
```

### Resource Requirements per Phase

| Phase | Min RAM | Recommended RAM | CPU Cores | Disk Space | Can Run Alongside Local Dev? |
|-------|---------|----------------|-----------|------------|------------------------------|
| **Phase 0** (Design) | 0 GB | 0 GB | N/A | 1 GB | ✅ Yes (no services running) |
| **Phase 1** (Istio) | 2 GB | 4 GB | 2 | 5 GB | ⚠️  Tight (stop local dev) |
| **Phase 2** (3 services) | 3 GB | 6 GB | 4 | 10 GB | ⚠️  Tight (stop local dev) |
| **Phase 3** (RabbitMQ) | +1 GB | +1.5 GB | 4 | +2 GB | ❌ Stop local dev |
| **Phase 4** (Observability) | +2 GB | +3 GB | 4 | +5 GB | ❌ Stop local dev |
| **Phase 5** (Kong) | +512 MB | +1 GB | 4 | +2 GB | ❌ Stop local dev |
| **Full Stack** | 8 GB | 12-16 GB | 4-8 | 30 GB | ❌ Stop local dev |

### ⚠️ Resource Recommendation

**Your VM (8.5 GB RAM) can run:**
- ✅ **Option 1**: Local dev branch (current setup) - 4-5 GB RAM
- ✅ **Option 2**: Microservices (minimal - 3 services) - 6-7 GB RAM
- ❌ **Both simultaneously**: Not recommended (9-11 GB needed)

**Recommended Approach:**
1. **Keep local dev for daily work** (Odoo-19.0-local-dev branch)
2. **Use microservices for learning/testing** (stop local dev first)
3. **For production microservices**: Deploy to AWS EKS (Phase 9)

---

## 🚀 Getting Started - Step by Step

### Decision Tree: Choose Your Path

```
START HERE
    │
    ├─➤ Want to learn microservices architecture?
    │   └─➤ Follow "Path A: Learning Track" (Phases 0-2)
    │       ├─ Run Phase 0 (Design) - no resources needed
    │       ├─ Run Phase 1 (Istio) - stop local dev
    │       └─ Run Phase 2 (Build 1-2 services) - test concepts
    │
    ├─➤ Want production-ready deployment?
    │   └─➤ Follow "Path B: Production Track" (All Phases)
    │       ├─ Skip local K8s (resource intensive)
    │       └─ Go directly to Phase 9 (AWS EKS)
    │
    └─➤ Want to keep current local dev?
        └─➤ Follow "Path C: Hybrid Approach"
            ├─ Keep Odoo-19.0-local-dev for development
            ├─ Use Docker Compose for testing microservices
            └─ Deploy to AWS when ready
```

---

## 📚 PATH A: Learning Track (Recommended for Your VM)

**Goal**: Understand microservices concepts without overwhelming resources  
**Duration**: 2-3 weeks  
**Resource Impact**: Moderate (stop local dev during testing)

### Step 1: Preparation (No services running)

**1.1 Install Required Tools**
```bash
# Navigate to your odoo directory
cd /home/brave/Desktop/FullStack/odoo

# Check current branch
git branch
# You should be on: Odoo-19.0-microservices

# If not, switch:
git checkout Odoo-19.0-microservices

# Install Kind (lightweight Kubernetes)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify installation
kind version

# Install kubectl (if not already installed)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify
helm version
```

**1.2 Create Workspace Structure**
```bash
# Create microservices directories
mkdir -p microservices/{auth-service,core-erp-service,accounting-service}
mkdir -p microservices/auth-service/{tests,models,api}
mkdir -p shared/{events,messaging,models}

# Create Istio configuration directory
mkdir -p istio/

# Create testing directory
mkdir -p tests/{integration,performance}
```

### Step 2: Phase 0 - Design Services (Days 1-2)

**No running services needed - just design work**

**2.1 Create Auth Service Structure**
```bash
cd microservices/auth-service

# Create main application file
cat > main.py << 'EOF'
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

app = FastAPI(title="Odoo Auth Service", version="1.0.0")

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

# Fake database (replace with real DB in production)
fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@odoo.local",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8080

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
EOF

# Create basic tests
mkdir -p tests
cat > tests/test_auth.py << 'EOF'
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401
EOF

# Add pytest to requirements
echo "pytest==7.4.3" >> requirements.txt
echo "httpx==0.25.2" >> requirements.txt

cd ../..
```

**2.2 Test Auth Service Locally (without K8s)**
```bash
cd microservices/auth-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start service locally (in background)
python main.py &
AUTH_PID=$!

# Wait for service to start
sleep 3

# Test the service
curl http://localhost:8080/health

# Test login
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Stop the service
kill $AUTH_PID

deactivate
cd ../..
```

**✅ Checkpoint**: You should see:
- Health check returns `{"status": "healthy"}`
- Login returns an `access_token`
- Tests pass with `pytest`

### Step 3: Test with Docker Compose (Low Resource)

**Instead of full Kubernetes**, let's test with Docker Compose first:

**3.1 Create Docker Compose for Testing**
```bash
cat > docker-compose.microservices.yml << 'EOF'
version: '3.8'

services:
  auth-service:
    build:
      context: ./microservices/auth-service
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - JWT_SECRET_KEY=dev-secret-key
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - odoo-network

  postgres-auth:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: auth_db
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - auth-db-data:/var/lib/postgresql/data
    networks:
      - odoo-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  auth-db-data:

networks:
  odoo-network:
    driver: bridge
EOF
```

**3.2 Test with Docker Compose**
```bash
# STOP your local dev Odoo first to free resources
# Find Odoo process
ps aux | grep odoo-bin | grep -v grep

# If running, you can stop it (or leave it if you have enough RAM)

# Build and start auth service
docker-compose -f docker-compose.microservices.yml up -d auth-service postgres-auth

# Check logs
docker-compose -f docker-compose.microservices.yml logs -f auth-service

# Test the service
curl http://localhost:8080/health

# Test login
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"

# Check resource usage
docker stats --no-stream

# Stop when done
docker-compose -f docker-compose.microservices.yml down
```

**✅ Expected Result**: Auth service running, using ~200-300 MB RAM

### Step 4: Add One More Service (Accounting)

**4.1 Create Accounting Service**
```bash
cd microservices
mkdir -p accounting-service/tests

cat > accounting-service/main.py << 'EOF'
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import httpx

app = FastAPI(title="Odoo Accounting Service", version="1.0.0")

AUTH_SERVICE_URL = "http://auth-service:8080"

class Invoice(BaseModel):
    id: Optional[int] = None
    partner_name: str
    amount: float
    date: date
    state: str = "draft"

# In-memory database (replace with real DB)
invoices_db = []
invoice_counter = 1

async def verify_token(authorization: str):
    """Verify JWT token with auth service"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.split(" ")[1]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")
            return response.json()
    except httpx.RequestError:
        # For local testing without auth service
        return {"username": "test"}

@app.get("/api/v1/accounting/invoices", response_model=List[Invoice])
async def get_invoices():
    """Get all invoices"""
    return invoices_db

@app.post("/api/v1/accounting/invoices", response_model=Invoice)
async def create_invoice(invoice: Invoice):
    """Create new invoice"""
    global invoice_counter
    invoice.id = invoice_counter
    invoice_counter += 1
    invoices_db.append(invoice)
    return invoice

@app.get("/api/v1/accounting/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int):
    """Get invoice by ID"""
    for invoice in invoices_db:
        if invoice.id == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "accounting-service",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

# Create requirements
cat > accounting-service/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
httpx==0.25.2
pytest==7.4.3
EOF

# Create Dockerfile
cat > accounting-service/Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
EOF

cd ..
```

**4.2 Update Docker Compose**
```bash
cat >> docker-compose.microservices.yml << 'EOF'

  accounting-service:
    build:
      context: ./microservices/accounting-service
      dockerfile: Dockerfile
    ports:
      - "8081:8080"
    environment:
      - AUTH_SERVICE_URL=http://auth-service:8080
    depends_on:
      - auth-service
      - postgres-accounting
    networks:
      - odoo-network

  postgres-accounting:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: accounting_db
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - accounting-db-data:/var/lib/postgresql/data
    networks:
      - odoo-network
EOF

# Add volume
sed -i '/^volumes:/a\  accounting-db-data:' docker-compose.microservices.yml
```

**4.3 Test Both Services**
```bash
# Start all services
docker-compose -f docker-compose.microservices.yml up -d

# Wait for services to be ready
sleep 10

# Test auth service
curl http://localhost:8080/health

# Get token
TOKEN=$(curl -s -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Token: $TOKEN"

# Test accounting service
curl http://localhost:8081/health

# Create invoice
curl -X POST "http://localhost:8081/api/v1/accounting/invoices" \
  -H "Content-Type: application/json" \
  -d '{"partner_name": "Customer A", "amount": 1000.50, "date": "2025-01-15"}'

# Get invoices
curl http://localhost:8081/api/v1/accounting/invoices

# Check resource usage
docker stats --no-stream

# View logs
docker-compose -f docker-compose.microservices.yml logs

# Stop when done
docker-compose -f docker-compose.microservices.yml down
```

**✅ Expected Resource Usage**:
- Auth service: ~200 MB RAM
- Accounting service: ~200 MB RAM
- 2x PostgreSQL: ~100 MB RAM each
- **Total**: ~600 MB RAM (Very manageable!)

---

## 📚 PATH B: Production Track (For AWS Deployment)

**Goal**: Deploy production-ready microservices to AWS EKS  
**Prerequisites**: AWS account, credit card, ~$100-200/month budget  
**Resource Impact**: None on your VM (everything runs in AWS)

### Quick Start for AWS Deployment

**1. Skip Local Kubernetes** (too resource-intensive for your VM)

**2. Go Directly to Phase 9** (AWS EKS)

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter your AWS Access Key, Secret Key, Region (eu-west-1)

# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Deploy EKS cluster (see DEPLOYMENT_PLAN.md Phase 9)
cd terraform/aws-eks
terraform init
terraform plan
terraform apply  # Takes 15-20 minutes

# Configure kubectl for EKS
aws eks update-kubeconfig --region eu-west-1 --name odoo-microservices-eks

# Deploy services
kubectl apply -k k8s/overlays/production/
```

---

## 📚 PATH C: Hybrid Approach (Recommended)

**Goal**: Keep local dev running + learn microservices concepts  
**Best for**: Your current VM resources

### Strategy

1. **Keep Odoo-19.0-local-dev** for daily development work
2. **Use Docker Compose** for microservices testing (low resource)
3. **Deploy to AWS EKS** when ready for production

### Daily Workflow

```bash
# Morning: Start local dev
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-local-dev
./odoo-bin -c odoo.conf  # Your current setup

# Afternoon: Test microservices (stop local dev first)
# Stop Odoo local dev
pkill -f odoo-bin

# Start microservices
git checkout Odoo-19.0-microservices
docker-compose -f docker-compose.microservices.yml up -d

# Test and learn
curl http://localhost:8080/health
curl http://localhost:8081/health

# Evening: Back to local dev
docker-compose -f docker-compose.microservices.yml down
git checkout Odoo-19.0-local-dev
./odoo-bin -c odoo.conf
```

---

## 🎯 Recommended Next Steps for YOU

Based on your VM resources (8.5 GB RAM, 8 CPU cores):

### Week 1: Learn Microservices Concepts
```bash
# Day 1-2: Create auth service (Done above in Step 2)
# Day 3-4: Create accounting service (Done above in Step 4)
# Day 5: Test with Docker Compose
docker-compose -f docker-compose.microservices.yml up -d
```

### Week 2: Add More Services
```bash
# Create inventory-service following same pattern
# Create crm-service
# Test inter-service communication
```

### Week 3: Deploy to AWS (Optional)
```bash
# Only if you want production deployment
# Follow Phase 9 in DEPLOYMENT_PLAN.md
# Cost: ~$150-200/month for EKS cluster
```

---

## ⚡ Quick Commands Reference

### Resource Management
```bash
# Check current resource usage
free -h
docker stats --no-stream

# Stop local dev to free resources
pkill -f odoo-bin
sudo systemctl stop postgresql  # If you want to free more

# Start local dev again
sudo systemctl start postgresql
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-local-dev
./odoo-bin -c odoo.conf
```

### Microservices Testing
```bash
# Start microservices (Docker Compose)
docker-compose -f docker-compose.microservices.yml up -d

# View logs
docker-compose -f docker-compose.microservices.yml logs -f

# Stop microservices
docker-compose -f docker-compose.microservices.yml down

# Clean up (free disk space)
docker system prune -a --volumes
```

### Git Branch Management
```bash
# Switch to microservices branch
git checkout Odoo-19.0-microservices

# Switch back to local dev
git checkout Odoo-19.0-local-dev

# View all branches
git branch -a
```

---

## 📁 Repository Structure

```
odoo/
├── microservices/              # Service implementations
│   ├── auth-service/           # JWT authentication
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── tests/
│   ├── core-erp-service/       # Core business logic
│   ├── accounting-service/     # Accounting & invoicing
│   ├── inventory-service/      # Inventory management
│   └── crm-service/            # Customer relationship
├── shared/                     # Shared libraries
│   ├── events/                 # Event schemas
│   ├── messaging/              # RabbitMQ publisher/consumer
│   └── models/                 # Common data models
├── k8s/                        # Kubernetes manifests
│   ├── base/                   # Base configurations
│   ├── overlays/               # Environment overlays
│   │   ├── dev/
│   │   ├── staging/
│   │   └── production/
│   └── services/               # Per-service K8s configs
├── istio/                      # Istio configurations
│   ├── virtual-services.yaml
│   ├── destination-rules.yaml
│   └── gateway.yaml
├── helm/                       # Helm charts
│   └── odoo/
│       ├── Chart.yaml
│       └── values.yaml
├── terraform/                  # Infrastructure as Code
│   └── aws-eks/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── ci-cd/                      # CI/CD configurations
│   ├── github-actions/
│   └── azure-pipelines/
├── argocd/                     # ArgoCD applications
│   ├── apps/
│   └── root-app.yaml
├── tests/                      # Test suites
│   ├── integration/
│   ├── performance/
│   └── e2e/
├── DEPLOYMENT_PLAN.md          # Detailed deployment guide
├── docker-compose.yml          # Local development
└── README.md                   # This file
```

---

## 🔐 Security

### Authentication & Authorization
- **OAuth2/JWT**: Kong OAuth2 plugin + JWT validation
- **mTLS**: Service-to-service encryption (Istio)
- **RBAC**: Kubernetes RBAC + custom service policies
- **Secrets**: Kubernetes Secrets + AWS Secrets Manager

### Network Security
- **Network Policies**: Deny-all by default, explicit allow rules
- **TLS**: cert-manager + Let's Encrypt/ACM
- **DDoS Protection**: AWS Shield + WAF
- **Rate Limiting**: Kong per-consumer & per-endpoint limits

### Security Scanning
```bash
# Container vulnerability scanning (Harbor + Trivy)
trivy image bravejongen/odoo-auth:latest

# Code scanning (SonarQube)
sonar-scanner -Dsonar.projectKey=odoo-microservices
```

---

## 📊 Monitoring & Observability

### Access Dashboards

**Kiali (Service Mesh)**
```bash
istioctl dashboard kiali
# http://localhost:20001
```

**Grafana (Metrics)**
```bash
istioctl dashboard grafana
# http://localhost:3000
```

**Jaeger (Tracing)**
```bash
istioctl dashboard jaeger
# http://localhost:16686
```

**Kibana (Logs)**
```bash
kubectl port-forward -n logging svc/kibana-kibana 5601:5601
# http://localhost:5601
```

**Prometheus (Metrics)**
```bash
istioctl dashboard prometheus
# http://localhost:9090
```

### Key Metrics to Monitor
- Request rate (requests/sec per service)
- Response time (p50, p90, p99)
- Error rate (% of failed requests)
- CPU & Memory usage
- Database connection pool stats
- Message queue depth
- Cache hit/miss ratio

---

## 🧪 Testing

### Unit Tests
```bash
cd microservices/auth-service
pytest tests/ -v --cov=. --cov-report=html
# Target: >80% coverage
```

### Integration Tests
```bash
pytest tests/integration/ -v --base-url=http://localhost:8080
```

### Load Testing
```bash
# Locust load testing (1000 concurrent users)
locust -f tests/performance/locustfile.py \
  --headless -u 1000 -r 100 --run-time 30m \
  --host https://odoo.yourdomain.com
```

### End-to-End Tests
```bash
# Playwright E2E tests
npm install --save-dev @playwright/test
npx playwright test
```

---

## 🚢 Deployment

### Development (Local Cluster)
```bash
kubectl apply -k k8s/overlays/dev/
kubectl port-forward svc/auth-service 8080:8080
```

### Staging (AWS EKS)
```bash
argocd app sync odoo-services-staging
argocd app wait odoo-services-staging --health
```

### Production (AWS EKS)
```bash
# Automated via GitHub Actions on merge to main
# Manual sync if needed
argocd app sync odoo-services-prod
argocd app wait odoo-services-prod --health --timeout 600
```

---

## 📖 Documentation

- **[⚡ Getting Started Guide](GETTING_STARTED.md)**: Quick 30-minute start guide
- **[📊 Resource Planning](RESOURCE_PLANNING.md)**: VM resource analysis and recommendations  
- **[🚀 Deployment Plan](DEPLOYMENT_PLAN.md)**: Complete 10-phase deployment guide (50 days)
- **[API Documentation](https://odoo.yourdomain.com/api/docs)**: OpenAPI/Swagger docs (after deployment)
- **[Architecture Decisions](docs/ADR/)**: ADR records
- **[Runbooks](docs/runbooks/)**: Operational procedures
- **[Contributing](CONTRIBUTING.md)**: Contribution guidelines

### 🎯 Start Here

**New to microservices?** → Read [GETTING_STARTED.md](GETTING_STARTED.md)  
**Want to check resources?** → Read [RESOURCE_PLANNING.md](RESOURCE_PLANNING.md)  
**Ready to deploy?** → Follow [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow
- Write tests first (TDD)
- Ensure >80% code coverage
- Run linters (Black, Flake8, mypy)
- Update documentation
- Pass CI/CD pipeline

---

## 📝 License

This project is licensed under the LGPL v3 License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Troubleshooting

### Common Issues

**Service not reachable?**
```bash
# Check pod status
kubectl get pods -n odoo-services

# Check Istio sidecar
kubectl get pods -n odoo-services -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# View logs
kubectl logs -f <pod-name> -n odoo-services -c auth-service
kubectl logs -f <pod-name> -n odoo-services -c istio-proxy
```

**Database connection issues?**
```bash
# Test connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgresql.odoo-services.svc.cluster.local -U odoo -d auth_db

# Check PgBouncer
kubectl exec -it pgbouncer-xxx -n odoo-services -- \
  psql -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"
```

**ArgoCD sync failing?**
```bash
# View sync errors
argocd app get auth-service
argocd app logs auth-service

# Force refresh
argocd app sync auth-service --force
```

---

## 📞 Contact

- **Project Lead**: [@bravejongen](https://github.com/bravejongen)
- **Issues**: [GitHub Issues](https://github.com/bravejongen/odoo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bravejongen/odoo/discussions)

---

**Last Updated**: December 2025  
**Version**: 2.0.0 (Microservices Architecture)  
**Branch**: Odoo-19.0-microservices
