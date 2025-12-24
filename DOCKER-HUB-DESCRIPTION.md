# Odoo 19.0 - Containerized

Production-ready Docker image for Odoo 19.0 ERP system, built from source with Docker-optimized configurations.

## 🚀 Quick Start

```bash
# Using docker-compose (recommended)
curl -O https://raw.githubusercontent.com/Brave-Full-Stack/odoo/Odoo-19.0-containerized/docker-compose.yml
docker-compose up -d

# Or run standalone
docker run -d \
  --name odoo \
  -p 8069:8069 \
  -e HOST=postgres \
  -e USER=odoo \
  -e PASSWORD=odoo \
  bravejongen/odoo:19.0
```

## 📦 What's Inside

- **Odoo 19.0** - Built from official odoo/odoo repository
- **Python 3.12** - Latest stable Python on Debian Bookworm
- **wkhtmltopdf 0.12.6** - For PDF report generation
- **PostgreSQL Client** - Database connectivity
- **All Dependencies** - Fully configured and ready to run

## 🔧 Configuration

### Pre-configured Settings
- Database manager enabled
- Admin master password: `admin` (change in production!)
- Container-ready database connection
- Health checks enabled
- Multi-worker support (4 workers)
- Optimized memory limits

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `postgres` | PostgreSQL hostname |
| `USER` | `odoo` | Database username |
| `PASSWORD` | `odoo` | Database password |
| `ODOO_ADMIN_PASSWORD` | `admin` | Master password |

## 🐳 Ports

| Port | Service |
|------|---------|
| 8069 | Odoo Web Interface |
| 8071 | Live Chat/Gevent |
| 8072 | Longpolling |

## 💾 Volumes

Mount these volumes for data persistence:

```yaml
volumes:
  - odoo-web-data:/var/lib/odoo
  - odoo-logs:/var/log/odoo
  - ./addons:/opt/odoo/addons  # Custom addons (optional)
```

## 🔗 Full Stack Setup

Complete setup with PostgreSQL and pgAdmin:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
    
  odoo:
    image: bravejongen/odoo:19.0
    depends_on:
      - postgres
    ports:
      - "8069:8069"
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-data:/var/lib/odoo

volumes:
  db-data:
  odoo-data:
```

## 🏥 Health Checks

Built-in health check endpoint:
```bash
curl http://localhost:8069/web/health
```

Container health status:
```bash
docker inspect --format='{{.State.Health.Status}}' odoo
```

## 📚 Documentation

- **GitHub Repository**: https://github.com/Brave-Full-Stack/odoo/tree/Odoo-19.0-containerized
- **Full README**: https://github.com/Brave-Full-Stack/odoo/blob/Odoo-19.0-containerized/README.md
- **Odoo Documentation**: https://www.odoo.com/documentation/19.0/

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **Change default passwords**:
   ```yaml
   environment:
     - ODOO_ADMIN_PASSWORD=your-secure-password
     - PASSWORD=your-db-password
   ```

2. **Disable database manager**:
   - Mount custom `odoo.conf` with `list_db = False`

3. **Use secrets** for sensitive data:
   ```yaml
   secrets:
     - db_password
     - admin_password
   ```

4. **Enable HTTPS** with reverse proxy (nginx/traefik)

## 🆚 Image Variants

- `bravejongen/odoo:19.0` - Version-tagged image (recommended)
- `bravejongen/odoo:latest` - Latest build

## 🛠️ Build Information

- **Built from**: Odoo-19.0-containerized branch
- **Base Image**: python:3.12-slim-bookworm
- **Size**: 2.26 GB
- **Architecture**: linux/amd64
- **Source**: https://github.com/odoo/odoo (19.0 branch)

## 📈 Performance

### Resource Requirements

| Environment | CPU | Memory | Disk |
|-------------|-----|--------|------|
| Development | 2 cores | 2 GB | 10 GB |
| Production | 4+ cores | 4+ GB | 20+ GB |

### Optimization Tips

1. **Workers**: Set based on CPU cores
   - Formula: (CPU cores * 2) + 1

2. **Memory Limits**: Configure per worker
   ```
   limit_memory_soft = 2147483648  # 2GB
   limit_memory_hard = 2684354560  # 2.5GB
   ```

3. **Database Connection Pool**:
   ```
   db_maxconn = 64
   ```

## 🐛 Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker exec odoo pg_isready -h postgres -U odoo
```

### Container Won't Start
```bash
# Check logs
docker-compose logs odoo

# Restart with fresh state
docker-compose down -v
docker-compose up -d
```

### Permission Issues
```bash
# Fix volume permissions
docker exec odoo chown -R odoo:odoo /var/lib/odoo
```

## 📝 Usage Examples

### Create Database via CLI
```bash
docker exec -it odoo odoo-bin -d mydb -i base --stop-after-init
```

### Install Modules
```bash
docker exec -it odoo odoo-bin -d mydb -i sale,purchase,crm --stop-after-init
```

### Update Modules
```bash
docker exec -it odoo odoo-bin -d mydb -u all --stop-after-init
```

### Shell Access
```bash
docker exec -it odoo bash
```

## 🤝 Contributing

Issues and pull requests welcome at: https://github.com/Brave-Full-Stack/odoo

## 📄 License

This Docker image contains Odoo, which is licensed under LGPL v3.  
See: https://github.com/odoo/odoo/blob/19.0/LICENSE

---

**Maintained by**: Brave Full Stack  
**Last Updated**: December 2025  
**Odoo Version**: 19.0
