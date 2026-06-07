"""
NovaForge Control Center — Update Manager
===========================================
Wraps apt for checking and applying system updates.
"""

import subprocess


class UpdateManager:
    """Manage system updates via apt."""

    def check_updates(self, progress_callback=None, output_callback=None):
        """Check for available updates. Returns count of updatable packages."""
        try:
            # Run apt update
            if progress_callback:
                progress_callback(10)
            if output_callback:
                output_callback("Running apt update...\n")

            result = subprocess.run(
                ["pkexec", "apt-get", "update"],
                capture_output=True, text=True, timeout=120
            )

            if output_callback and result.stdout:
                output_callback(result.stdout)

            if progress_callback:
                progress_callback(50)

            # Check upgradable packages
            if output_callback:
                output_callback("\nChecking for upgradable packages...\n")

            result = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True, text=True, timeout=30
            )

            if output_callback and result.stdout:
                output_callback(result.stdout)

            # Count upgradable (skip header line)
            lines = [l for l in result.stdout.strip().split("\n") if "/" in l]
            count = len(lines)

            if output_callback:
                output_callback(f"\n{count} packages can be upgraded.\n")

            if progress_callback:
                progress_callback(100)

            return count

        except subprocess.TimeoutExpired:
            if output_callback:
                output_callback("ERROR: Update check timed out.\n")
            return -1
        except Exception as e:
            if output_callback:
                output_callback(f"ERROR: {str(e)}\n")
            return -1

    def upgrade(self, progress_callback=None, output_callback=None):
        """Upgrade all packages. Returns True on success."""
        try:
            if progress_callback:
                progress_callback(5)
            if output_callback:
                output_callback("Starting system upgrade...\n")

            # Run apt upgrade
            proc = subprocess.Popen(
                ["pkexec", "apt-get", "upgrade", "-y"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            total_lines = 0
            for line in proc.stdout:
                total_lines += 1
                if output_callback:
                    output_callback(line)
                # Rough progress estimation
                if progress_callback and total_lines % 5 == 0:
                    progress = min(95, 5 + total_lines)
                    progress_callback(progress)

            proc.wait()

            if progress_callback:
                progress_callback(100)

            success = proc.returncode == 0
            if output_callback:
                if success:
                    output_callback("\n✓ Upgrade completed successfully!\n")
                else:
                    output_callback(f"\n✗ Upgrade failed (exit code: {proc.returncode})\n")

            return success

        except Exception as e:
            if output_callback:
                output_callback(f"ERROR: {str(e)}\n")
            return False
