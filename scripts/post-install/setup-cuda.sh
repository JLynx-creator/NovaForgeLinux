#!/bin/bash
# ============================================================
# NovaForge Linux — NVIDIA CUDA & GPU Acceleration Installer
# ============================================================
set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}=== NovaForge NVIDIA CUDA & GPU Acceleration Setup ===${NC}"
echo "This script installs CUDA Toolkit and configures Docker for GPU workloads."

# 1. Detect if NVIDIA GPU is present
if ! lspci | grep -qi nvidia; then
    echo -e "${RED}[CUDA Setup]${NC} No NVIDIA GPU detected on this system via lspci."
    echo -e "${RED}[CUDA Setup]${NC} This script is designed for NVIDIA GPUs only."
    read -p "Do you want to force install CUDA anyway? (y/N): " FORCE_INSTALL
    if [[ ! "$FORCE_INSTALL" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 2. Add NVIDIA CUDA repositories for Ubuntu 24.04 (Noble)
echo -e "${CYAN}[CUDA Setup]${NC} Setting up NVIDIA repository keys..."
distro="ubuntu2404"
arch="x86_64"

# Download keyring
wget https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-keyring_1.1-1_all.deb -O /tmp/cuda-keyring.deb
sudo dpkg -i /tmp/cuda-keyring.deb
rm /tmp/cuda-keyring.deb

sudo apt-get update

# 3. Install CUDA Toolkit and Drivers
echo -e "${CYAN}[CUDA Setup]${NC} Installing CUDA Toolkit and drivers..."
sudo apt-get install -y cuda-toolkit-12-4 nvidia-driver-550-server || sudo apt-get install -y cuda-toolkit

# 4. Configure environment variables (add to global profile or users profile)
echo -e "${CYAN}[CUDA Setup]${NC} Setting up global path environment variables..."
cat << 'EOF' | sudo tee /etc/profile.d/cuda.sh > /dev/null
# NVIDIA CUDA environment setup
export PATH=/usr/local/cuda-12.4/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
EOF
sudo chmod 644 /etc/profile.d/cuda.sh

# 5. Install NVIDIA Container Toolkit for Docker
echo -e "${CYAN}[CUDA Setup]${NC} Installing NVIDIA Container Toolkit for Docker GPU access..."
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list > /dev/null

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
echo -e "${CYAN}[CUDA Setup]${NC} Configuring Docker runtime for NVIDIA GPUs..."
sudo nvidia-container-toolkit-cdi generate --output=/etc/cdi/nvidia.yaml || true
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker daemon to apply runtime changes
if systemctl is-active --quiet docker; then
    echo -e "${CYAN}[CUDA Setup]${NC} Restarting Docker service..."
    sudo systemctl restart docker
fi

echo ""
echo -e "${GREEN}=== NovaForge: NVIDIA CUDA and Docker GPU Runtime Configured! ===${NC}"
echo -e "Please reboot your system to load the new GPU drivers."
echo -e "After rebooting, you can verify GPU functionality with:"
echo -e "  ${YELLOW}nvidia-smi${NC}"
echo -e "And verify PyTorch GPU detection inside your venv with:"
echo -e "  ${YELLOW}python3 -c \"import torch; print('GPU available:', torch.cuda.is_available())\"${NC}"
echo ""
