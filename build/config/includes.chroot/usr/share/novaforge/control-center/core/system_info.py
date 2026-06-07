"""
NovaForge Control Center — System Information Module
=====================================================
Collects static and live system information.
"""

import os
import platform
import subprocess

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import distro
    HAS_DISTRO = True
except ImportError:
    HAS_DISTRO = False


class SystemInfo:
    """Collect and provide system information."""

    def get_static_info(self):
        """Get static system information (doesn't change during session)."""
        info = {
            "kernel": platform.release(),
            "arch": platform.machine(),
            "hostname": platform.node(),
            "desktop": os.environ.get("XDG_CURRENT_DESKTOP", "Unknown"),
        }

        # Distribution info
        if HAS_DISTRO:
            info["distro"] = f"{distro.name()} {distro.version()}"
        else:
            info["distro"] = self._read_novaforge_version()

        # CPU model
        info["cpu_model"] = self._get_cpu_model()

        return info

    def get_live_stats(self):
        """Get real-time system statistics."""
        stats = {
            "cpu_percent": 0,
            "ram_used_gb": 0,
            "ram_total_gb": 0,
            "ram_percent": 0,
            "disk_used_gb": 0,
            "disk_total_gb": 0,
            "disk_percent": 0,
            "gpu_name": "N/A",
        }

        if HAS_PSUTIL:
            # CPU
            stats["cpu_percent"] = psutil.cpu_percent(interval=0.1)

            # RAM
            mem = psutil.virtual_memory()
            stats["ram_used_gb"] = mem.used / (1024 ** 3)
            stats["ram_total_gb"] = mem.total / (1024 ** 3)
            stats["ram_percent"] = mem.percent

            # Disk
            disk = psutil.disk_usage("/")
            stats["disk_used_gb"] = disk.used / (1024 ** 3)
            stats["disk_total_gb"] = disk.total / (1024 ** 3)
            stats["disk_percent"] = disk.percent

        # GPU
        stats["gpu_name"] = self._get_gpu_name()

        return stats

    def _get_cpu_model(self):
        """Get CPU model name from /proc/cpuinfo."""
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except (FileNotFoundError, PermissionError):
            pass
        return platform.processor() or "Unknown"

    def _get_gpu_name(self):
        """Get GPU name using lspci."""
        try:
            result = subprocess.run(
                ["lspci", "-v"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "VGA" in line or "3D" in line:
                    # Extract the GPU name after the colon
                    parts = line.split(":")
                    if len(parts) >= 3:
                        return parts[2].strip()
                    elif len(parts) >= 2:
                        return parts[1].strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return "N/A"

    def _read_novaforge_version(self):
        """Read NovaForge version from /etc/novaforge/release."""
        try:
            with open("/etc/novaforge/release", "r") as f:
                for line in f:
                    if line.startswith("DISTRIB_DESCRIPTION="):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            pass
        return "NovaForge Linux"
