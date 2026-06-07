"""
NovaForge Control Center — Driver Manager
===========================================
GPU driver detection and installation.
"""

import subprocess
import re


class DriverManager:
    """Manage GPU drivers."""

    def get_gpu_info(self):
        """Detect GPU hardware and current driver."""
        info = {
            "name": "Unknown",
            "vendor": "Unknown",
            "driver": "Unknown",
        }

        try:
            result = subprocess.run(
                ["lspci", "-vnns"],
                capture_output=True, text=True, timeout=10
            )
            # Find VGA/3D controller lines
            for block in result.stdout.split("\n\n"):
                if "VGA" in block or "3D" in block:
                    lines = block.split("\n")
                    if lines:
                        # First line has device name
                        match = re.search(r':\s+(.+)$', lines[0])
                        if match:
                            info["name"] = match.group(1).strip()

                        # Check vendor
                        name_lower = info["name"].lower()
                        if "nvidia" in name_lower:
                            info["vendor"] = "NVIDIA"
                        elif "amd" in name_lower or "radeon" in name_lower:
                            info["vendor"] = "AMD"
                        elif "intel" in name_lower:
                            info["vendor"] = "Intel"

                        # Find kernel driver
                        for line in lines:
                            if "Kernel driver" in line:
                                driver_match = re.search(r':\s+(\S+)', line)
                                if driver_match:
                                    info["driver"] = driver_match.group(1)
                    break

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return info

    def install_nvidia_recommended(self):
        """Install the recommended NVIDIA driver."""
        try:
            result = subprocess.run(
                ["pkexec", "ubuntu-drivers", "install", "--recommend"],
                capture_output=True, text=True, timeout=300
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_available_drivers(self):
        """List available drivers for the system."""
        try:
            result = subprocess.run(
                ["ubuntu-drivers", "list"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return [d.strip() for d in result.stdout.strip().split("\n") if d.strip()]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return []
