# Odoo 19.0 - Containerized Setup

This branch contains the Docker containerized setup for Odoo 19.0 with PostgreSQL and pgAdmin4.

## 🐳 Architecture

- **Odoo 19.0**: Custom built from source (Port 8070)
- **PostgreSQL 16**: Alpine-based database (Port 5433)
- **pgAdmin4**: Database management interface (Port 5050)

## 🐋 Docker Image

### Pre-built Image on Docker Hub

**Image:** `bravejongen/odoo:19.0` or `bravejongen/odoo:latest`

This image is built from the **Odoo-19.0-containerized** branch and includes:
- ✅ Odoo 19.0 source code from official repository
- ✅ Pre-configured for Docker container environments
- ✅ Database manager enabled (`list_db = True`)
- ✅ Container network ready (`db_host = postgres`)
- ✅ Admin password pre-set for quick setup
- ✅ All Python dependencies installed
- ✅ wkhtmltopdf for PDF reports
- ✅ Production-ready with proper health checks

**Image Size:** 2.26 GB  
**Base Image:** python:3.12-slim-bookworm  
**Exposed Ports:** 8069 (Odoo), 8071 (Live Chat), 8072 (Longpolling)

### Pull and Run

```bash
# Pull from Docker Hub
docker pull bravejongen/odoo:19.0

# Run standalone (requires PostgreSQL)
docker run -d \
  --name odoo \
  -p 8069:8069 \
  -e HOST=postgres \
  -e USER=odoo \
  -e PASSWORD=odoo \
  bravejongen/odoo:19.0

# Or use docker-compose (recommended)
docker-compose up -d
```

### Image vs Branch Comparison

| Aspect | Main (19.0) Branch | This Image (Containerized) |
|--------|-------------------|---------------------------|
| Odoo Code | ✅ Same 19.0 source | ✅ Same 19.0 source |
| Configuration | Local/default | Docker-optimized |
| Database Host | localhost/IP | `postgres` (container) |
| Admin Password | Not set | Pre-set to `admin` |
| Database Manager | Disabled | Enabled |
| Environment | VM/bare metal | Container-ready |
| Port Mapping | Direct 8069 | 8069 (mapped to 8070 in compose) |

## 📋 Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)
- 4GB+ RAM available
- 10GB+ free disk space

## 🚀 Quick Start

### 1. Start All Services

```bash
docker-compose up -d
```

### 2. Verify Services

```bash
docker-compose ps
```

All services should show `Up (healthy)` status.

### 3. Access Applications

- **Odoo**: http://localhost:8070
- **pgAdmin4**: http://localhost:5050
- **Database Manager**: http://localhost:8070/web/database/manager

## 🔐 Credentials

### Odoo Database Manager
- **Master Password**: `admin`

### PostgreSQL
- **Host**: `postgres` (container name) or `localhost:5433` (from host)
- **Database**: `postgres`
- **Username**: `odoo`
- **Password**: `odoo`

### pgAdmin4
- **Email**: `admin@admin.com`
- **Password**: `admin`
- **Master Password**: Set on first login (your choice)

#### Connecting to PostgreSQL in pgAdmin
1. Set pgAdmin master password on first login
2. Add New Server:
   - **Name**: Odoo PostgreSQL
   - **Host**: `postgres`
   - **Port**: `5432`
   - **Username**: `odoo`
   - **Password**: `odoo`
   - **Database**: `postgres`

## 📁 Volume Persistence

Data is persisted in Docker volumes:

```bash
# List volumes
docker volume ls | grep odoo

# Inspect volume
docker volume inspect odoo_odoo-db-data
docker volume inspect odoo_odoo-web-data
```

**Volumes:**
- `odoo-db-data`: PostgreSQL database files
- `odoo-web-data`: Odoo data directory
- `odoo-logs`: Odoo log files
- `pgadmin-data`: pgAdmin configuration

## 🛠️ Troubleshooting & Management

### View Logs

```bash
# Real-time logs (all services)
docker-compose logs -f

# Specific service
docker-compose logs -f odoo
docker-compose logs -f postgres
docker-compose logs -f pgadmin

# Last N lines
docker-compose logs --tail=50 odoo
```

### Access Container Shell

```bash
# Odoo container
docker exec -it odoo-app bash

# PostgreSQL container
docker exec -it odoo-postgres bash

# pgAdmin container
docker exec -it odoo-pgadmin sh
```

### Database Access

```bash
# PostgreSQL shell
docker exec -it odoo-postgres psql -U odoo -d postgres

# Common psql commands:
# \l              - List all databases
# \c dbname       - Connect to database
# \dt             - List tables
# \du             - List users
# \q              - Quit
```

### Restart Services

```bash
# Restart single service
docker-compose restart odoo

# Restart all services
docker-compose restart

# Stop and start (clean restart)
docker-compose down && docker-compose up -d
```

### Check Resource Usage

```bash
# Real-time stats
docker stats

# One-time snapshot
docker stats --no-stream
```

### Inspect Container Details

```bash
# View configuration
docker inspect odoo-app

# Check health status
docker inspect odoo-app --format='{{.State.Health.Status}}'

# View environment variables
docker exec odoo-app env
```

### Configuration Changes

#### Method 1: Edit and Rebuild (Persistent)

```bash
# 1. Edit configuration file
nano docker/odoo.conf

# 2. Rebuild and restart
docker-compose up -d --build odoo
```

#### Method 2: Live Changes (Testing Only - Lost on Restart)

```bash
# Edit inside container
docker exec -it odoo-app bash
nano /etc/odoo/odoo.conf
exit

# Restart to apply
docker-compose restart odoo
```

### Network Debugging

```bash
# Test connectivity between containers
docker exec odoo-app ping postgres

# Check network details
docker network inspect odoo_odoo-network

# Test Odoo from inside container
docker exec odoo-app curl http://localhost:8069
```

## 💾 Backup & Restore

### Backup Database

```bash
# Using docker exec
docker exec odoo-postgres pg_dump -U odoo -d odoo_test > backup_$(date +%Y%m%d).sql

# Using docker run
docker run --rm -v odoo_odoo-db-data:/data -v $(pwd):/backup alpine tar czf /backup/db-backup.tar.gz /data
```

### Restore Database

```bash
# Create database first
docker exec odoo-postgres psql -U odoo -c "CREATE DATABASE odoo_restored;"

# Restore from backup
docker exec -i odoo-postgres psql -U odoo -d odoo_restored < backup_20241224.sql
```

### Backup All Volumes

```bash
# Backup all volumes
docker run --rm \
  -v odoo_odoo-web-data:/web-data \
  -v odoo_odoo-db-data:/db-data \
  -v odoo_odoo-logs:/logs \
  -v $(pwd):/backup \
  alpine tar czf /backup/odoo-full-backup-$(date +%Y%m%d).tar.gz /web-data /db-data /logs
```

## 🧹 Cleanup

### Stop Services

```bash
# Stop but keep data
docker-compose down

# Stop and remove volumes (⚠️ DELETES ALL DATA)
docker-compose down -v
```

### Remove Old Images

```bash
# Remove unused images
docker image prune -a

# Remove specific image
docker rmi odoo_odoo
```

## 🔧 Configuration Files

### Key Files

- `docker-compose.yml`: Service orchestration
- `Dockerfile`: Odoo image build instructions
- `docker/odoo.conf`: Odoo configuration
- `.dockerignore`: Files excluded from image build

### Important Configuration Settings

**docker/odoo.conf:**
```ini
# Database
db_host = postgres
db_port = 5432
db_user = odoo
db_password = odoo

# Security
admin_passwd = admin
list_db = True
db_filter = .*

# Performance
workers = 4
max_cron_threads = 2
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
```

## 🐛 Common Issues

### Port Already in Use

```bash
# Check what's using the port
sudo netstat -tulpn | grep 8070

# Kill the process
sudo kill <PID>

# Or change port in docker-compose.yml
ports:
  - "8080:8069"  # Use 8080 instead
```

### Container Won't Start

```bash
# Check logs
docker-compose logs odoo

# Remove and recreate
docker-compose down
docker-compose up -d --force-recreate odoo
```

### Database Connection Failed

```bash
# Ensure postgres is healthy
docker-compose ps postgres

# Test connection
docker exec odoo-app pg_isready -h postgres -U odoo

# Restart postgres
docker-compose restart postgres
```

### Out of Memory

```bash
# Check memory usage
docker stats

# Reduce workers in docker/odoo.conf
workers = 2  # Instead of 4

# Rebuild
docker-compose up -d --build odoo
```

## 📊 Monitoring

### Health Checks

```bash
# Built-in health checks
docker-compose ps

# Manual health check
curl -f http://localhost:8070/web/health
```

### Log Rotation

Logs are stored in volume `odoo-logs`:

```bash
# View log size
docker exec odoo-app du -sh /var/log/odoo/

# View recent logs
docker exec odoo-app tail -100 /var/log/odoo/odoo.log
```

## 🔄 Updates

### Update Odoo Code

```bash
# Pull latest changes
git pull origin Odoo-19.0-containerized

# Rebuild image
docker-compose build odoo

# Restart with new image
docker-compose up -d odoo
```

### Update Base Image

```bash
# Pull latest Python base image
docker pull python:3.12-slim-bookworm

# Rebuild
docker-compose build --no-cache odoo
docker-compose up -d odoo
```

## 📝 Development Workflow

1. **Make Changes**: Edit code or configuration
2. **Rebuild**: `docker-compose up -d --build odoo`
3. **Test**: Verify changes work correctly
4. **Check Logs**: `docker-compose logs -f odoo`
5. **Commit**: `git add . && git commit -m "Description"`

## 🆚 Branch Comparison

- **19.0**: Original Odoo source code (reference)
- **Odoo-19.0-local-tested**: Local VM installation (port 8069)
- **Odoo-19.0-containerized**: Docker setup (this branch, port 8070)
- **Odoo-19.0-microservices**: Kubernetes manifests for production

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Odoo Documentation](https://www.odoo.com/documentation/19.0/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)
- [pgAdmin Docker Hub](https://hub.docker.com/r/dpage/pgadmin4)

## 🤝 Contributing

1. Create feature branch from `Odoo-19.0-containerized`
2. Make changes and test thoroughly
3. Commit with clear messages
4. Create pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

---

**Note**: This is a containerized development/testing environment. For production deployment, see the `Odoo-19.0-microservices` branch with Kubernetes configurations.
