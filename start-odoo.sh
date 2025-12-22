#!/bin/bash
# Odoo Quick Start Script
# Usage: ./start-odoo.sh [database_name]

set -e

ODOO_DIR="/home/brave/Desktop/FullStack/odoo"
DB_NAME="${1:-odoo19}"

echo "=== Odoo Recovery Script ==="
echo ""

# Check if PostgreSQL is running
echo "1. Checking PostgreSQL status..."
if ! sudo systemctl is-active --quiet postgresql; then
    echo "   PostgreSQL is down. Starting..."
    sudo systemctl start postgresql
    sleep 2
else
    echo "   PostgreSQL is running ✓"
fi

# Check if port 8069 is already in use
echo ""
echo "2. Checking if Odoo is already running..."
if sudo lsof -i :8069 -t > /dev/null 2>&1; then
    echo "   Port 8069 is already in use!"
    echo "   Existing process:"
    sudo lsof -i :8069
    read -p "   Kill existing process? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo kill -9 $(sudo lsof -i :8069 -t)
        echo "   Process killed ✓"
        sleep 1
    else
        echo "   Exiting..."
        exit 1
    fi
else
    echo "   Port 8069 is available ✓"
fi

# Navigate to Odoo directory
echo ""
echo "3. Navigating to Odoo directory..."
cd "$ODOO_DIR" || exit 1
echo "   Current directory: $(pwd)"
echo "   Current branch: $(git branch --show-current)"

# Check Python version
echo ""
echo "4. Checking Python version..."
python3 --version

# Check database exists
echo ""
echo "5. Checking database '$DB_NAME'..."
if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "   Database '$DB_NAME' exists ✓"
else
    echo "   WARNING: Database '$DB_NAME' not found!"
    read -p "   Create database? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        createdb -E UTF8 -l en_US.UTF-8 -T template0 "$DB_NAME"
        echo "   Database created ✓"
        echo "   Initializing base module..."
        ./odoo-bin -d "$DB_NAME" -i base --stop-after-init
    else
        echo "   Exiting..."
        exit 1
    fi
fi

# Start Odoo
echo ""
echo "6. Starting Odoo..."
echo "   Database: $DB_NAME"
echo "   URL: http://localhost:8069"
echo "   Press CTRL+C to stop"
echo ""
echo "=== Starting Odoo in Dev Mode ==="
echo ""

./odoo-bin -d "$DB_NAME" --dev=all
