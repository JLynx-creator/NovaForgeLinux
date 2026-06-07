#!/bin/bash
# ============================================================
# NovaForge Linux — GRUB Font Generator
# ============================================================
# Converts TTF fonts to GRUB PF2 format.
# Usage: bash generate-grub-font.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GRUB_THEME_DIR="${SCRIPT_DIR}/../config/includes.chroot/usr/share/grub/themes/novaforge"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}[NovaForge]${NC} Generating GRUB fonts..."

# Find Inter font
INTER_FONT=""
for path in \
    "/usr/share/fonts/truetype/inter/Inter-Regular.ttf" \
    "/usr/share/fonts/truetype/inter/Inter_18pt-Regular.ttf" \
    "/usr/share/fonts/opentype/inter/Inter-Regular.otf" \
    "/usr/share/fonts/TTF/Inter-Regular.ttf"; do
    if [ -f "$path" ]; then
        INTER_FONT="$path"
        break
    fi
done

if [ -z "$INTER_FONT" ]; then
    echo -e "${RED}[NovaForge]${NC} Inter font not found. Install with: sudo apt install fonts-inter"
    echo -e "${CYAN}[NovaForge]${NC} Falling back to DejaVu Sans..."
    INTER_FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fi

if [ ! -f "$INTER_FONT" ]; then
    echo -e "${RED}[NovaForge]${NC} No suitable font found. Exiting."
    exit 1
fi

mkdir -p "$GRUB_THEME_DIR"

# Generate regular font (16pt for menu items)
echo -e "${CYAN}[NovaForge]${NC} Generating regular font (16pt)..."
grub-mkfont -s 16 -o "${GRUB_THEME_DIR}/font.pf2" "$INTER_FONT"

# Generate large font (24pt for title)
echo -e "${CYAN}[NovaForge]${NC} Generating large font (24pt)..."
grub-mkfont -s 24 -o "${GRUB_THEME_DIR}/font-large.pf2" "$INTER_FONT"

echo -e "${GREEN}[NovaForge]${NC} GRUB fonts generated successfully!"
ls -la "${GRUB_THEME_DIR}"/*.pf2
