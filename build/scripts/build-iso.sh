#!/bin/bash
# ============================================================
# NovaForge Linux — Custom ISO Build Script
# ============================================================
# Replaces live-build with a transparent debootstrap + grub-mkrescue
# flow to generate a BIOS+UEFI bootable Live ISO.
# Usage: sudo bash build-iso.sh [version]
# ============================================================

set -ex

VERSION="${1:-$(cat ../VERSION 2>/dev/null || echo '2.1.0')}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(dirname "$SCRIPT_DIR")"

# Navigate to build directory and redirect all stdout/stderr to build.log
cd "$BUILD_DIR"
touch build.log
exec > >(tee -a build.log) 2>&1

echo "============================================================"
echo "🔥 NovaForge Linux Custom ISO Builder 🔥"
echo "Version: ${VERSION}"
echo "Build started at: $(date)"
echo "============================================================"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: This script must be run as root (sudo)."
    exit 1
fi

# Install dependencies on the host if missing
echo "[NovaForge] Checking host build dependencies..."
for dep in debootstrap squashfs-tools grub-mkrescue xorriso mtools dosfstools grub-pc-bin grub-efi-amd64-bin; do
    if ! dpkg -s "$dep" >/dev/null 2>&1; then
        echo "[NovaForge] Installing host package: $dep..."
        apt-get update && apt-get install -y "$dep"
    fi
done
echo "[NovaForge] Host dependencies satisfied."

# Clean up previous builds
echo "[NovaForge] Cleaning up previous directories..."
umount -lf chroot/dev/pts || true
umount -lf chroot/dev || true
umount -lf chroot/proc || true
umount -lf chroot/sys || true
rm -rf chroot livecd

# Create required output directory
mkdir -p ../output
mkdir -p chroot
mkdir -p livecd/casper
mkdir -p livecd/boot/grub

# 1. Bootstrap Ubuntu Noble minimal rootfs
echo "[NovaForge] Bootstrapping Ubuntu Noble base (Noble Numbat)..."
debootstrap --variant=minbase noble chroot http://archive.ubuntu.com/ubuntu

# 2. Configure chroot mirror sources list to include universe, restricted, and multiverse
echo "[NovaForge] Setting up chroot sources.list..."
cat > chroot/etc/apt/sources.list << EOF
deb http://archive.ubuntu.com/ubuntu noble main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu noble-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu noble-security main restricted universe multiverse
EOF

# 3. Mount virtual systems
echo "[NovaForge] Mounting chroot virtual filesystems..."
mount --bind /dev chroot/dev
mount --bind /dev/pts chroot/dev/pts
mount --bind /proc chroot/proc
mount --bind /sys chroot/sys

# 4. Copy resolver configs
cp /etc/resolv.conf chroot/etc/resolv.conf
cp /etc/hosts chroot/etc/hosts

# 5. Stamp version info into chroot
VERSION_DIR="chroot/etc/novaforge"
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

# 6. Parse required packages lists
echo "[NovaForge] Parsing package lists..."
PACKAGES=""
for list_file in config/package-lists/*.list.chroot; do
    if [ -f "$list_file" ]; then
        echo "Parsing package list: $list_file"
        while read -r line || [ -n "$line" ]; do
            # Trim whitespace and skip comments/empty lines
            line=$(echo "$line" | xargs)
            [[ -z "$line" ]] && continue
            [[ "$line" =~ ^# ]] && continue
            PACKAGES="$PACKAGES $line"
        done < "$list_file"
    fi
done

# 7. Run setup repositories hook inside chroot (to register external keys/sources)
echo "[NovaForge] Executing repository setup hook..."
mkdir -p chroot/tmp
cp config/hooks/live/0010-setup-repos.hook.chroot chroot/tmp/
chmod +x chroot/tmp/0010-setup-repos.hook.chroot
chroot chroot env DEBIAN_FRONTEND=noninteractive /bin/bash /tmp/0010-setup-repos.hook.chroot
rm -f chroot/tmp/0010-setup-repos.hook.chroot

# 8. Install packages inside chroot
echo "[NovaForge] Installing system packages inside chroot..."
chroot chroot apt-get update
chroot chroot env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $PACKAGES

# 9. Copy include filesystem files into chroot
echo "[NovaForge] Deploying includes filesystem overlay..."
if [ -d config/includes.chroot ]; then
    cp -r config/includes.chroot/* chroot/
fi

# 10. Run remaining customization hooks
echo "[NovaForge] Running customization hooks..."
for hook in config/hooks/live/*.hook.chroot; do
    if [ -f "$hook" ]; then
        hook_name=$(basename "$hook")
        if [ "$hook_name" != "0010-setup-repos.hook.chroot" ]; then
            echo "Executing hook: $hook_name"
            cp "$hook" chroot/tmp/
            chmod +x "chroot/tmp/$hook_name"
            chroot chroot env DEBIAN_FRONTEND=noninteractive /bin/bash "/tmp/$hook_name"
            rm -f "chroot/tmp/$hook_name"
        fi
    fi
done

# 11. Extract installed kernel and initrd for the livecd structure
echo "[NovaForge] Extracting kernel and initrd..."
KERNEL_FILE=$(ls chroot/boot/vmlinuz-* 2>/dev/null | head -n 1)
INITRD_FILE=$(ls chroot/boot/initrd.img-* 2>/dev/null | head -n 1)

if [ -z "$KERNEL_FILE" ] || [ -z "$INITRD_FILE" ]; then
    echo "ERROR: Linux kernel or initrd.img was not installed or found in chroot/boot!"
    exit 1
fi

echo "Found Kernel: $KERNEL_FILE"
echo "Found Initrd: $INITRD_FILE"
cp "$KERNEL_FILE" livecd/casper/vmlinuz
cp "$INITRD_FILE" livecd/casper/initrd.img

# 12. Unmount chroot filesystems
echo "[NovaForge] Unmounting chroot virtual filesystems..."
umount -lf chroot/dev/pts || true
umount -lf chroot/dev || true
umount -lf chroot/proc || true
umount -lf chroot/sys || true

# 13. Create SquashFS compressed filesystem
echo "[NovaForge] Building SquashFS compressed live filesystem..."
mksquashfs chroot livecd/casper/filesystem.squashfs -noappend -comp xz

# 14. Configure GRUB bootloader menu config
echo "[NovaForge] Creating bootloader config..."
cat > livecd/boot/grub/grub.cfg << EOF
set default="0"
set timeout=10

insmod all_video
insmod font

set menu_color_normal=white/black
set menu_color_highlight=cyan/black

menuentry "NovaForge Linux Live (Version ${VERSION})" {
    set gfxpayload=keep
    linux /casper/vmlinuz boot=casper quiet splash ---
    initrd /casper/initrd.img
}

menuentry "NovaForge Linux Live (Safe Graphics mode)" {
    set gfxpayload=keep
    linux /casper/vmlinuz boot=casper nomodeset quiet splash ---
    initrd /casper/initrd.img
}
EOF

# 15. Compile the bootable ISO using grub-mkrescue
echo "[NovaForge] Packaging bootable ISO image (grub-mkrescue)..."
FINAL_ISO="../output/novaforge-linux-${VERSION}-amd64.iso"
grub-mkrescue -o "$FINAL_ISO" livecd

# 16. Generate verification checksums
echo "[NovaForge] Generating verification checksums..."
sha256sum "$FINAL_ISO" > "${FINAL_ISO}.sha256"
md5sum "$FINAL_ISO" > "${FINAL_ISO}.md5"

# Clean up
echo "[NovaForge] Cleaning up intermediate chroot and build directories..."
rm -rf chroot livecd

echo "============================================================"
echo "✅ Custom ISO Build Completed Successfully!"
echo "ISO Output: $FINAL_ISO"
echo "Size: $(du -h "$FINAL_ISO" | cut -f1)"
echo "Build finished at: $(date)"
echo "============================================================"
