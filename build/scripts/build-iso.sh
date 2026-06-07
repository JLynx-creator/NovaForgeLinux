#!/bin/bash
# ============================================================
# NovaForge Linux — ISO Build Script
# ============================================================
# Main entry point for building the NovaForge Linux ISO.
# Usage: sudo bash build-iso.sh [version]
# ============================================================

set -e

VERSION="${1:-$(cat ../VERSION 2>/dev/null || echo '1.0.0')}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║      🔥 NovaForge Linux ISO Builder 🔥       ║"
echo "  ║            Version: ${VERSION}                    ║"
echo "  ╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}[NovaForge]${NC} This script must be run as root (sudo)."
    exit 1
fi

# Check dependencies
echo -e "${CYAN}[NovaForge]${NC} Checking dependencies..."
for cmd in lb debootstrap xorriso mksquashfs; do
    if ! command -v "$cmd" &>/dev/null; then
        echo -e "${RED}[NovaForge]${NC} Missing: $cmd"
        echo -e "${RED}[NovaForge]${NC} Run: sudo bash build/scripts/setup-build-env.sh"
        exit 1
    fi
done
echo -e "${GREEN}[NovaForge]${NC} All dependencies found."

# Navigate to build directory
cd "$BUILD_DIR"

# Clean previous build if exists
if [ -d ".build" ]; then
    echo -e "${YELLOW}[NovaForge]${NC} Cleaning previous build..."
    lb clean
fi

# Configure
echo -e "${CYAN}[NovaForge]${NC} Configuring live-build..."
bash auto/config

# Stamp version into the filesystem overlay
VERSION_DIR="config/includes.chroot/etc/novaforge"
mkdir -p "$VERSION_DIR"
echo "$VERSION" > "$VERSION_DIR/version"
cat > "$VERSION_DIR/release" << EOF
DISTRIB_ID=NovaForge
DISTRIB_RELEASE=${VERSION}
DISTRIB_CODENAME=ignition
DISTRIB_DESCRIPTION="NovaForge Linux ${VERSION}"
DISTRIB_BASE=Ubuntu
DISTRIB_BASE_CODENAME=noble
DISTRIB_BASE_RELEASE=24.04
EOF

# Build
echo -e "${CYAN}[NovaForge]${NC} Starting build (this may take 30-60 minutes)..."
echo -e "${CYAN}[NovaForge]${NC} Build started at: $(date)"

lb build 2>&1 | tee build.log

BUILD_EXIT=${PIPESTATUS[0]}

if [ $BUILD_EXIT -eq 0 ]; then
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════╗"
    echo "  ║         ✅ Build Successful!                  ║"
    echo "  ╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}[NovaForge]${NC} Build completed at: $(date)"
    
    # Rename ISO
    if ls *.iso 1>/dev/null 2>&1; then
        ISO_FILE=$(ls *.iso | head -1)
        FINAL_NAME="novaforge-linux-${VERSION}-amd64.iso"
        mv "$ISO_FILE" "$FINAL_NAME"
        
        # Generate checksums
        echo -e "${CYAN}[NovaForge]${NC} Generating checksums..."
        sha256sum "$FINAL_NAME" > "${FINAL_NAME}.sha256"
        md5sum "$FINAL_NAME" > "${FINAL_NAME}.md5"
        
        echo -e "${GREEN}[NovaForge]${NC} ISO: $FINAL_NAME"
        echo -e "${GREEN}[NovaForge]${NC} Size: $(du -h "$FINAL_NAME" | cut -f1)"
        echo -e "${GREEN}[NovaForge]${NC} SHA256: $(cat "${FINAL_NAME}.sha256" | cut -d' ' -f1)"
    fi
else
    echo -e "${RED}${BOLD}"
    echo "  ╔══════════════════════════════════════════════╗"
    echo "  ║         ❌ Build Failed!                      ║"
    echo "  ╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${RED}[NovaForge]${NC} Check build.log for details."
    exit 1
fi
