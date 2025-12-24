#!/bin/bash
# VM Performance Optimization Script

echo "======================================"
echo "VM Performance Optimization"
echo "======================================"
echo ""

# 1. Show current memory usage
echo "1. Current Memory Status:"
free -h
echo ""

# 2. Clear system caches (requires sudo)
echo "2. Clearing system caches..."
sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
echo "✓ Caches cleared"
echo ""

# 3. Show top memory consumers
echo "3. Top 10 Memory Consumers:"
ps aux --sort=-%mem | head -11
echo ""

# 4. Stop unnecessary services
echo "4. Stopping unnecessary services..."

# Stop pgAdmin if running
if pgrep -x "pgadmin4" > /dev/null; then
    echo "Stopping pgAdmin4..."
    pkill -f pgadmin4
    echo "✓ pgAdmin stopped"
fi

# 5. Docker cleanup if Docker is installed
if command -v docker &> /dev/null; then
    echo "5. Cleaning Docker resources..."
    docker system prune -af --volumes > /dev/null 2>&1
    echo "✓ Docker cleaned"
fi

# 6. Clean package manager cache
echo "6. Cleaning package caches..."
sudo apt-get clean > /dev/null 2>&1
sudo apt-get autoclean > /dev/null 2>&1
echo "✓ Package caches cleaned"
echo ""

# 7. Show final memory status
echo "7. Final Memory Status:"
free -h
echo ""

echo "======================================"
echo "✅ Optimization Complete!"
echo "======================================"
echo ""
echo "Additional Recommendations:"
echo "- Close Firefox tabs you're not using"
echo "- Restart VS Code to free fragmented memory"
echo "- Consider increasing VM RAM to 8GB+"
echo "- Use lighter alternatives (nano/vim instead of VS Code)"
