#!/bin/bash
# ============================================================
# NovaForge Linux — ISO Validation Script
# ============================================================
# Validates a built ISO image for correctness.
# Usage: bash validate-iso.sh <path-to-iso>
# ============================================================

set -e

ISO_PATH="${1}"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    local desc="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} $desc"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}✗${NC} $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo -e "${CYAN}[NovaForge]${NC} Validating ISO: $ISO_PATH"
echo ""

# Check ISO exists
if [ ! -f "$ISO_PATH" ]; then
    echo -e "${RED}[NovaForge]${NC} ISO file not found: $ISO_PATH"
    exit 1
fi

# Check file is a valid ISO
file "$ISO_PATH" | grep -qi "iso\|boot\|hybrid" 2>/dev/null
check "File is a valid ISO image" $?

# Check file size (should be > 1GB for a full desktop)
SIZE=$(stat -c%s "$ISO_PATH" 2>/dev/null || stat -f%z "$ISO_PATH" 2>/dev/null)
[ "$SIZE" -gt 1073741824 ] 2>/dev/null
check "ISO size > 1GB (size: $(numfmt --to=iec "$SIZE" 2>/dev/null || echo "${SIZE} bytes"))" $?

# Check ISO hybrid boot capability
file "$ISO_PATH" | grep -qi "boot" 2>/dev/null
check "ISO has boot sector" $?

# Check for EFI boot
if command -v xorriso &>/dev/null; then
    xorriso -indev "$ISO_PATH" -find / -name "*.efi" 2>/dev/null | grep -q "efi"
    check "EFI boot files present" $?
fi

# Check for squashfs
if command -v xorriso &>/dev/null; then
    xorriso -indev "$ISO_PATH" -find / -name "*.squashfs" 2>/dev/null | grep -q "squashfs"
    check "SquashFS filesystem found" $?
fi

# Verify checksum if exists
if [ -f "${ISO_PATH}.sha256" ]; then
    sha256sum -c "${ISO_PATH}.sha256" &>/dev/null
    check "SHA256 checksum verified" $?
else
    echo -e "  ${YELLOW}⊘${NC} SHA256 checksum file not found (skipped)"
fi

echo ""
echo -e "${CYAN}[NovaForge]${NC} Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"

if [ "$FAIL" -gt 0 ]; then
    echo -e "${RED}[NovaForge]${NC} Validation failed!"
    exit 1
else
    echo -e "${GREEN}[NovaForge]${NC} All checks passed!"
fi
