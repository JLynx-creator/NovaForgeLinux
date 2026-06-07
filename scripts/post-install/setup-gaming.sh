#!/bin/bash
# ============================================================
# NovaForge Linux — Gaming Optimizations & Setup
# ============================================================
set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${CYAN}=== NovaForge Gaming Optimizations Setup ===${NC}"
echo "This script configures controller support, GameMode permissions, and MangoHUD layouts."

# 1. Install additional gaming packages if not present
echo -e "${CYAN}[Gaming Setup]${NC} Installing game controller utilities and Wine dependencies..."
sudo apt-get update
sudo apt-get install -y \
    steam-devices \
    joystick \
    jstest-gtk \
    gamemode \
    mangohud \
    winetricks

# 2. Configure GameMode permissions
echo -e "${CYAN}[Gaming Setup]${NC} Configuring GameMode group permissions..."
# Add current user to the gamemode user group (if it exists) to allow renicing processes
CURRENT_USER=$(logname || echo $USER)
if getent group gamemode >/dev/null; then
    sudo usermod -aG gamemode "$CURRENT_USER"
fi

# 3. Create default MangoHUD configuration
echo -e "${CYAN}[Gaming Setup]${NC} Creating custom MangoHUD settings overlay..."
MANGOHUD_DIR="$HOME/.config/MangoHud"
mkdir -p "$MANGOHUD_DIR"

cat > "$MANGOHUD_DIR/MangoHud.conf" << 'EOF'
# NovaForge Custom MangoHUD Configuration
legacy_layout=0
horizontal
hud_no_margin

# Performance metrics
cpu_stats
cpu_temp
gpu_stats
gpu_temp
ram
vram
fps
frame_timing=0

# Style/Coloring (NovaForge Cyan/Purple Theme)
text_color=CDD6F4
gpu_color=7C3AED
cpu_color=00E5FF
fps_value_color=A6E3A1

# Control keys
toggle_hud=F12
EOF
chmod 644 "$MANGOHUD_DIR/MangoHud.conf"

# 4. Set up steam optimization (increase file watcher limit for proton)
echo -e "${CYAN}[Gaming Setup]${NC} Setting up steam proton file watcher configurations..."
sudo mkdir -p /etc/sysctl.d
cat << 'EOF' | sudo tee /etc/sysctl.d/80-gaming-proton.conf > /dev/null
# NovaForge Proton file watcher limit tweaks
fs.file-max=524288
EOF
sudo sysctl --system || true

echo ""
echo -e "${GREEN}=== NovaForge: Gaming Optimizations Setup Completed! ===${NC}"
echo -e "You can launch Steam, Lutris or custom games to test."
echo -e "To display performance overlay in Steam games, add this to the game Launch Options:"
echo -e "  ${YELLOW}mangohud %command%${NC}"
echo -e "To run with GameMode performance profiles, use:"
echo -e "  ${YELLOW}gamemoderun %command%${NC}"
echo -e "Combined performance stack:"
echo -e "  ${YELLOW}gamemoderun mangohud %command%${NC}"
echo ""
