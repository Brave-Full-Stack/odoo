# Odoo 19.0 - Local Development Branch

> **Branch**: `Odoo-19.0-local-dev`  
> **Purpose**: Local VM development and testing environment  
> **Database**: PostgreSQL (local, port 5432, database: `odoo19`)  
> **Port**: 8069

This branch contains the local development setup for Odoo 19.0, running directly on the VM without Docker containers.

## Quick Start

### Start Odoo (Recommended)

```bash
./start-odoo.sh
```

This script automatically:
- Checks PostgreSQL is running
- Verifies port 8069 is available
- Connects to existing database `odoo19`
- Starts Odoo in dev mode

### Access Points

- **Backend Dashboard**: http://localhost:8069/web
- **Website Frontend**: http://localhost:8069
- **Database Manager**: http://localhost:8069/web/database/manager

### Default Credentials

- **Username**: admin
- **Password**: admin

## Manual Start

If you prefer to start Odoo manually:

```bash
python3 odoo-bin -d odoo19 --dev=all
```

## Development Features

This local development branch includes:

- ✅ Dev mode enabled (`--dev=all`) for auto-reload
- ✅ All addons from `addons/` directory
- ✅ PostgreSQL v14 local database
- ✅ Data persistence (survives restarts)
- ✅ Full debug capabilities

## Database Information

**Database Name**: `odoo19`  
**Host**: localhost  
**Port**: 5432  
**User**: brave (or your system user)

All your work (modules, data, configurations) is stored in this database and persists across restarts.

## File Locations

- **Filestore**: `~/.local/share/Odoo/filestore/odoo19/`
- **Logs**: Terminal output (or configure in odoo.conf)
- **Addons**: `./addons/` and `./odoo/addons/`

## Branch Strategy

This repository uses a 4-branch workflow:

1. **19.0** - Reference branch (tracks upstream Odoo)
2. **Odoo-19.0-local-dev** - This branch (local VM development)
3. **Odoo-19.0-containerized** - Docker setup (port 8070)
4. **Odoo-19.0-microservices** - Kubernetes production manifests

## Troubleshooting

### Port Already in Use

```bash
sudo netstat -tlnp | grep :8069
# Kill the process if needed
kill -9 <PID>
```

### PostgreSQL Not Running

```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

### Clear Browser Cache

If you see old assets or styles, clear browser cache: `Ctrl+Shift+Del`

## Contributing to This Branch

This branch is for local development and testing. Once features are stable:

1. Test thoroughly in this environment
2. Merge to `Odoo-19.0-containerized` for Docker testing
3. Deploy via `Odoo-19.0-microservices` for production

---

## Original Odoo Documentation

For official Odoo documentation, see [README-ODOO-ORIGINAL.md](README-ODOO-ORIGINAL.md)

- [Official Setup Instructions](https://www.odoo.com/documentation/19.0/administration/install/install.html)
- [Odoo eLearning](https://www.odoo.com/slides)
- [Developer Tutorials](https://www.odoo.com/documentation/19.0/developer/howtos.html)
- [Security Issues](https://www.odoo.com/security-report)
