# 🔐 ODOO CREDENTIALS - PRIVATE
**⚠️ DO NOT COMMIT THIS FILE TO EXTERNAL REPOSITORIES ⚠️**

This file is tracked in the local branch only and excluded from external commits via `.gitignore`.

---

## 📋 Local Development Setup

### PostgreSQL (Port 5432)
- **Host:** `localhost` / `127.0.0.1`
- **Port:** `5432`
- **Database:** `odoo19`

#### User Accounts:
1. **System User:**
   - Username: `brave`
   - Password: `brave123`
   - Access: Owner of `odoo19` database

2. **Superuser:**
   - Username: `postgres`
   - Password: `postgres`
   - Access: Full PostgreSQL admin rights

### Odoo Application
- **URL:** http://localhost:8069
- **Admin Password:** (Set during Odoo first-time setup)
- **Process:** Python3 direct execution
- **Config File:** `/path/to/odoo.conf`

### pgAdmin4 (Desktop Application)
- **Application:** `pgadmin4` (installed locally)
- **Connection:** Use PostgreSQL credentials above

---

## 🐳 Docker Containerized Setup

### PostgreSQL Container (Port 5433)
- **Host (from host machine):** `localhost`
- **Host (from containers):** `postgres`
- **Port (external):** `5433`
- **Port (internal):** `5432`
- **Container:** `odoo-postgres`
- **Database:** `postgres`
- **Username:** `odoo`
- **Password:** `odoo`

### Odoo Container
- **URL:** http://localhost:8070
- **Port Mapping:**
  - Web: `8070:8069`
  - Long Polling: `8073:8071`
  - Additional: `8074:8072`
- **Container:** `odoo-app`
- **Admin Password:** `admin` (set via ODOO_ADMIN_PASSWORD env var)
- **Database Connection:**
  - Host: `postgres`
  - User: `odoo`
  - Password: `odoo`

### pgAdmin4 Container
- **URL:** http://localhost:5050
- **Container:** `odoo-pgadmin`
- **Login:**
  - Email: `admin@admin.com`
  - Password: `admin`

**To connect pgAdmin4 to containerized PostgreSQL:**
- Host: `postgres` (or `odoo-postgres`)
- Port: `5432`
- Username: `odoo`
- Password: `odoo`
- Database: `postgres`

---

## 🚀 Quick Start Commands

### Local Development
```bash
# Start PostgreSQL (if not running)
sudo systemctl start postgresql

# Start Odoo
python3 odoo-bin -c odoo.conf

# Launch pgAdmin4
pgadmin4
```

### Docker Containers
```bash
# Start all containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all containers
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 📝 Notes
- Local and containerized setups can run **simultaneously**
- Local setup uses ports: 8069, 5432
- Container setup uses ports: 8070, 8073, 8074, 5433, 5050
- All Docker data is stored in named volumes (persistent)
- Bind mount: `./addons` → `/opt/odoo/addons` (shared with container)

---

**Last Updated:** 24 December 2025
