"""
NovaForge Control Center — Gaming Compatibility Page
======================================================
Manages Steam Proton-GE versions, upgrades, and downloads.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QFrame, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.proton_manager import ProtonManager, ProtonDownloadWorker


class GamingPage(QWidget):
    """Steam compatibility layers manager interface."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = ProtonManager()
        self.download_worker = None
        self.latest_release_url = None
        self.latest_release_name = None

        self._setup_ui()
        self._refresh_installed()
        self._check_for_updates()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("🎮  Gaming Optimization")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Manage Proton-GE compatibility layers for Steam games")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        # Main Workspace Split
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # Left Column: Installed compatibility layers
        left_layout = QVBoxLayout()
        installed_title = QLabel("Installed Compatibility Tools")
        installed_title.setFont(QFont("Inter", 14, QFont.DemiBold))
        installed_title.setStyleSheet("color: #cdd6f4;")
        left_layout.addWidget(installed_title)

        self.installed_list = QListWidget()
        self.installed_list.setStyleSheet("""
            QListWidget { background-color: #1e1e2e; border: 1px solid #313244;
                          border-radius: 12px; padding: 8px; color: #cdd6f4; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #313244; }
            QListWidget::item:selected { background-color: rgba(124, 58, 237, 0.15); color: #7c3aed; }
        """)
        left_layout.addWidget(self.installed_list)

        # Delete Action
        self.btn_delete = QPushButton("🗑️  Delete Selected Version")
        self.btn_delete.setObjectName("dangerButton")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(self._delete_selected)
        left_layout.addWidget(self.btn_delete)

        split_layout.addLayout(left_layout, 2)

        # Right Column: Update Check and Download
        right_layout = QVBoxLayout()
        update_title = QLabel("Updates & Downloads")
        update_title.setFont(QFont("Inter", 14, QFont.DemiBold))
        update_title.setStyleSheet("color: #cdd6f4;")
        right_layout.addWidget(update_title)

        update_frame = QFrame()
        update_frame.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        update_layout = QVBoxLayout(update_frame)

        self.latest_label = QLabel("Checking for updates...")
        self.latest_label.setFont(QFont("Inter", 11, QFont.DemiBold))
        self.latest_label.setStyleSheet("color: #cdd6f4; border: none;")
        self.latest_label.setWordWrap(True)
        update_layout.addWidget(self.latest_label)

        self.info_text = QLabel("Connect to the internet to check the latest releases of GloriousEggroll's Proton-GE.")
        self.info_text.setFont(QFont("Inter", 10))
        self.info_text.setStyleSheet("color: #7f849c; border: none;")
        self.info_text.setWordWrap(True)
        update_layout.addWidget(self.info_text)

        self.btn_download = QPushButton("⬇️  Install Latest Release")
        self.btn_download.setObjectName("primaryButton")
        self.btn_download.setEnabled(False)
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.clicked.connect(self._download_latest)
        update_layout.addWidget(self.btn_download)

        # Status and Progress bars
        self.status_lbl = QLabel("")
        self.status_lbl.setFont(QFont("Inter", 10))
        self.status_lbl.setStyleSheet("color: #00e5ff; border: none;")
        self.status_lbl.hide()
        update_layout.addWidget(self.status_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        update_layout.addWidget(self.progress_bar)

        right_layout.addWidget(update_frame)

        # Manual Check Button
        self.btn_check = QPushButton("🔄  Check for Updates")
        self.btn_check.setCursor(Qt.PointingHandCursor)
        self.btn_check.clicked.connect(self._check_for_updates)
        right_layout.addWidget(self.btn_check)

        right_layout.addStretch()
        split_layout.addLayout(right_layout, 1)

        layout.addLayout(split_layout)

    def _refresh_installed(self):
        """Reload installed Proton-GE versions list."""
        self.installed_list.clear()
        versions = self.manager.get_installed_versions()
        if not versions:
            self.installed_list.addItem("No custom compatibility layers found.")
            self.btn_delete.setEnabled(False)
        else:
            self.btn_delete.setEnabled(True)
            for v in versions:
                self.installed_list.addItem(v)

    def _check_for_updates(self):
        """Query GitHub API for latest Proton version."""
        self.latest_label.setText("Querying GitHub releases...")
        self.latest_label.setStyleSheet("color: #cdd6f4; border: none;")
        self.btn_check.setEnabled(False)
        
        # Simple query directly
        import urllib.request
        from PyQt5.QtCore import QTimer
        # Use simple timer to call check in background
        QTimer.singleShot(100, self._async_check)

    def _async_check(self):
        res = self.manager.check_latest_release()
        self.btn_check.setEnabled(True)
        if res.get("success"):
            self.latest_release_url = res["download_url"]
            self.latest_release_name = res["version"]
            
            # Verify if already installed
            installed = self.manager.get_installed_versions()
            is_installed = self.latest_release_name in installed
            
            self.latest_label.setText(f"Latest Version: {self.latest_release_name}")
            if is_installed:
                self.latest_label.setStyleSheet("color: #a6e3a1; border: none;")
                self.info_text.setText("This version is already installed on your system.")
                self.btn_download.setEnabled(False)
            else:
                self.latest_label.setStyleSheet("color: #00e5ff; border: none;")
                self.info_text.setText("A newer version is available. Click install to integrate it into Steam.")
                self.btn_download.setEnabled(True)
        else:
            self.latest_label.setText("Failed to check for updates")
            self.latest_label.setStyleSheet("color: #f38ba8; border: none;")
            self.info_text.setText(f"Error: {res.get('error')}")
            self.btn_download.setEnabled(False)

    def _download_latest(self):
        """Trigger background download of tarball."""
        if not self.latest_release_url or not self.latest_release_name:
            return

        self.btn_download.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_check.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.status_lbl.show()

        self.download_worker = ProtonDownloadWorker(self.latest_release_url, self.latest_release_name)
        self.download_worker.progress.connect(self.progress_bar.setValue)
        self.download_worker.status.connect(self.status_lbl.setText)
        self.download_worker.finished.connect(self._on_download_finished)
        self.download_worker.start()

    def _on_download_finished(self, success, msg):
        self.progress_bar.hide()
        self.status_lbl.hide()
        self.btn_check.setEnabled(True)
        self._refresh_installed()

        if success:
            QMessageBox.information(self, "Download Complete", msg)
            self._check_for_updates() # Refresh update check state
        else:
            QMessageBox.critical(self, "Download Error", f"Failed to download and extract GE-Proton:\n{msg}")
            self.btn_download.setEnabled(True)

    def _delete_selected(self):
        """Remove selected version directory."""
        selected_item = self.installed_list.currentItem()
        if not selected_item:
            return
            
        version_name = selected_item.text()
        if version_name == "No custom compatibility layers found.":
            return

        confirm = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete {version_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            if self.manager.delete_version(version_name):
                QMessageBox.information(self, "Deleted", f"Successfully deleted {version_name}.")
                self._refresh_installed()
                self._check_for_updates() # Refresh update check state
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete directory for {version_name}.")
