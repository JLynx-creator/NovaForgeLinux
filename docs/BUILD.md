# Building NovaForge Linux

This document details the hardware requirements, prerequisites, build instructions, and verification steps for compiling the NovaForge Linux ISO image.

---

## Hardware & System Requirements

To compile the ISO locally, you must use an **Ubuntu-based system** (preferably Ubuntu 24.04 Noble Numbat) due to `live-build` kernel constraints and loop device mount requirements.

| Metric | Minimum | Recommended |
|--------|---------|-------------|
| **OS** | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |
| **CPU** | 4 Cores | 8+ Cores |
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 25 GB free | 50 GB free (SSD) |
| **Network** | Broad-band (for caching package downloads) |

---

## Build Steps

Follow these steps chronologically to build your custom distribution:

### 1. Set Up the Build Environment
First, update your local packages and install the compiler utilities (`live-build`, `xorriso`, `debootstrap`, etc.):

```bash
make setup
```

This commands executes `build/scripts/setup-build-env.sh` under sudo.

### 2. Configure & Build the ISO
Start the ISO compilation:

```bash
make iso
```

**How it works:**
* Cleans any residual `.build` states.
* Runs `auto/config` to set Ubuntu bootstrap options.
* Templates the configuration overlay (`build/config/includes.chroot/`).
* Runs `lb build` to bootstrap the chroot filesystem, download package lists, apply chroot hooks, compress the filesystem into SquashFS, and generate the bootable ISO hybrid image.

*Note: The process can take between 20 to 60 minutes depending on your CPU power and internet speed.*

### 3. Verify the Build
Once complete, validate the ISO structure and output:

```bash
make validate
```

This verifies the presence of boot loaders, SquashFS archives, and validates the file signature matches.

---

## Boot and Testing in QEMU

You can test the resulting ISO inside a local QEMU virtual machine directly from the terminal:

```bash
make test-qemu
```

---

## Troubleshooting

### Loop device issues
`live-build` uses loop devices to mount filesystem overlays. If the build fails with mounting errors, execute:
```bash
sudo losetup -D
make clean
```

### APT mirror caching errors
If repository indices become corrupted or timeout, perform a deep clean:
```bash
make purge
make iso
```
This drops the downloaded `.deb` package cache and starts fresh.
