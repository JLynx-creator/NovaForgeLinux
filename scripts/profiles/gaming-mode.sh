#!/bin/bash
# ============================================================
# NovaForge Linux — Switch to Gaming Profile
# ============================================================
set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (sudo)."
    exit 1
fi

echo "=== Switching to Gaming Profile ==="

# 1. Set CPU scaling governor to performance
echo "[Profile] Setting CPU governor to performance..."
if ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null 2>&1; then
    for gov in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
        echo "performance" > "$gov" || true
    done
elif command -v cpupower >/dev/null 2>&1; then
    cpupower frequency-set -g performance || true
fi

# 2. Adjust sysctl parameters
echo "[Profile] Adjusting sysctl parameters..."
sysctl -w vm.swappiness=10
sysctl -w vm.vfs_cache_pressure=50

# 3. Disable print manager service to free resources
echo "[Profile] Stopping cups-browsed service..."
systemctl stop cups-browsed || true

# 4. Enable Gamemode service if present
if systemctl list-unit-files | grep -q gamemode; then
    echo "[Profile] Starting gamemode daemon..."
    systemctl start gamemode || true
fi

# 5. Write profile environment file
echo "[Profile] Updating profile environment variables..."
mkdir -p /etc/novaforge
cat > /etc/novaforge/profile-env.sh << EOF
#!/bin/bash
# NovaForge gaming profile environment
export MANGOHUD="1"
export DXVK_ASYNC="1"
EOF
chmod 644 /etc/novaforge/profile-env.sh

# 6. Save active profile state
echo "gaming" > /etc/novaforge/current-profile

echo "=== NovaForge: Gaming Profile Activated ==="
