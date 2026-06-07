# Customizing NovaForge Linux

NovaForge is designed with modularity in mind. All theme, packages, and optimization settings can be customized before building.

---

## 1. Modifying Pre-installed Packages

To add or remove packages, navigate to the `build/config/package-lists/` directory:

* **`base.list.chroot`**: Core system and kernel libraries.
* **`kde.list.chroot`**: Plasma desktop shell components and apps.
* **`development.list.chroot`**: Text editors, language runtimes, Docker.
* **`gaming.list.chroot`**: Steam, Wine, MangoHUD overlays.
* **`ai.list.chroot`**: Python ML package tools.
* **`theming.list.chroot`**: Accent themes and cursors.

**To add a package:** Simply append its Debian/Ubuntu package name on a new line. For example, to add `neovim`, edit `development.list.chroot`:
```
neovim
```

---

## 2. Branding & Wallpapers

Custom assets are stored in the `/usr/share/` structure of the filesystem overlay:

* **Wallpapers**: Place new background images at:
  `build/config/includes.chroot/usr/share/wallpapers/novaforge/contents/images/`
* **SDDM Background**: Replace:
  `build/config/includes.chroot/usr/share/sddm/themes/novaforge/background.jpg`
* **GRUB Background**: Replace:
  `build/config/includes.chroot/usr/share/grub/themes/novaforge/background.png`

---

## 3. Modifying Boot Experience Themes

### GRUB boot menu
To customize fonts, layout, and entry icons:
* Edit configuration: `build/config/includes.chroot/usr/share/grub/themes/novaforge/theme.txt`
* Run `build/scripts/generate-grub-font.sh` if you want to convert a new `.ttf` font to GRUB's `.pf2` format.

### Plymouth splash screen
* Edit the animation script: `build/config/includes.chroot/usr/share/plymouth/themes/novaforge/novaforge.script`
* Replace progress dots or central branding images in the same folder.

---

## 4. Default Desktop User Configurations

Default settings for newly created user profiles (and the live user) are defined in `/etc/skel/`. These files are copied to `$HOME` upon user creation:

* **Window manager & compositor rules**:
  `build/config/includes.chroot/etc/skel/.config/kwinrc`
* **Fonts & general style colors**:
  `build/config/includes.chroot/etc/skel/.config/kdeglobals`
* **Application starter configs**:
  `build/config/includes.chroot/etc/skel/.config/plasmarc`
* **Default Terminal Settings**:
  `build/config/includes.chroot/etc/skel/.config/konsolerc`
  `build/config/includes.chroot/etc/skel/.local/share/konsole/`
* **Qt Theme (Kvantum)**:
  `build/config/includes.chroot/etc/skel/.config/Kvantum/kvantum.kvconfig`
