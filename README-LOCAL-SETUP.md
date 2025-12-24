# Odoo 19.0 - Local Development Setup

This branch contains a tested local Odoo 19.0 installation optimized for development VMs and manual deployments.

## 🎯 Purpose

**Use this branch for:**
- Local development on VMs
- Manual Odoo installations
- Quick testing and prototyping
- Learning and experimentation
- VM crash recovery

**Do NOT use for:**
- Production deployments → Use containerized or microservices branches
- Multi-instance setups → Use Docker or Kubernetes branches
- CI/CD automation → Use microservices branch

---

## 📋 Prerequisites

### System Requirements
- Ubuntu 22.04 LTS or later
- 8 GB RAM minimum (16 GB recommended)
- 50 GB free disk space
- Python 3.10+
- PostgreSQL 14+

### Required Packages
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev \
  postgresql postgresql-client \
  build-essential libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
  libjpeg-dev libpq-dev libffi-dev libssl-dev zlib1g-dev \
  git curl wget nodejs npm
```

---

## 🚀 Quick Start

### 1. Clone This Branch
```bash
git clone git@github.com:Brave-Full-Stack/odoo.git -b Odoo-19.0-local-tested
cd odoo
```

### 2. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Setup PostgreSQL
```bash
# Create PostgreSQL user
sudo -u postgres createuser -s $USER

# Create database (optional, script can do this)
createdb -E UTF8 -l en_US.UTF-8 -T template0 odoo19
```

### 4. Start Odoo
```bash
./start-odoo.sh odoo19
```

That's it! Odoo will be available at http://localhost:8069

---

## 📜 Using start-odoo.sh

### Basic Usage
```bash
./start-odoo.sh [database_name]
```

### Examples

**First time setup:**
```bash
./start-odoo.sh my_dev_db
```

**Daily development:**
```bash
./start-odoo.sh
```

**After VM crash:**
```bash
./start-odoo.sh odoo19
```

**Multiple databases:**
```bash
./start-odoo.sh customer_test
./start-odoo.sh feature_dev
./start-odoo.sh staging_db
```

### What the Script Does

1. ✅ Checks if PostgreSQL is running (starts if needed)
2. ✅ Detects port 8069 conflicts (offers to kill blocking process)
3. ✅ Navigates to Odoo directory
4. ✅ Verifies Python version
5. ✅ Checks if database exists (creates if missing)
6. ✅ Starts Odoo in development mode (`--dev=all`)

### Features

- **Auto-reload:** Code changes reload automatically
- **No cache:** Always uses latest code
- **Database creation:** Creates DB if missing
- **Conflict resolution:** Handles port 8069 conflicts
- **Interactive:** Prompts for confirmation

---

## 🔧 Development Workflow

### Typical Day

```bash
# Morning - Start development
cd ~/Desktop/FullStack/odoo
git pull origin Odoo-19.0-local-tested
./start-odoo.sh my_dev_db

# During development
# - Edit files in addons/
# - Changes auto-reload
# - Test at http://localhost:8069

# End of day - Commit changes
git add .
git commit -m "Your changes"
git push origin Odoo-19.0-local-tested
```

### Working with Custom Addons

```bash
# Add your custom addon
mkdir -p addons/my_custom_addon
cd addons/my_custom_addon
# Create __manifest__.py, models/, views/, etc.

# Restart Odoo to see new addon
# CTRL+C to stop, then:
./start-odoo.sh my_dev_db
```

### Database Management

```bash
# List databases
psql -l

# Backup database
pg_dump odoo19 > backup.sql

# Restore database
psql odoo19 < backup.sql

# Drop database
dropdb odoo19

# Create fresh database
createdb -E UTF8 -l en_US.UTF-8 -T template0 odoo19
./start-odoo.sh odoo19  # Will initialize base module
```

---

## 🐛 Troubleshooting

### Port 8069 Already in Use

The script will detect this and offer to kill the process:
```bash
./start-odoo.sh
# Follow prompts to kill blocking process
```

Manual alternative:
```bash
# Find process
sudo lsof -i :8069

# Kill process
sudo kill -9 <PID>
```

### PostgreSQL Not Starting

```bash
# Check status
sudo systemctl status postgresql

# Start service
sudo systemctl start postgresql

# Enable on boot
sudo systemctl enable postgresql
```

### Python Dependencies Missing

```bash
# Reinstall all dependencies
pip3 install -r requirements.txt --force-reinstall
```

### Database Connection Failed

```bash
# Check PostgreSQL user
sudo -u postgres psql -c "\du"

# Create user if missing
sudo -u postgres createuser -s $USER

# Grant permissions
sudo -u postgres psql -c "ALTER USER $USER WITH PASSWORD 'yourpassword';"
```

### Odoo Won't Start

```bash
# Check logs
tail -f /var/log/postgresql/postgresql-*.log

# Test database connection
psql -U $USER -d postgres -c "SELECT version();"

# Verify Python version
python3 --version  # Should be 3.10+

# Check dependencies
pip3 list | grep -E "psycopg2|werkzeug|babel"
```

---

## 📊 Useful Commands

### Odoo Management

```bash
# Start with specific database
./odoo-bin -d mydb

# Update module
./odoo-bin -d mydb -u module_name --stop-after-init

# Install module
./odoo-bin -d mydb -i module_name --stop-after-init

# Run tests
./odoo-bin -d test_db --test-enable --stop-after-init

# Shell mode
./odoo-bin shell -d mydb
```

### Git Operations

```bash
# Check current branch
git branch --show-current

# Switch branches
git checkout 19.0  # Official Odoo
git checkout Odoo-19.0-containerized  # Docker version
git checkout Odoo-19.0-microservices  # K8s version

# Pull updates
git pull origin Odoo-19.0-local-tested

# Push changes
git push origin Odoo-19.0-local-tested
```

---

## 🌿 Branch Overview

| Branch | Purpose | Use Case |
|--------|---------|----------|
| **19.0** | Official Odoo | Base/reference |
| **Odoo-19.0-local-tested** | Manual install | **This branch** - Local dev |
| **Odoo-19.0-containerized** | Docker setup | Testing, staging |
| **Odoo-19.0-microservices** | K8s/CI/CD | Production, cloud |

---

## 📝 Notes

- This branch uses **direct Python execution** (no containers)
- Development mode enables **auto-reload** on file changes
- PostgreSQL runs as **local service** (not containerized)
- Port 8069 is used for **single instance** only
- Perfect for **rapid development** and **learning**

---

## 🚀 Team Onboarding

New team member? Here's what you need:

1. **Clone this branch:**
   ```bash
   git clone git@github.com:Brave-Full-Stack/odoo.git -b Odoo-19.0-local-tested
   cd odoo
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start Odoo:**
   ```bash
   ./start-odoo.sh my_dev_db
   ```

4. **Access Odoo:**
   - URL: http://localhost:8069
   - Create admin account on first access

That's it! 🎉

---

## 📧 Support

- Documentation: See this README
- Issues: Create GitHub issue
- Questions: Contact team lead

**Happy coding!** 💻
