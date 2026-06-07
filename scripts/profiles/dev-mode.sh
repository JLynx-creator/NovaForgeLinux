#!/bin/bash
# ============================================================
# NovaForge Linux — Switch to Development Profile
# ============================================================
set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (sudo)."
    exit 1
fi

echo "=== Switching to Development Profile ==="

# 1. Set CPU scaling governor to powersave (balanced/efficient)
echo "[Profile] Setting CPU governor to powersave..."
if ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null 2>&1; then
    for gov in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
        echo "powersave" > "$gov" || true
    done
elif command -v cpupower >/dev/null 2>&1; then
    cpupower frequency-set -g powersave || true
fi

# 2. Adjust sysctl parameters
echo "[Profile] Adjusting sysctl parameters..."
sysctl -w vm.swappiness=60
sysctl -w fs.inotify.max_user_watches=524288

# 3. Start development services like Docker if present
if systemctl list-unit-files | grep -q docker; then
    echo "[Profile] Starting docker service..."
    systemctl start docker || true
fi

# 4. Write profile environment file (empty for dev mode env)
echo "[Profile] Updating profile environment variables..."
mkdir -p /etc/novaforge
cat > /etc/novaforge/profile-env.sh << EOF
#!/bin/bash
# NovaForge development profile environment
EOF
chmod 644 /etc/novaforge/profile-env.sh

# 5. Save active profile state
echo "development" > /etc/novaforge/current-profile

echo "=== NovaForge: Development Profile Activated ==="
