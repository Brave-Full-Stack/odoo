# Getting Started with Odoo Microservices

**Quick Reference Guide for Your VM (8.5 GB RAM, 8 CPU)**

---

## 🚦 Choose Your Path

### PATH A: Learning Track (Recommended)
**What**: Build 2-3 microservices locally with Docker Compose  
**Resources**: Low (~600 MB RAM)  
**Duration**: 1-2 weeks  
**Keep local dev**: ⚠️ Stop during testing  

### PATH B: Production Track
**What**: Deploy full stack to AWS EKS  
**Resources**: None (runs in AWS)  
**Cost**: ~$150-200/month  
**Keep local dev**: ✅ Yes (independent)  

### PATH C: Hybrid (Best for You)
**What**: Local dev for work + Docker Compose for learning  
**Resources**: Switch between them  
**Keep local dev**: ✅ Yes (switch branches)  

---

## 🎯 Quickest Way to Start (30 Minutes)

### Step 1: Create Your First Microservice (10 min)

```bash
# Navigate to odoo directory
cd /home/brave/Desktop/FullStack/odoo

# Switch to microservices branch
git checkout Odoo-19.0-microservices

# Create auth service directory
mkdir -p microservices/auth-service
cd microservices/auth-service

# Download the complete auth service (I provided the code above)
# Or copy from the README sections

# Create virtual environment and test
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-jose passlib[bcrypt] python-multipart pydantic

# Run locally
python main.py
```

**In another terminal:**
```bash
# Test the service
curl http://localhost:8080/health

# Should see: {"status": "healthy", "service": "auth-service", ...}
```

### Step 2: Containerize and Test (10 min)

```bash
# Stop the Python process (Ctrl+C)
cd /home/brave/Desktop/FullStack/odoo

# Create Docker Compose file (see README)
# Build and run
docker-compose -f docker-compose.microservices.yml up -d auth-service

# Test
curl http://localhost:8080/health

# Login test
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

### Step 3: Check Resources (2 min)

```bash
# See what's using resources
docker stats --no-stream

# You should see:
# auth-service: ~200 MB RAM, <1% CPU
# postgres: ~100 MB RAM
```

### Step 4: Clean Up (2 min)

```bash
# Stop services
docker-compose -f docker-compose.microservices.yml down

# Remove containers (optional)
docker system prune -f
```

---

## 📊 Resource Calculator

### Can I Run This?

| Scenario | RAM Needed | Can Run? | Notes |
|----------|------------|----------|-------|
| **Local Dev Only** | 4-5 GB | ✅ Yes | Your current setup |
| **Auth Service (Docker)** | 300 MB | ✅ Yes | Stop local dev first |
| **2 Services (Docker)** | 600 MB | ✅ Yes | Stop local dev first |
| **3 Services + RabbitMQ** | 1.2 GB | ✅ Yes | Stop local dev first |
| **Full K8s + Istio** | 6-8 GB | ⚠️ Tight | Must stop local dev |
| **Both (Local Dev + Microservices)** | 9-11 GB | ❌ No | Not enough RAM |

### Recommendation
**Use Docker Compose instead of Kubernetes for learning**
- Much lighter on resources
- Easier to debug
- Same concepts apply
- Can test inter-service communication

---

## 🔄 Daily Workflow

### Morning: Development Work
```bash
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-local-dev

# Start Odoo (your current setup)
./odoo-bin -c odoo.conf
# Work on features, test, develop...
```

### Afternoon: Learn Microservices
```bash
# Stop local dev
pkill -f odoo-bin

# Switch branch
git checkout Odoo-19.0-microservices

# Start microservices
docker-compose -f docker-compose.microservices.yml up -d

# Test and learn
curl http://localhost:8080/health
curl http://localhost:8081/api/v1/accounting/invoices

# Experiment, break things, learn!
```

### Evening: Back to Normal
```bash
# Stop microservices
docker-compose -f docker-compose.microservices.yml down

# Back to local dev
git checkout Odoo-19.0-local-dev
./odoo-bin -c odoo.conf
```

---

## 🎓 Learning Path (Step by Step)

### Week 1: Understand Microservices

**Day 1**: Read architecture concepts
- Review DEPLOYMENT_PLAN.md Phase 0
- Understand service boundaries
- Learn about event-driven architecture

**Day 2**: Build auth service
- Copy code from README
- Run locally with Python
- Test with curl

**Day 3**: Containerize auth service
- Create Dockerfile
- Build image
- Run with docker-compose

**Day 4**: Build accounting service
- Create second service
- Implement REST API
- Test service-to-service calls

**Day 5**: Test both services
- Start both with docker-compose
- Test login flow
- Test invoice creation
- Check logs and metrics

### Week 2: Add Complexity

**Day 6-7**: Add database persistence
- Connect PostgreSQL
- Create SQLAlchemy models
- Test CRUD operations

**Day 8-9**: Add RabbitMQ events
- Install RabbitMQ container
- Publish invoice.created event
- Consume events in other service

**Day 10**: Add simple API Gateway
- Use nginx as reverse proxy
- Route /auth/* to auth service
- Route /accounting/* to accounting

### Week 3: Production Concepts

**Day 11-12**: Add monitoring
- Prometheus metrics endpoint
- Simple Grafana dashboard
- View request rates

**Day 13-14**: Add tests
- Write pytest unit tests
- Integration tests
- Load test with Locust

**Day 15**: Documentation
- Document your services
- Create API docs (OpenAPI)
- Write README for each service

---

## 🆘 Troubleshooting

### "Cannot allocate memory"
```bash
# Check memory
free -h

# Stop local dev
pkill -f odoo-bin

# Stop unused Docker containers
docker stop $(docker ps -aq)
docker system prune -f
```

### "Port already in use"
```bash
# Find what's using the port
sudo lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### "Docker build fails"
```bash
# Clean Docker cache
docker system prune -a

# Check disk space
df -h

# If low, clean old images
docker image prune -a
```

### "Services can't communicate"
```bash
# Check network
docker network ls
docker network inspect <network-name>

# Check service names in docker-compose
# Services reach each other by service name
# e.g., http://auth-service:8080 (not localhost)
```

---

## 📈 Next Steps

### After Week 1 (Basic Understanding)
- ✅ You understand microservices
- ✅ You can build simple services
- ✅ You can test with Docker Compose
- 👉 **Next**: Add more services (CRM, inventory)

### After Week 2 (Intermediate)
- ✅ Services communicate via HTTP
- ✅ Events flow through RabbitMQ
- ✅ Database per service works
- 👉 **Next**: Add API Gateway (Kong or nginx)

### After Week 3 (Advanced)
- ✅ Complete local microservices stack
- ✅ Monitoring and logging working
- ✅ Tests passing
- 👉 **Next**: Deploy to AWS EKS (Phase 9)

---

## 💡 Pro Tips

1. **Start Small**: Don't try to build all 10 services at once. Start with 2-3.

2. **Use Docker Compose**: Much easier than Kubernetes for learning.

3. **Stop Local Dev**: Always stop your local dev Odoo when testing microservices.

4. **Monitor Resources**: Use `docker stats` to see what's using RAM.

5. **Clean Up**: Run `docker system prune` weekly to free disk space.

6. **Test Often**: After each change, test with curl or Postman.

7. **Read Logs**: `docker-compose logs -f` is your friend.

8. **Keep It Simple**: Don't add complexity until you need it.

---

## 🚀 Ready to Start?

Pick your path and follow the step-by-step instructions in the README.md!

**Recommended first command:**
```bash
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-microservices
mkdir -p microservices/auth-service
# Copy the auth service code from README
# Start building!
```

**Questions?** Check:
- Full details: [README.md](README.md)
- Deployment guide: [DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)
- Architecture diagrams: Top of README.md

---

**Good luck! Start small, learn incrementally, and have fun! 🎉**
