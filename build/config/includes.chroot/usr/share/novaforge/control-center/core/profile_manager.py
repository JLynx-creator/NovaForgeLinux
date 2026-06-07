"""
NovaForge Control Center — Profile Manager
============================================
Manages system performance profiles (Gaming, Development, AI).
"""

import os
import subprocess


PROFILES = {
    "gaming": {
        "cpu_governor": "performance",
        "swappiness": 10,
        "disable_services": ["cups-browsed"],
        "enable_services": ["gamemode"],
        "env_vars": {
            "MANGOHUD": "1",
            "DXVK_ASYNC": "1",
        },
        "sysctl": {
            "vm.swappiness": "10",
            "vm.vfs_cache_pressure": "50",
        },
    },
    "development": {
        "cpu_governor": "powersave",
        "swappiness": 60,
        "disable_services": [],
        "enable_services": ["docker"],
        "env_vars": {},
        "sysctl": {
            "vm.swappiness": "60",
            "fs.inotify.max_user_watches": "524288",
        },
    },
    "ai": {
        "cpu_governor": "performance",
        "swappiness": 10,
        "disable_services": ["cups-browsed"],
        "enable_services": [],
        "env_vars": {
            "CUDA_VISIBLE_DEVICES": "all",
        },
        "sysctl": {
            "vm.swappiness": "10",
            "vm.overcommit_memory": "1",
        },
    },
}

PROFILE_STATE_FILE = "/etc/novaforge/current-profile"


class ProfileManager:
    """Manage system performance profiles."""

    def get_current_profile(self):
        """Get the currently active profile name."""
        try:
            with open(PROFILE_STATE_FILE, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "development"  # Default

    def switch_profile(self, profile_name):
        """Switch to the specified profile. Requires root."""
        if profile_name not in PROFILES:
            return False

        profile = PROFILES[profile_name]

        try:
            # Set CPU governor
            self._set_cpu_governor(profile["cpu_governor"])

            # Apply sysctl settings
            for key, value in profile["sysctl"].items():
                self._run_sudo(["sysctl", "-w", f"{key}={value}"])

            # Manage services
            for svc in profile.get("disable_services", []):
                self._run_sudo(["systemctl", "stop", svc])

            for svc in profile.get("enable_services", []):
                self._run_sudo(["systemctl", "start", svc])

            # Write environment variables
            env_file = "/etc/novaforge/profile-env.sh"
            env_lines = ["#!/bin/bash", f"# NovaForge {profile_name} profile"]
            for key, value in profile.get("env_vars", {}).items():
                env_lines.append(f'export {key}="{value}"')

            self._write_file_sudo(env_file, "\n".join(env_lines) + "\n")

            # Save current profile
            self._write_file_sudo(PROFILE_STATE_FILE, profile_name + "\n")

            return True

        except Exception as e:
            print(f"Error switching profile: {e}")
            return False

    def _set_cpu_governor(self, governor):
        """Set CPU frequency governor for all cores."""
        try:
            # Find all CPU frequency scaling governors
            import glob
            gov_files = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
            for gov_file in gov_files:
                self._run_sudo(["tee", gov_file], input_text=governor)
        except Exception:
            # Fallback to cpupower
            self._run_sudo(["cpupower", "frequency-set", "-g", governor])

    def _run_sudo(self, cmd, input_text=None):
        """Run a command with pkexec for privilege escalation."""
        full_cmd = ["pkexec"] + cmd
        result = subprocess.run(
            full_cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0

    def _write_file_sudo(self, path, content):
        """Write content to a file with sudo privileges."""
        # Ensure directory exists
        dir_path = os.path.dirname(path)
        self._run_sudo(["mkdir", "-p", dir_path])
        
        proc = subprocess.Popen(
            ["pkexec", "tee", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        proc.communicate(input=content)
        return proc.returncode == 0
