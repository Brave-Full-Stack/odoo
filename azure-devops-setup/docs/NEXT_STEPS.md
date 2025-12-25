# 🎯 Your Next Steps - Start in 5 Minutes!

**Your VM**: 8.5 GB RAM, 8 cores - Perfect for learning!  
**Current**: Running Odoo local-dev (~5.4 GB RAM)  
**Goal**: Learn microservices without breaking your setup

---

## 🚀 Quickest Start (Copy-Paste These Commands)

### Step 1: Prepare (2 minutes)
```bash
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-microservices
mkdir -p microservices/auth-service
cd microservices/auth-service
```

### Step 2: Create Auth Service (3 minutes)
```bash
# Create main.py (copy from README.md section "Step 2.1")
# Or download it:
cat > main.py << 'PYTHON_EOF'
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

app = FastAPI(title="Odoo Auth Service", version="1.0.0")

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "admin": {
        "username": "admin",
        "email": "admin@odoo.local",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
PYTHON_EOF

# Create requirements
cat > requirements.txt << 'REQ_EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
REQ_EOF

# Create Dockerfile
cat > Dockerfile << 'DOCKER_EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
DOCKER_EOF
```

### Step 3: Test Locally with Python (5 minutes)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run service
python main.py &
SERVICE_PID=$!

# Wait for it to start
sleep 3

# Test it
curl http://localhost:8080/health
# Should see: {"status":"healthy","service":"auth-service","version":"1.0.0"}

# Test login
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
# Should see: {"access_token":"eyJ...","token_type":"bearer"}

# Stop service
kill $SERVICE_PID
deactivate
```

### Step 4: Test with Docker (Optional - 5 minutes)
```bash
cd /home/brave/Desktop/FullStack/odoo

# Create docker-compose file
cat > docker-compose.microservices.yml << 'COMPOSE_EOF'
version: '3.8'

services:
  auth-service:
    build:
      context: ./microservices/auth-service
    ports:
      - "8080:8080"
    environment:
      - JWT_SECRET_KEY=dev-secret-key
    networks:
      - odoo-network

networks:
  odoo-network:
    driver: bridge
COMPOSE_EOF

# Build and run
docker-compose -f docker-compose.microservices.yml up -d

# Test
curl http://localhost:8080/health

# Check resource usage
docker stats --no-stream

# Clean up
docker-compose -f docker-compose.microservices.yml down
```

---

## ✅ What You've Accomplished

After following the steps above:
- ✅ Created your first microservice (auth-service)
- ✅ Tested it locally with Python
- ✅ Containerized it with Docker
- ✅ Verified it uses only ~200 MB RAM
- ✅ Ready to build more services!

---

## 📚 What to Read Next

### For Understanding
1. **[RESOURCE_PLANNING.md](RESOURCE_PLANNING.md)** - Understand your VM capacity
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Detailed learning paths

### For Implementation  
3. **[README.md](README.md)** - Complete service examples
4. **[DEPLOYMENT_PLAN.md](DEPLOYMENT_PLAN.md)** - Full production guide

---

## 🎓 Your Learning Path

```
Week 1: Build Basics
├─ Day 1: ✅ Auth service (you just did this!)
├─ Day 2: Build accounting service
├─ Day 3: Test both services together
├─ Day 4: Add database (PostgreSQL)
└─ Day 5: Add inter-service communication

Week 2: Add Complexity
├─ Day 6: Add RabbitMQ for events
├─ Day 7: Add Redis for caching
├─ Day 8: Add API Gateway (nginx)
├─ Day 9: Add monitoring (Prometheus)
└─ Day 10: Load testing

Week 3: Advanced Topics
├─ Day 11: Write tests (pytest)
├─ Day 12: Add CI/CD (GitHub Actions)
├─ Day 13: Security hardening
├─ Day 14: Documentation
└─ Day 15: Review and consolidate

Week 4: Production (Optional)
├─ Deploy to AWS EKS
├─ Set up monitoring
├─ Configure autoscaling
└─ Go live!
```

---

## 💡 Pro Tips

1. **Don't Rush**: Build one service at a time
2. **Test Often**: After each change, test with curl
3. **Read Logs**: They tell you what's wrong
4. **Save Your Work**: Commit to git regularly
5. **Ask Questions**: Check documentation when stuck

---

## 🆘 Quick Help

### Service won't start?
```bash
# Check if port is in use
sudo lsof -i :8080

# Check logs
docker-compose logs auth-service
```

### Out of memory?
```bash
# Check usage
free -h

# Stop local dev first
pkill -f odoo-bin

# Clean Docker
docker system prune -f
```

### Can't access service?
```bash
# Check if running
docker ps

# Check container logs
docker logs <container-id>

# Test from inside container
docker exec -it <container-id> curl localhost:8080/health
```

---

## 🎯 Your First Goal

**By the end of today:**
- ✅ Auth service running
- ✅ Can login and get JWT token
- ✅ Understand how it works

**Tomorrow:**
- Build accounting service
- Connect it to auth service
- Test the flow

**This week:**
- 3-4 services running
- Basic inter-service communication
- Comfortable with Docker Compose

---

## 🚀 Ready? Run These Commands Now!

```bash
cd /home/brave/Desktop/FullStack/odoo
git checkout Odoo-19.0-microservices

# Follow Step 1-3 above
# Total time: 15 minutes
# You'll have your first microservice running!
```

**Questions?** 
- Check README.md for detailed examples
- Read GETTING_STARTED.md for learning paths
- Review RESOURCE_PLANNING.md for VM optimization

**Good luck! You've got this! 🎉**
