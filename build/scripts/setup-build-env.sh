#!/bin/bash
# ============================================================
# NovaForge Linux — Build Environment Setup
# ============================================================
# Installs all dependencies required to build the ISO.
# Must be run on Ubuntu 24.04 LTS.
# Usage: sudo bash setup-build-env.sh
# ============================================================

set -e

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}[NovaForge]${NC} Setting up build environment..."

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}[NovaForge]${NC} This script must be run as root (sudo)."
    exit 1
fi

# Check Ubuntu version
if ! grep -q "noble\|24.04" /etc/os-release 2>/dev/null; then
    echo -e "${RED}[NovaForge]${NC} WARNING: This script is designed for Ubuntu 24.04 LTS (Noble)."
    echo -e "${RED}[NovaForge]${NC} Building on other versions may cause issues."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package lists
echo -e "${CYAN}[NovaForge]${NC} Updating package lists..."
apt-get update

# Install live-build and dependencies
echo -e "${CYAN}[NovaForge]${NC} Installing build tools..."
apt-get install -y \
    live-build \
    debootstrap \
    xorriso \
    squashfs-tools \
    grub-pc-bin \
    grub-efi-amd64-bin \
    grub-efi-amd64-signed \
    shim-signed \
    mtools \
    dosfstools \
    isolinux \
    syslinux-utils \
    gdisk \
    fdisk \
    apt-utils \
    coreutils \
    genisoimage

# Install optional tools
echo -e "${CYAN}[NovaForge]${NC} Installing helper tools..."
apt-get install -y \
    git \
    curl \
    wget \
    shellcheck \
    qemu-system-x86 \
    ovmf \
    2>/dev/null || true

# Install font generation tools (for GRUB)
echo -e "${CYAN}[NovaForge]${NC} Installing font tools..."
apt-get install -y \
    grub-common \
    fonts-inter \
    fonttools \
    2>/dev/null || true

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Build environment setup complete! ✓        ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║   Next steps:                                ║${NC}"
echo -e "${GREEN}║     1. cd to project root                    ║${NC}"
echo -e "${GREEN}║     2. Run: make iso                         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
