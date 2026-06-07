# NovaForge Performance Profiles

NovaForge Linux implements an active performance profiling system to customize your hardware configurations dynamically for **Gaming**, **Software Development**, or **AI workloads**.

---

## Profile Details

Each profile overrides CPU scaling, memory allocation constraints, background services, and environment parameters:

| Profile | CPU Governor | Swappiness | Managed Services | Key Environment Variables | Best Used For |
|---------|--------------|------------|------------------|---------------------------|---------------|
| **Gaming** | `performance` | `10` | Starts `gamemode`, stops `cups-browsed` | `MANGOHUD=1`<br>`DXVK_ASYNC=1` | Steam, Proton, Emulator gaming. |
| **Development** | `powersave` | `60` | Starts `docker` | *None* | Programming, Docker setups, compiling. |
| **AI** | `performance` | `10` | Stops `cups-browsed` | `CUDA_VISIBLE_DEVICES=all` | Model training, LLM inference, PyTorch. |

---

## Profile Toggling Methods

### 1. Graphical Interface (NovaForge Control Center)
Open the **NovaForge Control Center** from the system application launcher or run:
```bash
novaforge-control-center
```
Navigate to the **Profiles** tab in the sidebar, choose your desired performance mode, and click **Apply Profile**.

### 2. Command Line Scripts
If you are working from a terminal, run the shell script overlays directly:

```bash
# Activate Gaming Profile
sudo bash /scripts/profiles/gaming-mode.sh

# Activate Development Profile
sudo bash /scripts/profiles/dev-mode.sh

# Activate AI Profile
sudo bash /scripts/profiles/ai-mode.sh
```

---

## Architecture & Internals

* **Governor Setting**: Updates `/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` or uses `cpupower` utility to optimize core clock frequencies.
* **Environment variables**: System profile settings are written to `/etc/novaforge/profile-env.sh`. This file is sourced automatically during login shells to configure runtime options globally.
* **State File**: The active profile identifier is written to `/etc/novaforge/current-profile` to track active states.
