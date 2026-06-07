#!/bin/bash
# ============================================================
# NovaForge Linux — Switch to AI Profile
# ============================================================
set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (sudo)."
    exit 1
fi

echo "=== Switching to AI Profile ==="

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
sysctl -w vm.overcommit_memory=1

# 3. Disable print manager service to free resources
echo "[Profile] Stopping cups-browsed service..."
systemctl stop cups-browsed || true

# 4. Write profile environment file with AI specific variables
echo "[Profile] Updating profile environment variables..."
mkdir -p /etc/novaforge
cat > /etc/novaforge/profile-env.sh << EOF
#!/bin/bash
# NovaForge AI profile environment
export CUDA_VISIBLE_DEVICES="all"
EOF
chmod 644 /etc/novaforge/profile-env.sh

# 5. Save active profile state
echo "ai" > /etc/novaforge/current-profile

echo "=== NovaForge: AI Profile Activated ==="
