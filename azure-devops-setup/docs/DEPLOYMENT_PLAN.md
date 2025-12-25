# Odoo Microservices Deployment Plan
**Production-Ready Kubernetes Microservices Architecture**

> **Branch**: `Odoo-19.0-microservices`  
> **Architecture**: Event-Driven Microservices with Service Mesh  
> **Goal**: Deploy distributed Odoo system → Harbor → ArgoCD → AWS EKS  
> **Timeline**: 4-5 weeks (phased microservices approach)

---

## 🏗️ Microservices Architecture Overview

### Core Services Decomposition

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway (Kong/NGINX)                  │
│                     + Authentication (OAuth2/JWT)                │
└────────────────┬────────────────────────────────────────────────┘
                 │
    ┌────────────┼────────────┬─────────────┬──────────────┐
    │            │            │             │              │
┌───▼───┐  ┌────▼────┐  ┌───▼────┐  ┌────▼─────┐  ┌────▼─────┐
│ Auth  │  │  Core   │  │ Addon  │  │ Workflow │  │  Report  │
│Service│  │   ERP   │  │Service │  │  Engine  │  │ Service  │
└───┬───┘  └────┬────┘  └───┬────┘  └────┬─────┘  └────┬─────┘
    │           │            │             │              │
    └───────────┴────────────┴─────────────┴──────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
          ┌─────▼─────┐           ┌──────▼──────┐
          │ Message   │           │   Service   │
          │   Queue   │           │    Mesh     │
          │ (RabbitMQ)│           │   (Istio)   │
          └─────┬─────┘           └──────┬──────┘
                │                         │
    ┌───────────┴───────────┬─────────────┴──────┐
    │                       │                    │
┌───▼────┐          ┌──────▼──────┐      ┌─────▼─────┐
│User DB │          │Product DB   │      │ Order DB  │
│(Postgres)         │(Postgres)   │      │(Postgres) │
└────────┘          └─────────────┘      └───────────┘
```

### Microservices Components

1. **API Gateway Service** (Kong/Ambassador)
   - Routing, rate limiting, authentication
   - Service discovery integration
   
2. **Authentication Service**
   - User authentication (OAuth2, SAML, LDAP)
   - JWT token management
   - Session handling

3. **Core ERP Service**
   - Base Odoo functionality
   - Core business logic
   - Main database operations

4. **Module Services** (Separate per major module)
   - Accounting Service
   - Inventory Service
   - CRM Service
   - HR Service
   - Sales Service

5. **Workflow Engine Service**
   - Business process automation
   - Scheduled jobs (cron)
   - Event processing

6. **Reporting Service**
   - Report generation (PDF, Excel)
   - Analytics and BI
   - Data aggregation

7. **Notification Service**
   - Email notifications
   - Push notifications
   - SMS integration

8. **File Storage Service**
   - Attachments and documents
   - S3/MinIO integration

9. **Search Service** (Elasticsearch)
   - Full-text search
   - Product search
   - Document indexing

10. **Cache Service** (Redis)
    - Session storage
    - Query caching
    - Distributed locks

---

## 📋 Table of Contents

1. [Phase 0: Microservices Design (Days 1-5)](#phase-0-microservices-design)
2. [Phase 1: Service Mesh Setup (Days 6-10)](#phase-1-service-mesh-setup)
3. [Phase 2: Core Services Development (Days 11-18)](#phase-2-core-services-development)
4. [Phase 3: Event Bus & Messaging (Days 19-22)](#phase-3-event-bus--messaging)
5. [Phase 4: Observability Stack (Days 23-26)](#phase-4-observability-stack)
6. [Phase 5: API Gateway & Security (Days 27-30)](#phase-5-api-gateway--security)
7. [Phase 6: Container Registry (Days 31-32)](#phase-6-container-registry)
8. [Phase 7: GitOps with ArgoCD (Days 33-35)](#phase-7-gitops-with-argocd)
9. [Phase 8: CI/CD Pipeline (Days 36-38)](#phase-8-cicd-pipeline)
10. [Phase 9: Cloud Infrastructure (Days 39-45)](#phase-9-cloud-infrastructure)
11. [Testing & Validation](#testing--validation)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## Phase 0: Microservices Design (Days 1-5)

### Objective
Design and architect Odoo as distributed microservices

### 0.1 Domain-Driven Design

Create service boundaries based on Odoo modules:

```
microservices/
├── auth-service/          # Authentication & Authorization
├── core-erp-service/      # Base Odoo core
├── accounting-service/    # Accounting module
├── inventory-service/     # Stock & Warehouse
├── crm-service/          # Customer Relationship
├── hr-service/           # Human Resources
├── sales-service/        # Sales & Orders
├── reporting-service/    # Reports & Analytics
├── workflow-service/     # Cron & Automation
├── notification-service/ # Email, SMS, Push
├── file-service/         # File storage
└── api-gateway/          # Kong/NGINX config
```

### 0.2 Database Per Service Pattern

Each service has its own database:

```yaml
# Database architecture
auth-db:         # Users, sessions, tokens
  type: PostgreSQL
  size: 50GB

core-erp-db:     # Core models, res_partner, res_company
  type: PostgreSQL
  size: 100GB

accounting-db:   # Invoices, payments, journals
  type: PostgreSQL
  size: 200GB

inventory-db:    # Products, stock, warehouses
  type: PostgreSQL
  size: 150GB

crm-db:          # Leads, opportunities, activities
  type: PostgreSQL
  size: 80GB

analytics-db:    # Aggregated data for reports
  type: TimescaleDB
  size: 300GB
```

### 0.3 Inter-Service Communication

```yaml
# Communication patterns
Synchronous:
  - REST APIs (service-to-service)
  - gRPC (high-performance calls)
  
Asynchronous:
  - RabbitMQ (event bus)
  - Kafka (event streaming)
  
Event Types:
  - UserCreated
  - OrderPlaced
  - InvoiceGenerated
  - InventoryUpdated
  - PaymentReceived
```

### 0.4 Create Service Structure

```bash
# Create microservices directories
mkdir -p microservices/{auth,core-erp,accounting,inventory,crm,hr,sales,reporting,workflow,notification,file-storage,api-gateway}

# Create shared libraries
mkdir -p shared/
cd shared/
mkdir -p {models,utils,config,middleware,events}

# Create each service structure
for service in auth core-erp accounting inventory crm hr sales reporting workflow notification file-storage; do
  cd ../microservices/$service/
  mkdir -p {controllers,models,services,repositories,events,config,tests}
  touch Dockerfile requirements.txt README.md
done
```

### 0.5 Define Service APIs

Create OpenAPI specs for each service:

```yaml
# microservices/auth/openapi.yaml
openapi: 3.0.0
info:
  title: Auth Service API
  version: 1.0.0
paths:
  /api/v1/auth/login:
    post:
      summary: User login
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                username: string
                password: string
      responses:
        200:
          description: JWT token
          content:
            application/json:
              schema:
                type: object
                properties:
                  token: string
                  refresh_token: string
                  expires_in: integer
  
  /api/v1/auth/validate:
    get:
      summary: Validate JWT token
      security:
        - BearerAuth: []
      responses:
        200:
          description: Token valid
```

### 0.6 Service Dependencies Matrix

```yaml
# service-dependencies.yaml
auth-service:
  depends_on: []
  database: auth-db
  cache: redis
  
core-erp-service:
  depends_on:
    - auth-service
  database: core-erp-db
  cache: redis
  
accounting-service:
  depends_on:
    - auth-service
    - core-erp-service
  database: accounting-db
  message_queue: rabbitmq
  
inventory-service:
  depends_on:
    - auth-service
    - core-erp-service
  database: inventory-db
  message_queue: rabbitmq
  search: elasticsearch
```

---

## Phase 1: Service Mesh Setup (Days 6-10)

---

### Objective
Install and configure Istio service mesh for microservices communication

### 1.1 Install Istio

```bash
# Install Istio CLI
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.20.0
export PATH=$PWD/bin:$PATH

# Install Istio on cluster (use Kind for this phase)
istioctl install --set profile=demo -y

# Enable automatic sidecar injection
kubectl label namespace default istio-injection=enabled
kubectl create namespace odoo-services
kubectl label namespace odoo-services istio-injection=enabled

# Verify installation
kubectl get pods -n istio-system
istioctl verify-install
```

### 1.2 Install Kiali (Service Mesh Dashboard)

```bash
# Install observability add-ons
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml

# Access Kiali dashboard
istioctl dashboard kiali
# Opens: http://localhost:20001
```

### 1.3 Configure Traffic Management

Create `istio/virtual-services.yaml`:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: odoo-services
  namespace: odoo-services
spec:
  hosts:
  - "*"
  gateways:
  - odoo-gateway
  http:
  - match:
    - uri:
        prefix: /api/v1/auth
    route:
    - destination:
        host: auth-service
        port:
          number: 8080
  - match:
    - uri:
        prefix: /api/v1/accounting
    route:
    - destination:
        host: accounting-service
        port:
          number: 8080
  - match:
    - uri:
        prefix: /api/v1/inventory
    route:
    - destination:
        host: inventory-service
        port:
          number: 8080
  - match:
    - uri:
        prefix: /api/v1/crm
    route:
    - destination:
        host: crm-service
        port:
          number: 8080
---
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: odoo-gateway
  namespace: odoo-services
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: odoo-tls-cert
    hosts:
    - "odoo.yourdomain.com"
```

### 1.4 Configure Resilience Patterns

Create `istio/destination-rules.yaml`:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: auth-service
  namespace: odoo-services
spec:
  host: auth-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    loadBalancer:
      simple: LEAST_REQUEST
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: accounting-service
  namespace: odoo-services
spec:
  host: accounting-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 200
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 200
    loadBalancer:
      consistentHash:
        httpHeaderName: "x-user-id"  # Session affinity
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 20s
      baseEjectionTime: 60s
```

### 1.5 mTLS Configuration

```bash
# Enable strict mTLS for all services
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: odoo-services
spec:
  mtls:
    mode: STRICT
EOF

# Verify mTLS is enabled
istioctl x describe pod <pod-name> -n odoo-services
```

### 1.6 Service Mesh Testing

```bash
# Deploy test services
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: auth-service
  namespace: odoo-services
  labels:
    app: auth-service
spec:
  ports:
  - port: 8080
    name: http
  selector:
    app: auth-service
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: odoo-services
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
      version: v1
  template:
    metadata:
      labels:
        app: auth-service
        version: v1
    spec:
      containers:
      - name: auth-service
        image: bravejongen/odoo-auth:latest
        ports:
        - containerPort: 8080
EOF

# Test service mesh
kubectl exec -it <test-pod> -n odoo-services -- curl http://auth-service:8080/health

# View in Kiali
istioctl dashboard kiali
```

---

## Phase 2: Core Services Development (Days 11-18)

### Objective
Develop and containerize core microservices

### 2.1 Authentication Service

Create `microservices/auth-service/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

app = FastAPI(title="Auth Service")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class User(BaseModel):
    username: str
    email: str
    full_name: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validate credentials (connect to auth-db)
    # For demo, accept any user
    access_token = create_access_token(data={"sub": form_data.username})
    refresh_token = create_access_token(data={"sub": form_data.username, "type": "refresh"})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }

@app.get("/api/v1/auth/validate")
async def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "valid": True}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}
```

Create `microservices/auth-service/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

Create `microservices/auth-service/requirements.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
psycopg2-binary==2.9.9
pydantic==2.5.0
```

### 2.2 Core ERP Service

Create `microservices/core-erp-service/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

app = FastAPI(title="Core ERP Service")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8080")

class Partner(BaseModel):
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

async def verify_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_SERVICE_URL}/api/v1/auth/validate",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return response.json()

@app.get("/api/v1/partners", response_model=List[Partner])
async def get_partners(token: str = Depends(verify_token)):
    # Query database
    return [
        Partner(id=1, name="Partner 1", email="partner1@example.com"),
        Partner(id=2, name="Partner 2", email="partner2@example.com")
    ]

@app.post("/api/v1/partners", response_model=Partner)
async def create_partner(partner: Partner, token: str = Depends(verify_token)):
    # Insert into database
    partner.id = 1  # Simulated ID
    return partner

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "core-erp-service"}
```

### 2.3 Accounting Service

Create `microservices/accounting-service/main.py`:

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import asyncio
import aio_pika

app = FastAPI(title="Accounting Service")

class Invoice(BaseModel):
    id: Optional[int] = None
    partner_id: int
    date: date
    amount: float
    state: str = "draft"

# RabbitMQ connection
async def publish_event(event_type: str, data: dict):
    connection = await aio_pika.connect_robust("amqp://rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(data).encode()),
            routing_key=f"odoo.{event_type}"
        )

@app.post("/api/v1/invoices", response_model=Invoice)
async def create_invoice(invoice: Invoice):
    # Save to database
    invoice.id = 1
    
    # Publish event
    await publish_event("invoice.created", {
        "invoice_id": invoice.id,
        "partner_id": invoice.partner_id,
        "amount": invoice.amount
    })
    
    return invoice

@app.get("/api/v1/invoices", response_model=List[Invoice])
async def get_invoices():
    return [
        Invoice(id=1, partner_id=1, date=date.today(), amount=1000.0, state="draft")
    ]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "accounting-service"}
```

### 2.4 Build All Services

```bash
# Build each service
for service in auth-service core-erp-service accounting-service; do
  cd microservices/$service/
  docker build -t bravejongen/odoo-$service:latest .
  cd ../..
done

# Test locally
docker run -p 8081:8080 bravejongen/odoo-auth-service:latest
curl http://localhost:8081/health
```

---

## Phase 3: Event Bus & Messaging (Days 19-22)

### Objective
Set up event-driven architecture with RabbitMQ/Kafka

### 3.1 Install RabbitMQ

```bash
# Add RabbitMQ Helm repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Install RabbitMQ
helm install rabbitmq bitnami/rabbitmq \
  --namespace odoo-services \
  --set auth.username=odoo \
  --set auth.password=odoo123 \
  --set persistence.enabled=true \
  --set persistence.size=20Gi \
  --set metrics.enabled=true

# Get RabbitMQ password
kubectl get secret --namespace odoo-services rabbitmq -o jsonpath="{.data.rabbitmq-password}" | base64 -d

# Port forward to management UI
kubectl port-forward --namespace odoo-services svc/rabbitmq 15672:15672
# Access: http://localhost:15672 (user: odoo, pass: odoo123)
```

### 3.2 Define Event Schemas

Create `shared/events/schemas.py`:

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BaseEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    service: str

class InvoiceCreated(BaseEvent):
    invoice_id: int
    partner_id: int
    amount: float
    currency: str = "USD"

class PaymentReceived(BaseEvent):
    payment_id: int
    invoice_id: int
    amount: float
    payment_method: str

class InventoryUpdated(BaseEvent):
    product_id: int
    location_id: int
    quantity_change: float
    new_quantity: float

class OrderPlaced(BaseEvent):
    order_id: int
    customer_id: int
    total_amount: float
    items: list
```

### 3.3 Event Publisher (Shared Library)

Create `shared/messaging/publisher.py`:

```python
import aio_pika
import json
from typing import Any

class EventPublisher:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
    
    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        
        # Declare exchange
        self.exchange = await self.channel.declare_exchange(
            "odoo_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
    
    async def publish(self, routing_key: str, message: Any):
        if not self.channel:
            await self.connect()
        
        await self.exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                content_type="application/json"
            ),
            routing_key=routing_key
        )
    
    async def close(self):
        if self.connection:
            await self.connection.close()
```

### 3.4 Event Consumer (Shared Library)

Create `shared/messaging/consumer.py`:

```python
import aio_pika
import json
from typing import Callable
import asyncio

class EventConsumer:
    def __init__(self, rabbitmq_url: str, queue_name: str):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.handlers = {}
    
    def register_handler(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler
    
    async def start(self):
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        channel = await connection.channel()
        
        # Declare queue
        queue = await channel.declare_queue(self.queue_name, durable=True)
        
        # Bind to exchange
        exchange = await channel.declare_exchange(
            "odoo_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        await queue.bind(exchange, routing_key="odoo.#")
        
        # Start consuming
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    event_type = body.get("event_type")
                    
                    if event_type in self.handlers:
                        await self.handlers[event_type](body)
```

### 3.5 Update Services with Events

Update `microservices/inventory-service/main.py`:

```python
from fastapi import FastAPI
from shared.messaging.consumer import EventConsumer
from shared.messaging.publisher import EventPublisher
import asyncio

app = FastAPI(title="Inventory Service")

publisher = EventPublisher("amqp://odoo:odoo123@rabbitmq:5672/")
consumer = EventConsumer("amqp://odoo:odoo123@rabbitmq:5672/", "inventory_queue")

async def handle_order_placed(event: dict):
    # Update inventory when order is placed
    print(f"Reducing inventory for order {event['order_id']}")
    # Update database
    # Publish inventory updated event
    await publisher.publish("odoo.inventory.updated", {
        "event_type": "inventory.updated",
        "product_id": event["product_id"],
        "quantity_change": -event["quantity"]
    })

@app.on_event("startup")
async def startup():
    await publisher.connect()
    consumer.register_handler("order.placed", handle_order_placed)
    asyncio.create_task(consumer.start())

@app.on_event("shutdown")
async def shutdown():
    await publisher.close()
```

---

## Phase 4: Observability Stack (Days 23-26)

### 1.1 Choose Local Kubernetes Platform

#### Option A: Kind (Recommended for CI/CD testing)
```bash
# Install Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster with ingress support
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: odoo-dev
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

#### Option B: Minikube (Easier for beginners)
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --cpus=4 --memory=8192 --driver=docker
minikube addons enable ingress
minikube addons enable metrics-server
```

### 1.2 Install Required Tools

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/

# Install kubectx and kubens (optional but useful)
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens

# Verify installations
kubectl version --client
helm version
kustomize version
```

### 1.3 Build and Load Odoo Image

```bash
# Build Odoo image
docker build -t odoo:19.0-local -f Dockerfile .

# Load image to Kind
kind load docker-image odoo:19.0-local --name odoo-dev

# OR for Minikube
minikube image load odoo:19.0-local
```

### 1.4 Create Namespace and Secrets

```bash
# Create odoo namespace
kubectl create namespace odoo-dev

# Create secrets
kubectl create secret generic odoo-secrets -n odoo-dev \
  --from-literal=postgresql-password=odoo123 \
  --from-literal=odoo-admin-password=admin123

# Create pgadmin secret
kubectl create secret generic pgadmin-secret -n odoo-dev \
  --from-literal=pgadmin-password=admin123 \
  --from-literal=pgadmin-email=admin@odoo.local
```

### 1.5 Deploy with Kustomize (Development)

```bash
# Apply dev overlay
kubectl apply -k k8s/overlays/dev/

# Check deployment status
kubectl get all -n odoo-dev
kubectl get pvc -n odoo-dev
kubectl get ingress -n odoo-dev

# Watch pods until running
kubectl get pods -n odoo-dev -w
```

### 1.6 Access the Application

```bash
# For Kind - Port forward
kubectl port-forward -n odoo-dev svc/odoo 8069:8069

# For Minikube - Get URL
minikube service odoo -n odoo-dev --url

# Access pgAdmin
kubectl port-forward -n odoo-dev svc/pgadmin 5050:80

# Check logs
kubectl logs -n odoo-dev -l app=odoo --tail=100 -f
```

### 1.7 Testing Checklist

- [ ] All pods are running
- [ ] PVCs are bound
- [ ] Can access Odoo at http://localhost:8069
- [ ] Can login to backend
- [ ] Database is accessible via pgAdmin
- [ ] Data persists after pod restart

---

## Phase 6: Container Registry - Harbor (Days 31-32)

### Objective
Set up Harbor registry and push microservice images

### 6.1 Deploy Harbor on Kubernetes

```bash
# Add Harbor Helm repo
helm repo add harbor https://helm.goharbor.io
helm repo update

# Create harbor namespace
kubectl create namespace harbor

# Install Harbor
helm install harbor harbor/harbor \
  --namespace harbor \
  --set expose.type=nodePort \
  --set expose.tls.enabled=false \
  --set persistence.enabled=true \
  --set persistence.persistentVolumeClaim.registry.size=50Gi \
  --set persistence.persistentVolumeClaim.database.size=10Gi \
  --set harborAdminPassword=Harbor12345 \
  --set trivy.enabled=true  # Enable vulnerability scanning

# Get Harbor URL
kubectl port-forward -n harbor svc/harbor 8080:80
# Access: http://localhost:8080 (admin/Harbor12345)
```

### 6.2 Configure Docker for Harbor

```bash
# Add insecure registry (for local development)
sudo tee -a /etc/docker/daemon.json <<EOF
{
  "insecure-registries": ["harbor.local:8080", "localhost:8080"]
}
EOF

sudo systemctl restart docker

# Login to Harbor
docker login localhost:8080
# Username: admin
# Password: Harbor12345
```

### 6.3 Create Harbor Projects

```bash
# Via Harbor UI or API
curl -X POST "http://localhost:8080/api/v2.0/projects" \
  -H "authorization: Basic $(echo -n admin:Harbor12345 | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "odoo-services",
    "public": false,
    "metadata": {
      "auto_scan": "true",
      "severity": "high"
    }
  }'
```

### 6.4 Build and Push Images

```bash
# Tag images for Harbor
for service in auth-service core-erp-service accounting-service inventory-service crm-service; do
  docker tag bravejongen/odoo-$service:latest localhost:8080/odoo-services/odoo-$service:latest
  docker tag bravejongen/odoo-$service:latest localhost:8080/odoo-services/odoo-$service:v1.0.0
  docker push localhost:8080/odoo-services/odoo-$service:latest
  docker push localhost:8080/odoo-services/odoo-$service:v1.0.0
done

# Verify in Harbor UI
# Should see 5 repositories with vulnerability scan results
```

### 6.5 Kubernetes ImagePullSecret

```bash
# Create secret for pulling from Harbor
kubectl create secret docker-registry harbor-secret \
  --namespace odoo-services \
  --docker-server=localhost:8080 \
  --docker-username=admin \
  --docker-password=Harbor12345

# Update deployments to use secret
kubectl patch serviceaccount default \
  -n odoo-services \
  -p '{"imagePullSecrets": [{"name": "harbor-secret"}]}'
```

---

## Phase 7: GitOps with ArgoCD (Days 33-35)

### Objective
Set up ArgoCD for automated GitOps deployments

### 7.1 Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward to ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8081:443
# Access: https://localhost:8081 (admin/<password>)
```

### 7.2 Install ArgoCD CLI

```bash
# Linux
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# Login via CLI
argocd login localhost:8081 --insecure
# Username: admin
# Password: <from previous step>

# Change password
argocd account update-password
```

### 7.3 Connect Git Repository

```bash
# Add repository (use HTTPS)
argocd repo add https://github.com/bravejongen/odoo.git \
  --username bravejongen \
  --password <github-personal-access-token>

# Or add via SSH
ssh-keygen -t ed25519 -C "argocd@odoo" -f ~/.ssh/argocd_ed25519
argocd repo add git@github.com:bravejongen/odoo.git \
  --ssh-private-key-path ~/.ssh/argocd_ed25519

# Verify
argocd repo list
```

### 7.4 Create ArgoCD Applications

Create `argocd/apps/auth-service.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: auth-service
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/bravejongen/odoo.git
    targetRevision: Odoo-19.0-microservices
    path: k8s/services/auth-service
  destination:
    server: https://kubernetes.default.svc
    namespace: odoo-services
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

Apply all applications:

```bash
# Create app for each service
kubectl apply -f argocd/apps/

# Or use ArgoCD CLI
for service in auth-service core-erp-service accounting-service inventory-service crm-service; do
  argocd app create $service \
    --repo https://github.com/bravejongen/odoo.git \
    --path k8s/services/$service \
    --dest-server https://kubernetes.default.svc \
    --dest-namespace odoo-services \
    --revision Odoo-19.0-microservices \
    --sync-policy automated \
    --auto-prune \
    --self-heal
done
```

### 7.5 App of Apps Pattern

Create `argocd/root-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: odoo-root
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/bravejongen/odoo.git
    targetRevision: Odoo-19.0-microservices
    path: argocd/apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```bash
kubectl apply -f argocd/root-app.yaml
```

### 7.6 Monitor Deployments

```bash
# Watch all applications
argocd app list

# Get specific app details
argocd app get auth-service

# View sync status
argocd app sync auth-service

# View application logs
argocd app logs auth-service --tail 100 -f

# Diff between Git and cluster
argocd app diff auth-service
```

---

## Phase 8: CI/CD Pipeline (Days 36-38)

### Objective
Automate build, test, and deployment with GitHub Actions or Azure DevOps

### 8.1 GitHub Actions Pipeline

Create `.github/workflows/microservices-ci-cd.yml`:

```yaml
name: Microservices CI/CD

on:
  push:
    branches: [Odoo-19.0-microservices]
    paths:
      - 'microservices/**'
      - 'k8s/**'
  pull_request:
    branches: [Odoo-19.0-microservices]

env:
  HARBOR_REGISTRY: harbor.yourdomain.com
  HARBOR_PROJECT: odoo-services

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
      
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            auth-service:
              - 'microservices/auth-service/**'
            accounting-service:
              - 'microservices/accounting-service/**'
            inventory-service:
              - 'microservices/inventory-service/**'
            crm-service:
              - 'microservices/crm-service/**'

  build-and-test:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.services != '[]' }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJSON(needs.detect-changes.outputs.services) }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd microservices/${{ matrix.service }}
          pip install -r requirements.txt
          pip install pytest pytest-cov black flake8 mypy
      
      - name: Lint code
        run: |
          cd microservices/${{ matrix.service }}
          black --check .
          flake8 . --max-line-length=120
          mypy . --ignore-missing-imports
      
      - name: Run tests
        run: |
          cd microservices/${{ matrix.service }}
          pytest tests/ -v --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./microservices/${{ matrix.service }}/coverage.xml
          flags: ${{ matrix.service }}
      
      - name: Build Docker image
        run: |
          cd microservices/${{ matrix.service }}
          docker build -t ${{ env.HARBOR_REGISTRY }}/${{ env.HARBOR_PROJECT }}/${{ matrix.service }}:${{ github.sha }} .
          docker build -t ${{ env.HARBOR_REGISTRY }}/${{ env.HARBOR_PROJECT }}/${{ matrix.service }}:latest .
      
      - name: Login to Harbor
        uses: docker/login-action@v3
        with:
          registry: ${{ env.HARBOR_REGISTRY }}
          username: ${{ secrets.HARBOR_USERNAME }}
          password: ${{ secrets.HARBOR_PASSWORD }}
      
      - name: Push Docker image
        run: |
          docker push ${{ env.HARBOR_REGISTRY }}/${{ env.HARBOR_PROJECT }}/${{ matrix.service }}:${{ github.sha }}
          docker push ${{ env.HARBOR_REGISTRY }}/${{ env.HARBOR_PROJECT }}/${{ matrix.service }}:latest
      
      - name: Update Kubernetes manifests
        run: |
          cd k8s/services/${{ matrix.service }}
          sed -i 's|image:.*|image: ${{ env.HARBOR_REGISTRY }}/${{ env.HARBOR_PROJECT }}/${{ matrix.service }}:${{ github.sha }}|' deployment.yaml
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add deployment.yaml
          git commit -m "Update ${{ matrix.service }} image to ${{ github.sha }}"
          git push

  deploy-dev:
    needs: build-and-test
    runs-on: ubuntu-latest
    environment: development
    
    steps:
      - name: Trigger ArgoCD Sync
        run: |
          argocd app sync odoo-services --auth-token ${{ secrets.ARGOCD_TOKEN }}
          argocd app wait odoo-services --health --timeout 300

  integration-tests:
    needs: deploy-dev
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run integration tests
        run: |
          pip install pytest requests
          pytest tests/integration/ -v --base-url=https://dev.odoo.yourdomain.com
      
      - name: Run performance tests
        run: |
          pip install locust
          locust -f tests/performance/locustfile.py --headless -u 100 -r 10 --run-time 5m --host=https://dev.odoo.yourdomain.com

  deploy-production:
    needs: integration-tests
    if: github.ref == 'refs/heads/Odoo-19.0-microservices' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Deploy to production
        run: |
          argocd app sync odoo-services-prod --auth-token ${{ secrets.ARGOCD_TOKEN }}
          argocd app wait odoo-services-prod --health --timeout 600
      
      - name: Smoke tests
        run: |
          curl -f https://odoo.yourdomain.com/health || exit 1
          curl -f https://odoo.yourdomain.com/api/v1/auth/health || exit 1
```

### 8.2 Azure DevOps Pipeline

Create `azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - Odoo-19.0-microservices
  paths:
    include:
      - microservices/*
      - k8s/*

variables:
  harborRegistry: 'harbor.yourdomain.com'
  harborProject: 'odoo-services'

stages:
- stage: Build
  jobs:
  - job: BuildServices
    strategy:
      matrix:
        auth:
          serviceName: 'auth-service'
        accounting:
          serviceName: 'accounting-service'
        inventory:
          serviceName: 'inventory-service'
    
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'
    
    - script: |
        cd microservices/$(serviceName)
        pip install -r requirements.txt
        pip install pytest pytest-cov
        pytest tests/ -v --cov=. --cov-report=html
      displayName: 'Run tests'
    
    - task: Docker@2
      inputs:
        containerRegistry: 'HarborConnection'
        repository: '$(harborProject)/$(serviceName)'
        command: 'buildAndPush'
        Dockerfile: 'microservices/$(serviceName)/Dockerfile'
        tags: |
          $(Build.BuildId)
          latest

- stage: DeployDev
  dependsOn: Build
  jobs:
  - deployment: DeployToDev
    environment: 'development'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              argocd app sync odoo-services
            displayName: 'Trigger ArgoCD Sync'

- stage: DeployProd
  dependsOn: DeployDev
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/Odoo-19.0-microservices'))
  jobs:
  - deployment: DeployToProduction
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: |
              argocd app sync odoo-services-prod
            displayName: 'Deploy to Production'
```

---

## Phase 9: Cloud Infrastructure - AWS EKS (Days 39-45)

# OR login to Docker Hub
docker login
# Username: bravejongen
```

### 2.3 Tag and Push Images

```bash
# For Harbor
docker tag odoo:19.0-local harbor.local:8080/odoo/odoo:19.0
docker tag odoo:19.0-local harbor.local:8080/odoo/odoo:latest
docker push harbor.local:8080/odoo/odoo:19.0
docker push harbor.local:8080/odoo/odoo:latest

# For Docker Hub (already done previously)
docker tag odoo:19.0-local bravejongen/odoo:19.0-microservices
docker tag odoo:19.0-local bravejongen/odoo:latest
docker push bravejongen/odoo:19.0-microservices
docker push bravejongen/odoo:latest
```

### 2.4 Configure Kubernetes to Pull from Registry

```bash
# Create docker-registry secret
kubectl create secret docker-registry harbor-registry -n odoo-dev \
  --docker-server=harbor.local:8080 \
  --docker-username=admin \
  --docker-password=Harbor12345 \
  --docker-email=admin@odoo.local

# OR for Docker Hub
kubectl create secret docker-registry dockerhub-registry -n odoo-dev \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=bravejongen \
  --docker-password=YOUR_DOCKER_PASSWORD \
  --docker-email=your-email@example.com

# Update deployment to use image pull secret
# (will be done in k8s manifests)
```

### 2.5 Harbor Security Configuration

```bash
# Enable vulnerability scanning in Harbor
# 1. Login to Harbor UI: http://harbor.local:8080
# 2. Go to Projects → odoo → Configuration
# 3. Enable "Automatically scan images on push"
# 4. Set deployment security: Prevent vulnerable images from running

# Create Harbor robot account for CI/CD
# 1. Projects → odoo → Robot Accounts
# 2. Create robot account: odoo-ci
# 3. Save token for CI/CD pipeline
```

---

## Phase 3: GitOps with ArgoCD (Days 6-8)

### Objective
Implement GitOps workflow with ArgoCD for automated deployments

### 3.1 Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=300s

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Access ArgoCD: https://localhost:8080
# Username: admin
# Password: (from command above)
```

### 3.2 Install ArgoCD CLI

```bash
# Download CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

# Login via CLI
argocd login localhost:8080 --insecure --username admin --password <password>

# Change admin password
argocd account update-password
```

### 3.3 Connect GitHub Repository

```bash
# Add repository via CLI
argocd repo add git@github.com:Brave-Full-Stack/odoo.git \
  --ssh-private-key-path ~/.ssh/id_rsa \
  --name odoo-repo

# OR add via UI:
# Settings → Repositories → Connect Repo
# Via SSH: git@github.com:Brave-Full-Stack/odoo.git
```

### 3.4 Create ArgoCD Application

```bash
# Create app for dev environment
argocd app create odoo-dev \
  --repo git@github.com:Brave-Full-Stack/odoo.git \
  --path k8s/overlays/dev \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace odoo-dev \
  --sync-policy automated \
  --self-heal \
  --auto-prune

# Create app for production environment
argocd app create odoo-prod \
  --repo git@github.com:Brave-Full-Stack/odoo.git \
  --path k8s/overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace odoo-prod \
  --sync-policy manual

# View applications
argocd app list
argocd app get odoo-dev
```

### 3.5 Configure ArgoCD Application (YAML)

Create `argocd/application-dev.yaml`:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: odoo-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:Brave-Full-Stack/odoo.git
    targetRevision: Odoo-19.0-microservices
    path: k8s/overlays/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: odoo-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
    - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

Apply:
```bash
kubectl apply -f argocd/application-dev.yaml -n argocd
```

### 3.6 ArgoCD Notifications (Optional)

```bash
# Install ArgoCD notifications
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/stable/manifests/install.yaml

# Configure Slack/Email notifications
# Edit argocd-notifications-cm ConfigMap
```

### 3.7 GitOps Workflow

Now your workflow is:
1. **Make changes** → Push to GitHub
2. **ArgoCD detects change** → Syncs automatically (dev)
3. **Review in dev** → Promote to prod
4. **Manual approval** → Sync to production

```bash
# Example: Update image version
git checkout Odoo-19.0-microservices
# Edit k8s/overlays/dev/kustomization.yaml to change image tag
git add . && git commit -m "chore: Update to odoo:19.0.1"
git push

# ArgoCD automatically detects and syncs (if auto-sync enabled)
argocd app sync odoo-dev

# Monitor sync
argocd app wait odoo-dev --health
```

---

## Phase 4: CI/CD Pipeline (Days 9-12)

### Objective
Automate build, test, scan, and deployment process

### 4.1 GitHub Actions Pipeline (Recommended)

Create `.github/workflows/build-and-deploy.yaml`:

```yaml
name: Build and Deploy Odoo

on:
  push:
    branches:
      - Odoo-19.0-microservices
    paths:
      - 'odoo/**'
      - 'addons/**'
      - 'Dockerfile'
      - 'k8s/**'
  pull_request:
    branches:
      - Odoo-19.0-microservices

env:
  REGISTRY: harbor.local:8080
  IMAGE_NAME: odoo/odoo
  DOCKER_HUB_USERNAME: bravejongen

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ || echo "No tests yet"
    
    - name: Lint Python code
      run: |
        pip install ruff
        ruff check . || true
  
  build-and-push:
    needs: build-and-test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ env.DOCKER_HUB_USERNAME }}
        password: ${{ secrets.DOCKER_HUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.DOCKER_HUB_USERNAME }}/odoo
        tags: |
          type=raw,value=19.0-microservices
          type=sha,prefix=19.0-
          type=raw,value=latest
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ env.DOCKER_HUB_USERNAME }}/odoo:latest
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
  
  deploy-to-dev:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Update Kustomization
      run: |
        cd k8s/overlays/dev
        kustomize edit set image odoo=${{ env.DOCKER_HUB_USERNAME }}/odoo:19.0-${{ github.sha }}
    
    - name: Commit and push changes
      run: |
        git config --global user.email "github-actions@github.com"
        git config --global user.name "GitHub Actions"
        git add k8s/overlays/dev/kustomization.yaml
        git commit -m "chore: Update dev image to ${{ github.sha }}" || exit 0
        git push
    
    - name: Notify ArgoCD
      run: |
        # ArgoCD will auto-sync the changes
        echo "ArgoCD will detect and deploy the changes"
```

### 4.2 Azure DevOps Pipeline (Alternative)

Update `ci-cd/azure-pipelines/azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
    - Odoo-19.0-microservices
  paths:
    include:
    - odoo/**
    - addons/**
    - Dockerfile
    - k8s/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  dockerRegistryServiceConnection: 'DockerHub'
  imageRepository: 'bravejongen/odoo'
  containerRegistry: 'docker.io'
  dockerfilePath: '$(Build.SourcesDirectory)/Dockerfile'
  tag: '19.0-$(Build.BuildId)'

stages:
- stage: Build
  displayName: Build and Test
  jobs:
  - job: Build
    displayName: Build Odoo
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'
      displayName: 'Use Python 3.12'
    
    - script: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
      displayName: 'Install dependencies'
    
    - script: |
        python -m pytest tests/ || echo "No tests yet"
      displayName: 'Run tests'

- stage: Docker
  displayName: Build and Push Docker Image
  dependsOn: Build
  jobs:
  - job: BuildPush
    displayName: Build and Push
    steps:
    - task: Docker@2
      displayName: Build and push image
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          latest

- stage: Deploy
  displayName: Deploy to Dev
  dependsOn: Docker
  jobs:
  - deployment: DeployDev
    displayName: Deploy to Development
    environment: 'odoo-dev'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            displayName: Deploy to Kubernetes
            inputs:
              action: deploy
              manifests: |
                $(Pipeline.Workspace)/k8s/overlays/dev
```

### 4.3 Configure GitHub Secrets

```bash
# Add secrets to GitHub repository
# Settings → Secrets and variables → Actions → New repository secret

# Required secrets:
DOCKER_HUB_TOKEN           # Docker Hub access token
HARBOR_USERNAME            # Harbor admin username (if using Harbor)
HARBOR_PASSWORD            # Harbor password
AWS_ACCESS_KEY_ID          # For AWS EKS
AWS_SECRET_ACCESS_KEY      # For AWS EKS
KUBE_CONFIG                # Kubernetes config (for direct deployment)
ARGOCD_AUTH_TOKEN          # ArgoCD API token
```

### 4.4 Testing CI/CD Pipeline

```bash
# Test locally with act (GitHub Actions locally)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
act -l  # List workflows
act push  # Run push workflow locally

# Create test commit
git checkout Odoo-19.0-microservices
echo "# Test" >> README.md
git add README.md
git commit -m "test: Trigger CI/CD pipeline"
git push

# Monitor workflow
# GitHub → Actions tab
# Or via CLI:
gh run list
gh run watch
```

---

## Phase 9: Cloud Infrastructure - AWS EKS (Days 39-45)

### Objective
Deploy production microservices infrastructure on AWS EKS

### 9.1 Install Required Tools

```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
terraform version

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version

# Configure AWS credentials
aws configure
# AWS Access Key ID: YOUR_KEY
# AWS Secret Access Key: YOUR_SECRET
# Default region: eu-west-1
# Default output format: json

# Install kubectl AWS IAM authenticator
curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_linux_amd64
chmod +x aws-iam-authenticator
sudo mv aws-iam-authenticator /usr/local/bin/
```

### 9.2 Terraform EKS Configuration

Create `terraform/aws-eks/main.tf`:

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
  
  backend "s3" {
    bucket = "odoo-terraform-state"
    key    = "eks/terraform.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = false  # High availability
  enable_dns_hostnames = true
  enable_dns_support   = true

  # Kubernetes tags
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  tags = var.tags
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.public_subnets

  # Cluster endpoint configuration
  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  # Encryption
  cluster_encryption_config = {
    resources        = ["secrets"]
    provider_key_arn = aws_kms_key.eks.arn
  }

  # Add-ons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent    = true
      before_compute = true
      configuration_values = jsonencode({
        env = {
          ENABLE_PREFIX_DELEGATION = "true"
          ENABLE_POD_ENI           = "true"
          POD_SECURITY_GROUP_ENFORCING_MODE = "standard"
        }
      })
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  # Node groups
  eks_managed_node_groups = {
    # System node group (for Istio, monitoring, etc.)
    system = {
      name           = "system-nodes"
      instance_types = ["t3.large"]
      min_size       = 2
      max_size       = 4
      desired_size   = 2

      labels = {
        role = "system"
      }

      taints = [{
        key    = "system"
        value  = "true"
        effect = "NoSchedule"
      }]
    }

    # Application node group (for microservices)
    apps = {
      name           = "app-nodes"
      instance_types = ["t3.xlarge"]
      min_size       = 3
      max_size       = 10
      desired_size   = 3

      labels = {
        role = "application"
      }
    }

    # Database node group (for PostgreSQL pods)
    data = {
      name           = "data-nodes"
      instance_types = ["r5.large"]  # Memory-optimized
      min_size       = 2
      max_size       = 4
      desired_size   = 2

      labels = {
        role = "database"
      }

      taints = [{
        key    = "database"
        value  = "true"
        effect = "NoSchedule"
      }]
    }
  }

  # Cluster security group rules
  cluster_security_group_additional_rules = {
    egress_nodes_ephemeral_ports_tcp = {
      description                = "To node 1025-65535"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "egress"
      source_node_security_group = true
    }
  }

  # Node security group rules
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
    
    # Istio ports
    ingress_istio_webhook = {
      description = "Istio webhook"
      protocol    = "tcp"
      from_port   = 15017
      to_port     = 15017
      type        = "ingress"
      self        = true
    }
  }

  # AWS auth - allow IAM users/roles to access cluster
  manage_aws_auth_configmap = true

  aws_auth_users = [
    {
      userarn  = "arn:aws:iam::ACCOUNT_ID:user/admin"
      username = "admin"
      groups   = ["system:masters"]
    }
  ]

  tags = var.tags
}

# KMS key for EKS encryption
resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption Key"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = var.tags
}

resource "aws_kms_alias" "eks" {
  name          = "alias/${var.cluster_name}-eks"
  target_key_id = aws_kms_key.eks.key_id
}

# RDS for PostgreSQL (for production databases)
resource "aws_db_subnet_group" "odoo" {
  name       = "${var.cluster_name}-db-subnet"
  subnet_ids = module.vpc.private_subnets

  tags = var.tags
}

resource "aws_security_group" "rds" {
  name_prefix = "${var.cluster_name}-rds-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  tags = var.tags
}

# ElastiCache for Redis
resource "aws_elasticache_subnet_group" "odoo" {
  name       = "${var.cluster_name}-cache-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "elasticache" {
  name_prefix = "${var.cluster_name}-cache-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  tags = var.tags
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "${var.cluster_name}-redis"
  replication_group_description = "Redis for Odoo microservices"
  engine                     = "redis"
  engine_version             = "7.0"
  node_type                  = "cache.r5.large"
  number_cache_clusters      = 2
  port                       = 6379
  subnet_group_name          = aws_elasticache_subnet_group.odoo.name
  security_group_ids         = [aws_security_group.elasticache.id]
  automatic_failover_enabled = true
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  tags = var.tags
}
```

Create `terraform/aws-eks/variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "odoo-microservices-eks"
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default = {
    Project     = "Odoo-Microservices"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}
```

### 9.3 Deploy EKS Cluster

```bash
cd terraform/aws-eks

# Initialize Terraform
terraform init

# Create S3 bucket for state (first time only)
aws s3 mb s3://odoo-terraform-state --region eu-west-1
aws s3api put-bucket-versioning \
  --bucket odoo-terraform-state \
  --versioning-configuration Status=Enabled

# Plan deployment
terraform plan -out=tfplan

# Apply configuration
terraform apply tfplan
# This takes 15-20 minutes

# Configure kubectl
aws eks update-kubeconfig --region eu-west-1 --name odoo-microservices-eks

# Verify cluster access
kubectl get nodes
kubectl get pods -A
```

### 9.4 Install Core Components on EKS

```bash
# Install Istio
istioctl install --set profile=production -y

# Install Prometheus Operator
kubectl create -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml

# Install Cert-Manager (for TLS)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml

# Install External DNS (for Route53)
helm install external-dns bitnami/external-dns \
  --set provider=aws \
  --set aws.region=eu-west-1 \
  --set txtOwnerId=odoo-microservices \
  --set policy=sync

# Install AWS Load Balancer Controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=odoo-microservices-eks \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 9.5 Deploy Microservices to EKS

```bash
# Update ArgoCD to point to EKS
kubectl config use-context arn:aws:eks:eu-west-1:ACCOUNT_ID:cluster/odoo-microservices-eks

# Add EKS cluster to ArgoCD
argocd cluster add arn:aws:eks:eu-west-1:ACCOUNT_ID:cluster/odoo-microservices-eks

# Create production ArgoCD applications
for service in auth-service core-erp-service accounting-service inventory-service crm-service; do
  argocd app create $service-prod \
    --repo https://github.com/bravejongen/odoo.git \
    --path k8s/overlays/production/$service \
    --dest-server https://eks-cluster-endpoint \
    --dest-namespace odoo-production \
    --sync-policy automated
done

# Monitor deployment
argocd app list
kubectl get pods -n odoo-production -w
```

### 9.6 Configure Production Ingress

Create `k8s/production/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: odoo-ingress
  namespace: odoo-production
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:eu-west-1:ACCOUNT_ID:certificate/CERT_ID
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    external-dns.alpha.kubernetes.io/hostname: odoo.yourdomain.com
spec:
  rules:
  - host: odoo.yourdomain.com
    http:
      paths:
      - path: /api/v1/auth
        pathType: Prefix
        backend:
          service:
            name: auth-service
            port:
              number: 8080
      - path: /api/v1/accounting
        pathType: Prefix
        backend:
          service:
            name: accounting-service
            port:
              number: 8080
      - path: /api/v1/inventory
        pathType: Prefix
        backend:
          service:
            name: inventory-service
            port:
              number: 8080
```

```bash
kubectl apply -f k8s/production/ingress.yaml

# Get ALB DNS name
kubectl get ingress -n odoo-production odoo-ingress
```

### 9.7 Production Monitoring Setup

```bash
# Create Grafana LoadBalancer
kubectl expose deployment grafana -n istio-system \
  --type=LoadBalancer \
  --name=grafana-lb \
  --port=3000

# Get Grafana URL
kubectl get svc grafana-lb -n istio-system

# Configure CloudWatch integration
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: istio-system
data:
  prometheus.yml: |
    remote_write:
      - url: https://aps-workspaces.eu-west-1.amazonaws.com/workspaces/ws-xxx/api/v1/remote_write
        sigv4:
          region: eu-west-1
        queue_config:
          max_samples_per_send: 1000
          max_shards: 200
          capacity: 2500
EOF
```

---

## Phase 10: Production Optimization (Days 46-50)

### Objective
Fine-tune production environment for performance, security, and cost

### 10.1 Horizontal Pod Autoscaling

Create HPA for each service:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: auth-service-hpa
  namespace: odoo-production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: auth-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
```

```bash
kubectl apply -f k8s/production/hpa/
```

### 10.2 Cluster Autoscaler

```bash
# Enable Cluster Autoscaler in Terraform (already configured)
# Or install via Helm
helm install cluster-autoscaler autoscaler/cluster-autoscaler \
  --namespace kube-system \
  --set autoDiscovery.clusterName=odoo-microservices-eks \
  --set awsRegion=eu-west-1 \
  --set rbac.serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::ACCOUNT_ID:role/cluster-autoscaler

# Verify autoscaler
kubectl logs -f deployment/cluster-autoscaler -n kube-system
```

### 10.3 Database Performance Tuning

```sql
-- Connect to each service database and optimize
-- Example for accounting DB

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM invoices WHERE state = 'draft';

-- Add indexes
CREATE INDEX idx_invoices_state ON invoices(state);
CREATE INDEX idx_invoices_partner_date ON invoices(partner_id, date);

-- Vacuum and analyze
VACUUM ANALYZE invoices;

-- Configure connection pooling (PgBouncer)
```

Deploy PgBouncer:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgbouncer-accounting
  namespace: odoo-production
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pgbouncer
      service: accounting
  template:
    metadata:
      labels:
        app: pgbouncer
        service: accounting
    spec:
      containers:
      - name: pgbouncer
        image: edoburu/pgbouncer:latest
        ports:
        - containerPort: 5432
        env:
        - name: DATABASE_URL
          value: "postgres://user:pass@rds-endpoint:5432/accounting_db"
        - name: POOL_MODE
          value: "transaction"
        - name: MAX_CLIENT_CONN
          value: "1000"
        - name: DEFAULT_POOL_SIZE
          value: "25"
```

### 10.4 Caching Strategy

```python
# Add Redis caching to services
from redis import Redis
from functools import wraps
import json
import hashlib

redis_client = Redis(host='redis.odoo-production.svc.cluster.local', port=6379)

def cached(ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = hashlib.md5(
                f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}".encode()
            ).hexdigest()
            
            # Try cache first
            cached_value = redis_client.get(key)
            if cached_value:
                return json.loads(cached_value)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

# Usage
@app.get("/api/v1/partners/{partner_id}")
@cached(ttl=600)  # Cache for 10 minutes
async def get_partner(partner_id: int):
    # Expensive database query
    return query_partner(partner_id)
```

### 10.5 Rate Limiting and Throttling

Update Kong configuration:

```bash
# Global rate limiting
curl -X POST http://$KONG_ADMIN:8001/plugins \
  --data name=rate-limiting \
  --data config.minute=1000 \
  --data config.hour=10000 \
  --data config.policy=cluster \
  --data config.fault_tolerant=true

# Per-consumer rate limiting
curl -X POST http://$KONG_ADMIN:8001/consumers/premium-user/plugins \
  --data name=rate-limiting \
  --data config.minute=5000

# Response rate limiting (for heavy endpoints)
curl -X POST http://$KONG_ADMIN:8001/services/reporting-service/plugins \
  --data name=rate-limiting \
  --data config.minute=100
```

### 10.6 Security Hardening

```bash
# Enable Pod Security Standards
kubectl label namespace odoo-production pod-security.kubernetes.io/enforce=restricted

# Network Policies
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: odoo-production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-accounting-to-db
  namespace: odoo-production
spec:
  podSelector:
    matchLabels:
      app: accounting-service
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432
EOF

# OPA Gatekeeper policies
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Require resource limits
kubectl apply -f - <<EOF
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: must-have-resources
spec:
  match:
    kinds:
    - apiGroups: ["apps"]
      kinds: ["Deployment"]
    namespaces: ["odoo-production"]
  parameters:
    limits: ["memory", "cpu"]
    requests: ["memory", "cpu"]
EOF
```

### 10.7 Backup and Disaster Recovery

```bash
# Install Velero for cluster backups
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm install velero vmware-tanzu/velero \
  --namespace velero --create-namespace \
  --set configuration.provider=aws \
  --set configuration.backupStorageLocation.bucket=odoo-backups \
  --set configuration.backupStorageLocation.config.region=eu-west-1 \
  --set snapshotsEnabled=true \
  --set deployRestic=true

# Create backup schedule
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces odoo-production \
  --ttl 720h

# Database backups (RDS automated backups already enabled)
# Create additional manual snapshots
aws rds create-db-snapshot \
  --db-instance-identifier odoo-accounting-db \
  --db-snapshot-identifier accounting-manual-$(date +%Y%m%d-%H%M%S)
```

### 10.8 Cost Optimization

```bash
# Use Spot Instances for non-critical workloads
# Update Terraform with mixed instance types

# Enable AWS Savings Plans
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days 7

# Right-size resources based on actual usage
kubectl top nodes
kubectl top pods -n odoo-production --sort-by=cpu
kubectl top pods -n odoo-production --sort-by=memory

# Use Kubecost for cost visibility
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost --create-namespace \
  --set kubecostToken="YOUR_TOKEN"

kubectl port-forward -n kubecost deployment/kubecost-cost-analyzer 9090:9090
# Access: http://localhost:9090
```

### 10.9 Load Testing

Create `tests/performance/locustfile.py`:

```python
from locust import HttpUser, task, between
import random

class OdooUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login and get token
        response = self.client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def list_partners(self):
        self.client.get("/api/v1/partners", headers=self.headers)
    
    @task(2)
    def get_invoices(self):
        self.client.get("/api/v1/accounting/invoices", headers=self.headers)
    
    @task(1)
    def create_invoice(self):
        self.client.post("/api/v1/accounting/invoices", 
            headers=self.headers,
            json={
                "partner_id": random.randint(1, 100),
                "amount": random.uniform(100, 10000),
                "date": "2024-01-15"
            }
        )
```

```bash
# Run load test
pip install locust
locust -f tests/performance/locustfile.py \
  --headless \
  -u 1000 \
  -r 100 \
  --run-time 30m \
  --host https://odoo.yourdomain.com \
  --html load-test-report.html

# Analyze results
# - Response time percentiles
# - Requests per second
# - Failure rate
# - Resource utilization during test
```

### 10.10 Production Readiness Checklist

- [ ] All services have HPA configured
- [ ] Cluster Autoscaler is enabled
- [ ] Database indexes are optimized
- [ ] PgBouncer is deployed for connection pooling
- [ ] Redis caching is implemented
- [ ] Rate limiting is configured
- [ ] Network policies are enforced
- [ ] OPA Gatekeeper policies are active
- [ ] Pod Security Standards are enforced
- [ ] Backups are scheduled (Velero + RDS)
- [ ] Monitoring dashboards are configured
- [ ] Alerts are set up (PagerDuty/Slack)
- [ ] Load testing passed (1000+ concurrent users)
- [ ] Disaster recovery plan is documented
- [ ] Cost optimization analysis completed
- [ ] Security scan passed (no critical vulnerabilities)
- [ ] Documentation is up to date

---

## Timeline Summary

| Phase | Duration | Description |
|-------|----------|-------------|
| **Phase 0** | Days 1-10 | Microservices design, DDD, service boundaries |
| **Phase 1** | Days 11-18 | Service mesh setup (Istio, mTLS, traffic management) |
| **Phase 2** | Days 11-18 | Core services development (auth, core-erp, accounting) |
| **Phase 3** | Days 19-22 | Event bus & messaging (RabbitMQ, event schemas) |
| **Phase 4** | Days 23-26 | Observability stack (Prometheus, Grafana, Jaeger, EFK) |
| **Phase 5** | Days 27-30 | API Gateway & Security (Kong, OAuth2, JWT, rate limiting) |
| **Phase 6** | Days 31-32 | Container Registry (Harbor, vulnerability scanning) |
| **Phase 7** | Days 33-35 | GitOps with ArgoCD (automated deployments) |
| **Phase 8** | Days 36-38 | CI/CD Pipeline (GitHub Actions/Azure DevOps) |
| **Phase 9** | Days 39-45 | AWS EKS deployment (production infrastructure) |
| **Phase 10** | Days 46-50 | Production optimization (autoscaling, caching, security) |

**Total Duration**: 7-8 weeks (50 days)

---

## Testing & Validation

### Unit Testing

```bash
# Each service should have pytest tests
cd microservices/auth-service
pytest tests/ -v --cov=. --cov-report=html

# Coverage requirements: >80%
```

### Integration Testing

```python
# tests/integration/test_invoice_flow.py
import pytest
import httpx

BASE_URL = "https://odoo.yourdomain.com"

@pytest.fixture
async def auth_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/v1/auth/login", json={
            "username": "test", "password": "test"
        })
        return response.json()["access_token"]

@pytest.mark.asyncio
async def test_invoice_creation_flow(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    async with httpx.AsyncClient() as client:
        # Create partner
        partner_resp = await client.post(f"{BASE_URL}/api/v1/partners",
            headers=headers,
            json={"name": "Test Partner", "email": "test@example.com"}
        )
        partner_id = partner_resp.json()["id"]
        
        # Create invoice
        invoice_resp = await client.post(f"{BASE_URL}/api/v1/accounting/invoices",
            headers=headers,
            json={"partner_id": partner_id, "amount": 1000.0}
        )
        assert invoice_resp.status_code == 200
        invoice_id = invoice_resp.json()["id"]
        
        # Verify invoice was created
        get_resp = await client.get(f"{BASE_URL}/api/v1/accounting/invoices/{invoice_id}",
            headers=headers
        )
        assert get_resp.json()["partner_id"] == partner_id
```

### End-to-End Testing

```bash
# Use Cypress or Playwright for frontend E2E tests
npm install --save-dev @playwright/test

# tests/e2e/invoice.spec.ts
import { test, expect } from '@playwright/test';

test('create invoice flow', async ({ page }) => {
  await page.goto('https://odoo.yourdomain.com');
  await page.fill('[name=username]', 'admin');
  await page.fill('[name=password]', 'admin');
  await page.click('button[type=submit]');
  
  await page.click('text=Accounting');
  await page.click('text=Invoices');
  await page.click('text=Create');
  
  await page.fill('[name=partner]', 'Test Partner');
  await page.fill('[name=amount]', '1000');
  await page.click('text=Save');
  
  await expect(page.locator('text=Invoice created successfully')).toBeVisible();
});
```

---

## Troubleshooting Guide

### Service Communication Issues

```bash
# Check Istio sidecar injection
kubectl get pods -n odoo-services -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

# Verify mTLS
istioctl x describe pod auth-service-xxx -n odoo-services

# Check service mesh traffic
kubectl logs -n odoo-services auth-service-xxx -c istio-proxy -f

# Debug with ephemeral container
kubectl debug -it auth-service-xxx -n odoo-services --image=curlimages/curl -- sh
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- \
  psql -h postgresql.odoo-services.svc.cluster.local -U odoo -d accounting

# Check PgBouncer stats
kubectl exec -it pgbouncer-xxx -n odoo-services -- psql -p 6432 -U pgbouncer pgbouncer -c "SHOW STATS;"

# View connection pool
kubectl exec -it pgbouncer-xxx -n odoo-services -- psql -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"
```

### Performance Issues

```bash
# Check resource usage
kubectl top pods -n odoo-services --sort-by=cpu
kubectl top nodes

# View slow queries
kubectl exec -it postgresql-0 -n odoo-services -- \
  psql -U postgres -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"

# Check Istio latency
istioctl dashboard envoy auth-service-xxx.odoo-services
```

### ArgoCD Sync Issues

```bash
# View app status
argocd app get auth-service

# View sync errors
argocd app logs auth-service

# Force sync
argocd app sync auth-service --force

# Diff between Git and cluster
argocd app diff auth-service
```

---

## Best Practices

### 1. Service Design
- Keep services small and focused (single responsibility)
- Design for failure (circuit breakers, retries)
- Use asynchronous communication for non-critical operations
- Implement idempotency for all state-changing operations

### 2. Database Management
- One database per service
- Use database migrations (Alembic/Flyway)
- No direct database access between services
- Eventual consistency is acceptable

### 3. API Design
- Use REST for synchronous, gRPC for high-performance
- Version all APIs (/api/v1/)
- Implement proper error handling
- Use OpenAPI/Swagger for documentation

### 4. Security
- Use mTLS for inter-service communication
- Implement OAuth2/JWT for authentication
- Store secrets in Kubernetes Secrets or AWS Secrets Manager
- Regular security scans (Trivy, Snyk)

### 5. Monitoring
- Implement structured logging (JSON)
- Use correlation IDs for request tracing
- Set up alerts for critical metrics
- Regular performance reviews

---

## Additional Resources

- [Istio Documentation](https://istio.io/latest/docs/)
- [Kong API Gateway](https://docs.konghq.com/)
- [ArgoCD Best Practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- [AWS EKS Workshop](https://www.eksworkshop.com/)
- [Microservices Patterns](https://microservices.io/patterns/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

---

**Last Updated**: January 2024  
**Version**: 2.0.0  
**Branch**: Odoo-19.0-microservices
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    odoo_nodes = {
      desired_size = 2
      min_size     = 1
      max_size     = 4

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = "production"
        Application = "odoo"
      }

      tags = {
        Name = "odoo-node"
      }
    }
  }

  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}

# EBS CSI Driver (for persistent volumes)
resource "aws_eks_addon" "ebs_csi_driver" {
  cluster_name = module.eks.cluster_name
  addon_name   = "aws-ebs-csi-driver"
}

# Outputs
output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_name" {
  value = module.eks.cluster_name
}

output "kubeconfig_command" {
  value = "aws eks update-kubeconfig --region ${var.aws_region} --name ${var.cluster_name}"
}
```

#### 5.1.3 Deploy Infrastructure

```bash
cd terraform/aws-eks/

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan -out=tfplan

# Apply (create infrastructure)
terraform apply tfplan

# This will take 15-20 minutes
# After completion, configure kubectl:
aws eks update-kubeconfig --region eu-west-1 --name odoo-eks-cluster

# Verify cluster access
kubectl get nodes
kubectl get ns
```

### 5.2 Option B: Pulumi (Infrastructure as Code alternative)

#### 5.2.1 Install Pulumi

```bash
# Install Pulumi
curl -fsSL https://get.pulumi.com | sh
export PATH=$PATH:$HOME/.pulumi/bin
pulumi version

# Login to Pulumi (free for individuals)
pulumi login
```

#### 5.2.2 Create Pulumi Project

```bash
mkdir -p pulumi/aws-eks
cd pulumi/aws-eks

# Initialize Python project
pulumi new aws-python --name odoo-eks --description "Odoo EKS infrastructure"

# Install dependencies
pip install pulumi pulumi-aws pulumi-eks pulumi-kubernetes
```

Create `__main__.py`:

```python
import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s

# Configuration
config = pulumi.Config()
cluster_name = config.get("clusterName") or "odoo-eks"
node_count = config.get_int("nodeCount") or 2
instance_type = config.get("instanceType") or "t3.large"

# Create VPC
vpc = aws.ec2.Vpc("odoo-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": f"{cluster_name}-vpc"}
)

# Create EKS cluster
cluster = eks.Cluster("odoo-eks",
    vpc_id=vpc.id,
    instance_type=instance_type,
    desired_capacity=node_count,
    min_size=1,
    max_size=4,
    tags={"Name": cluster_name}
)

# Install ArgoCD
argocd_namespace = k8s.core.v1.Namespace("argocd",
    metadata={"name": "argocd"},
    opts=pulumi.ResourceOptions(provider=cluster.provider)
)

# Export cluster details
pulumi.export("kubeconfig", cluster.kubeconfig)
pulumi.export("cluster_name", cluster.eks_cluster.name)
pulumi.export("cluster_endpoint", cluster.eks_cluster.endpoint)
```

#### 5.2.3 Deploy with Pulumi

```bash
# Preview deployment
pulumi preview

# Deploy infrastructure
pulumi up --yes

# Get kubeconfig
pulumi stack output kubeconfig > kubeconfig.yaml
export KUBECONFIG=./kubeconfig.yaml

# Verify
kubectl get nodes
```

### 5.3 Install Production Components on EKS

```bash
# Create namespaces
kubectl create namespace odoo-prod
kubectl create namespace argocd
kubectl create namespace harbor

# Install NGINX Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer

# Install cert-manager (for SSL)
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install Harbor (production registry)
helm install harbor harbor/harbor \
  --namespace harbor \
  --set expose.type=loadBalancer \
  --set expose.tls.enabled=true \
  --set externalURL=https://harbor.yourdomain.com \
  --set harborAdminPassword=HarborSecurePassword123

# Wait for LoadBalancers
kubectl get svc -n ingress-nginx
kubectl get svc -n harbor
```

### 5.4 Configure DNS

```bash
# Get LoadBalancer IPs
INGRESS_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
ARGOCD_IP=$(kubectl get svc -n argocd argocd-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
HARBOR_IP=$(kubectl get svc -n harbor harbor -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Update DNS records:
# odoo.yourdomain.com     → CNAME → $INGRESS_IP
# argocd.yourdomain.com   → CNAME → $ARGOCD_IP
# harbor.yourdomain.com   → CNAME → $HARBOR_IP
```

### 5.5 Deploy Odoo to Production

```bash
# Create ArgoCD application for production
argocd app create odoo-prod \
  --repo git@github.com:Brave-Full-Stack/odoo.git \
  --path k8s/overlays/production \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace odoo-prod \
  --sync-policy manual \
  --self-heal \
  --auto-prune

# Manual sync to production
argocd app sync odoo-prod

# Monitor deployment
kubectl get pods -n odoo-prod -w
argocd app wait odoo-prod --health
```

---

## Testing & Validation

### Functional Testing

```bash
# 1. Health checks
kubectl get pods -n odoo-prod
kubectl get svc -n odoo-prod
kubectl describe deployment odoo -n odoo-prod

# 2. Database connectivity
kubectl exec -it -n odoo-prod deploy/postgres -- psql -U odoo -d odoo19 -c '\l'

# 3. Application logs
kubectl logs -n odoo-prod -l app=odoo --tail=100

# 4. HTTP endpoints
curl -I https://odoo.yourdomain.com
curl -I https://odoo.yourdomain.com/web/health

# 5. Load testing
kubectl run -it --rm load-test --image=busybox --restart=Never -- \
  wget -q -O- http://odoo.odoo-prod.svc.cluster.local:8069
```

### Performance Testing

```bash
# Install k6 for load testing
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Create load test script
cat > load-test.js <<EOF
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '3m', target: 10 },
    { duration: '1m', target: 0 },
  ],
};

export default function () {
  const res = http.get('https://odoo.yourdomain.com');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
EOF

# Run test
k6 run load-test.js
```

### Security Testing

```bash
# Scan with Trivy
trivy image bravejongen/odoo:latest

# Scan Kubernetes manifests
trivy config k8s/

# Check RBAC
kubectl auth can-i --list --namespace=odoo-prod

# Network policies
kubectl get networkpolicies -n odoo-prod
```

---

## Troubleshooting Guide

### Common Issues

#### 1. Pods not starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n odoo-prod

# Common fixes:
# - ImagePullBackOff: Check registry credentials
kubectl get secret dockerhub-registry -n odoo-prod -o yaml

# - CrashLoopBackOff: Check logs
kubectl logs <pod-name> -n odoo-prod --previous

# - Pending: Check PVC status
kubectl get pvc -n odoo-prod
```

#### 2. ArgoCD sync issues

```bash
# Check sync status
argocd app get odoo-prod

# Force sync
argocd app sync odoo-prod --force

# Check repo connectivity
argocd repo list
```

#### 3. Database connection issues

```bash
# Test database connectivity
kubectl exec -it -n odoo-prod deploy/odoo -- python3 -c "import psycopg2; conn = psycopg2.connect('dbname=odoo19 user=odoo host=postgres password=odoo123'); print('Connected!')"

# Check service
kubectl get svc postgres -n odoo-prod
```

#### 4. Ingress not working

```bash
# Check ingress
kubectl get ingress -n odoo-prod
kubectl describe ingress odoo -n odoo-prod

# Check ingress controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

---

## Timeline Summary

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| **Phase 1** | Days 1-3 | Local K8s cluster, Odoo running locally |
| **Phase 2** | Days 4-5 | Harbor registry, Images pushed |
| **Phase 3** | Days 6-8 | ArgoCD installed, GitOps workflow |
| **Phase 4** | Days 9-12 | CI/CD pipelines, Automated builds |
| **Phase 5** | Days 13-20 | AWS EKS cluster, Production deployment |

---

## Next Steps

1. **Choose your path**:
   - Quick start: Minikube + Docker Hub + GitHub Actions
   - Production: Kind + Harbor + ArgoCD + AWS EKS + Terraform

2. **Start with Phase 1** (local development)
3. **Add Harbor** (Phase 2) for image management
4. **Implement GitOps** (Phase 3) with ArgoCD
5. **Automate** (Phase 4) with CI/CD
6. **Scale to cloud** (Phase 5) with AWS EKS

Each phase builds on the previous one. Start small, test thoroughly, then expand.

Ready to start? Let me know which phase you'd like to begin with!
