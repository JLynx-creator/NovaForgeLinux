FROM ubuntu:24.04

# Avoid prompt interactive warnings
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies needed for live-build
RUN apt-get update && apt-get install -y \
    live-build \
    debootstrap \
    xorriso \
    squashfs-tools \
    mtools \
    dosfstools \
    grub-pc-bin \
    grub-efi-amd64-bin \
    isolinux \
    fdisk \
    sudo \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
