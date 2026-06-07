<div align="center">

# 🔥 NovaForge Linux

### *Forge Your Universe*

**A premium Ubuntu-based distribution for Gaming, Development & AI**

[![Build ISO](https://img.shields.io/badge/build-passing-00E5FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/novaforge-linux/novaforge/actions)
[![Version](https://img.shields.io/badge/version-1.0.0-7C3AED?style=for-the-badge)](https://github.com/novaforge-linux/novaforge/releases)
[![License](https://img.shields.io/badge/license-MIT-F59E0B?style=for-the-badge)](LICENSE)
[![Ubuntu](https://img.shields.io/badge/based_on-Ubuntu_24.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![KDE Plasma](https://img.shields.io/badge/desktop-KDE_Plasma_6-1D99F3?style=for-the-badge&logo=kde&logoColor=white)](https://kde.org)

---

*NovaForge Linux is a meticulously crafted Ubuntu LTS-based distribution that unifies Gaming, Software Development, and AI Development into a single, premium desktop experience. Install once — everything is ready.*

</div>

---

## ✨ Features

### 🎮 Gaming Ready
- **Steam** pre-installed with Proton support
- **Lutris** for managing all your game libraries
- **MangoHud** overlay for real-time performance monitoring
- **GameMode** for automatic system optimization during gameplay
- **Wine** & **Vulkan** drivers out of the box

### 💻 Developer Powerhouse
- **VS Code** with a polished dark theme
- **Git**, **Python 3**, **Node.js**, **Docker** — pre-configured
- **Build tools** and compilers ready to go
- Optimized **terminal** experience with JetBrains Mono font

### 🤖 AI Development
- **Ollama** for running local LLMs
- **CUDA-ready** setup scripts for NVIDIA GPUs
- **PyTorch** & **TensorFlow** environment bootstrap
- **Jupyter Notebook** pre-installed
- Python AI/ML libraries ready to use

### 🎨 Premium Design
- Custom **KDE Plasma 6** global theme with dark mode & neon accents
- Beautiful **GRUB** boot menu, **Plymouth** splash animation
- Modern **SDDM** login screen with glassmorphism design
- Hybrid panel layout: macOS-style top bar + Windows-style floating dock
- Custom **Konsole** terminal theme with transparency

### ⚡ System Optimization
- **Three performance profiles**: Gaming, Development, AI
- Unnecessary Ubuntu services disabled for faster boot
- Memory & CPU governor optimization per profile
- **NovaForge Control Center** for easy system management

---

## 📸 Screenshots

> Screenshots will be added after the first build.

---

## 🚀 Quick Start

### Download

Download the latest ISO from the [Releases](https://github.com/novaforge-linux/novaforge/releases) page.

### Create Bootable USB

```bash
# Linux
sudo dd if=novaforge-linux-1.0.0.iso of=/dev/sdX bs=4M status=progress

# Or use balenaEtcher, Ventoy, or Rufus (Windows)
```

### Build From Source

```bash
# Clone the repository
git clone https://github.com/novaforge-linux/novaforge.git
cd novaforge

# Set up build environment (Ubuntu 24.04 required)
sudo bash build/scripts/setup-build-env.sh

# Build the ISO
make iso

# The ISO will be in output/
ls output/*.iso
```

---

## 🏗️ Project Structure

```
novaforge/
├── build/                    # ISO build system
│   ├── auto/                 # live-build automation scripts
│   ├── config/               # Build configuration
│   │   ├── package-lists/    # Software packages to include
│   │   ├── hooks/            # Build-time customization scripts
│   │   ├── preseed/          # Installer pre-configuration
│   │   └── includes.chroot/  # Filesystem overlay
│   └── scripts/              # Build helper scripts
├── branding/                 # Logo, wallpapers, color palette
├── scripts/                  # Post-install & profile scripts
├── docs/                     # Documentation
├── .github/workflows/        # CI/CD pipeline
├── Makefile                  # Build orchestration
└── VERSION                   # Current version
```

---

## 🛠️ NovaForge Control Center

A built-in system management application that provides:

| Feature | Description |
|---------|-------------|
| **Dashboard** | CPU, RAM, GPU, disk usage at a glance |
| **Profiles** | Switch between Gaming, Dev, and AI modes |
| **Drivers** | GPU driver management shortcuts |
| **Updates** | Graphical apt update/upgrade center |

---

## 🎨 Design System

| Element | Value |
|---------|-------|
| Primary Color | `#00E5FF` — Cyan Neon |
| Secondary Color | `#7C3AED` — Electric Purple |
| Accent Color | `#F59E0B` — Amber Glow |
| Background | `#0A0A1A` → `#11111B` → `#1E1E2E` |
| UI Font | Inter |
| Mono Font | JetBrains Mono |
| Icons | Tela Circle Dark |
| Cursor | Bibata Modern Ice |

---

## 📋 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 64-bit dual-core | Quad-core+ |
| RAM | 4 GB | 16 GB |
| Storage | 25 GB | 50 GB+ SSD |
| GPU | Integrated | NVIDIA/AMD dedicated |
| Display | 1366×768 | 1920×1080+ |

---

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full version roadmap.

- **v1.0** — Initial release with core features
- **v1.1** — Additional themes, Flatpak integration
- **v1.2** — Custom installer, welcome app
- **v2.0** — ARM64 support, advanced AI tools

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

NovaForge Linux is released under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ for creators, gamers, and innovators.**

*NovaForge Linux — Forge Your Universe*

</div>
