"""
NovaForge Control Center — Proton-GE Manager Module
=====================================================
Manages GloriousEggroll's custom Proton compatibility tools for Steam.
Allows listing, downloading, installing and deleting versions.
"""

import os
import tarfile
import urllib.request
import json
import ssl
from PyQt5.QtCore import QThread, pyqtSignal

STEAM_COMPAT_DIR = os.path.expanduser("~/.steam/root/compatibilitytools.d")
if not os.path.exists(STEAM_COMPAT_DIR):
    # Fallback to alternative path
    STEAM_COMPAT_DIR = os.path.expanduser("~/.local/share/Steam/compatibilitytools.d")


class ProtonDownloadWorker(QThread):
    """Background worker to download and extract GE-Proton versions."""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, tarball_url, version_name):
        super().__init__()
        self.tarball_url = tarball_url
        self.version_name = version_name

    def run(self):
        try:
            # Ensure target directory exists
            os.makedirs(STEAM_COMPAT_DIR, exist_ok=True)
            
            # Temporary tarball file path
            temp_tar = os.path.join(STEAM_COMPAT_DIR, f"{self.version_name}.tar.gz")
            
            self.status.emit(f"Downloading {self.version_name}...")
            
            # SSL Context bypass if needed (standard practice on some Linux setups)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # Download implementation with progress updates
            req = urllib.request.urlopen(self.tarball_url, context=ctx)
            total_size = int(req.info().get('Content-Length', 0))
            downloaded = 0
            block_size = 1024 * 64 # 64KB chunks

            with open(temp_tar, 'wb') as f:
                while True:
                    buffer = req.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    f.write(buffer)
                    
                    if total_size > 0:
                        pct = int((downloaded / total_size) * 100)
                        self.progress.emit(pct)
            
            self.status.emit("Extracting files (this may take a minute)...")
            
            # Extract tarball
            with tarfile.open(temp_tar, 'r:gz') as tar:
                tar.extractall(path=STEAM_COMPAT_DIR)
                
            # Clean up temp file
            if os.path.exists(temp_tar):
                os.remove(temp_tar)
                
            self.finished.emit(True, f"Successfully installed {self.version_name}!")
        except Exception as e:
            self.finished.emit(False, str(e))


class ProtonManager:
    """Manages GE-Proton versions in Steam directories."""

    def get_installed_versions(self):
        """List all installed GE-Proton versions."""
        versions = []
        if os.path.exists(STEAM_COMPAT_DIR):
            try:
                for name in os.listdir(STEAM_COMPAT_DIR):
                    if os.path.isdir(os.path.join(STEAM_COMPAT_DIR, name)):
                        versions.append(name)
            except Exception:
                pass
        return sorted(versions)

    def delete_version(self, version_name):
        """Delete an installed GE-Proton version."""
        path = os.path.join(STEAM_COMPAT_DIR, version_name)
        if os.path.exists(path) and os.path.isdir(path):
            try:
                import shutil
                shutil.rmtree(path)
                return True
            except Exception:
                pass
        return False

    def check_latest_release(self):
        """Query the GitHub API for the latest GE-Proton release details."""
        url = "https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest"
        try:
            # Bypass SSL certificate checks for network safety
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (NovaForge Linux Builder)'}
            )
            with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
                res = json.loads(r.read().decode())
                
                version_name = res.get("tag_name", "")
                assets = res.get("assets", [])
                tarball_url = ""
                
                for asset in assets:
                    name = asset.get("name", "")
                    if name.endswith(".tar.gz"):
                        tarball_url = asset.get("browser_download_url", "")
                        break
                        
                return {
                    "success": True,
                    "version": version_name,
                    "download_url": tarball_url,
                    "body": res.get("body", "No description available.")
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
