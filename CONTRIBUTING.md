# Contributing to NovaForge Linux

Thank you for your interest in contributing to NovaForge Linux! This document provides guidelines and instructions for contributing.

## 📋 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## 🚀 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/novaforge-linux/novaforge/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (run `neofetch` or check NovaForge Control Center)
   - Screenshots if applicable

### Suggesting Features

1. Open a [Feature Request](https://github.com/novaforge-linux/novaforge/issues/new?template=feature_request.md)
2. Describe the feature and its use case
3. Explain how it fits NovaForge's vision (Gaming + Dev + AI)

### Submitting Changes

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes**:
   ```bash
   # Lint shell scripts
   shellcheck build/scripts/*.sh build/auto/*
   
   # Lint Python code
   python3 -m flake8 build/config/includes.chroot/usr/share/novaforge/
   
   # Build ISO (requires Ubuntu 24.04)
   make iso
   ```
5. **Commit** with clear messages:
   ```bash
   git commit -m "feat: add new wallpaper variant"
   git commit -m "fix: resolve SDDM theme blur on Wayland"
   git commit -m "docs: update build instructions for Noble"
   ```
6. **Push** and create a **Pull Request**

### Commit Message Format

We use conventional commits:

| Prefix | Description |
|--------|-------------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `style:` | Code style / formatting |
| `refactor:` | Code refactoring |
| `perf:` | Performance improvement |
| `test:` | Adding/updating tests |
| `build:` | Build system changes |
| `ci:` | CI/CD changes |
| `chore:` | Maintenance tasks |

## 📁 Project Areas

| Area | Directory | Skills Needed |
|------|-----------|---------------|
| Build System | `build/` | Shell scripting, live-build |
| KDE Themes | `build/config/includes.chroot/usr/share/plasma/` | QML, SVG, KDE theming |
| SDDM Theme | `build/config/includes.chroot/usr/share/sddm/` | QML, Qt Quick |
| GRUB Theme | `build/config/includes.chroot/usr/share/grub/` | GRUB scripting |
| Plymouth | `build/config/includes.chroot/usr/share/plymouth/` | Plymouth scripting |
| Control Center | `build/config/includes.chroot/usr/share/novaforge/` | Python, PyQt5 |
| Wallpapers | `branding/wallpapers/` | Graphic design |
| Documentation | `docs/` | Technical writing |
| CI/CD | `.github/workflows/` | GitHub Actions |

## 🎨 Design Guidelines

- Follow the NovaForge color palette (see `branding/colors.md`)
- Dark mode first — all UI must look great on dark backgrounds
- Use **Inter** for UI text, **JetBrains Mono** for code/terminal
- Accent colors: Cyan `#00E5FF`, Purple `#7C3AED`, Amber `#F59E0B`
- Maintain visual consistency across all themes (GRUB → Plymouth → SDDM → KDE)

## 🧪 Testing

### Local Testing

```bash
# Build ISO
make iso

# Test in QEMU
make test-qemu

# Or manually:
qemu-system-x86_64 -cdrom output/novaforge-linux-*.iso -m 4096 -boot d
```

### What to Test

- [ ] GRUB theme displays correctly
- [ ] Plymouth splash animation plays smoothly
- [ ] SDDM login screen renders properly
- [ ] KDE desktop loads with correct theme
- [ ] Panel layout is correct (top bar + bottom dock)
- [ ] All pre-installed software launches
- [ ] Control Center profile switching works
- [ ] System optimization is applied

## ❓ Questions?

Open a [Discussion](https://github.com/novaforge-linux/novaforge/discussions) or reach out in Issues.

---

Thank you for helping make NovaForge Linux better! 🔥
