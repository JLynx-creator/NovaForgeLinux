#!/bin/bash
# ============================================================
# NovaForge Linux — Dockerized ISO Build Script
# ============================================================
# Main entry point for building the NovaForge Linux ISO
# inside an isolated Docker container.
# Usage: sudo bash build-iso.sh [version]
# ============================================================

set -ex

VERSION="${1:-$(cat ../VERSION 2>/dev/null || echo '2.2.0')}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(dirname "$SCRIPT_DIR")"
REPO_DIR="$(dirname "$BUILD_DIR")"

# Navigate to project root and redirect all stdout/stderr to build.log
cd "$REPO_DIR"
touch build.log
exec > >(tee -a build.log) 2>&1

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}"
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║  🔥 NovaForge Linux Dockerized ISO Builder 🔥 ║"
echo "  ║            Version: ${VERSION}                    ║"
echo "  ╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &>/dev/null; then
    echo -e "${RED}[NovaForge]${NC} Docker must be installed and running."
    exit 1
fi

# Build the Docker builder image
echo -e "${CYAN}[NovaForge]${NC} Building Docker builder image..."
docker build -t novaforge-builder:latest -f build/Dockerfile build/

# Stamp version into the filesystem overlay (run locally before mounting)
VERSION_DIR="build/config/includes.chroot/etc/novaforge"
mkdir -p "$VERSION_DIR"
echo "$VERSION" > "$VERSION_DIR/version"
cat > "$VERSION_DIR/release" << EOF
DISTRIB_ID=NovaForge
DISTRIB_RELEASE=${VERSION}
DISTRIB_CODENAME=ignition-v2
DISTRIB_DESCRIPTION="NovaForge Linux ${VERSION}"
DISTRIB_BASE=Ubuntu
DISTRIB_BASE_CODENAME=noble
DISTRIB_BASE_RELEASE=24.04
EOF

# Ensure directory permissions and clean previous builds
echo -e "${YELLOW}[NovaForge]${NC} Cleaning previous builds inside Docker..."
docker run --rm --privileged -v "$(pwd)":/build -w /build novaforge-builder:latest /bin/bash -c "cd build && lb clean || true"

# Run the build inside Docker
echo -e "${CYAN}[NovaForge]${NC} Starting compilation inside Docker container..."
echo -e "${CYAN}[NovaForge]${NC} Build started at: $(date)"

# Run live-build config and build inside the container
docker run --rm --privileged \
    -v "$(pwd)":/build \
    -w /build \
    novaforge-builder:latest \
    /bin/bash -c "cd build && lb config && lb build"

BUILD_EXIT=$?

if [ $BUILD_EXIT -eq 0 ]; then
    echo ""
    echo -e "${GREEN}${BOLD}"
    echo "  ╔══════════════════════════════════════════════╗"
    echo "  ║         ✅ Build Successful!                  ║"
    echo "  ╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${GREEN}[NovaForge]${NC} Build completed at: $(date)"
    
    # Check for generated ISO in build directory
    if ls build/*.iso 1>/dev/null 2>&1; then
        ISO_FILE=$(ls build/*.iso | head -1)
        FINAL_ISO="output/novaforge-linux-${VERSION}-amd64.iso"
        mkdir -p output
        mv "$ISO_FILE" "$FINAL_ISO"
        
        # Generate checksums
        echo -e "${CYAN}[NovaForge]${NC} Generating checksums..."
        sha256sum "$FINAL_ISO" > "${FINAL_ISO}.sha256"
        md5sum "$FINAL_ISO" > "${FINAL_ISO}.md5"
        
        echo -e "${GREEN}[NovaForge]${NC} ISO: $FINAL_ISO"
        echo -e "${GREEN}[NovaForge]${NC} Size: $(du -h "$FINAL_ISO" | cut -f1)"
    else
        echo -e "${RED}[NovaForge]${NC} ISO file was not found in build directory after build."
        exit 1
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
