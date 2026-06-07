"""
NovaForge Control Center — Drivers Page
=========================================
GPU driver management interface.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.driver_manager import DriverManager


class DriversPage(QWidget):
    """GPU and driver management page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.driver_manager = DriverManager()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("🖥️  Driver Manager")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Manage GPU drivers and hardware acceleration")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # GPU Info Card
        gpu_frame = QFrame()
        gpu_frame.setStyleSheet("""
            QFrame { background-color: #1e1e2e; border: 1px solid #313244;
                     border-radius: 12px; padding: 20px; }
        """)
        gpu_layout = QVBoxLayout(gpu_frame)

        gpu_info = self.driver_manager.get_gpu_info()

        gpu_name_label = QLabel(f"Detected GPU: {gpu_info.get('name', 'Unknown')}")
        gpu_name_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        gpu_name_label.setStyleSheet("color: #00e5ff; border: none;")
        gpu_layout.addWidget(gpu_name_label)

        gpu_driver_label = QLabel(f"Current Driver: {gpu_info.get('driver', 'Unknown')}")
        gpu_driver_label.setFont(QFont("Inter", 12))
        gpu_driver_label.setStyleSheet("color: #cdd6f4; border: none;")
        gpu_layout.addWidget(gpu_driver_label)

        gpu_vendor_label = QLabel(f"Vendor: {gpu_info.get('vendor', 'Unknown')}")
        gpu_vendor_label.setFont(QFont("Inter", 12))
        gpu_vendor_label.setStyleSheet("color: #7f849c; border: none;")
        gpu_layout.addWidget(gpu_vendor_label)

        layout.addWidget(gpu_frame)

        # Action buttons
        layout.addSpacing(8)
        actions_title = QLabel("Quick Actions")
        actions_title.setFont(QFont("Inter", 16, QFont.DemiBold))
        actions_title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(actions_title)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_additional = QPushButton("  Open Additional Drivers")
        btn_additional.setMinimumHeight(44)
        btn_additional.setCursor(Qt.PointingHandCursor)
        btn_additional.clicked.connect(self._open_additional_drivers)
        btn_layout.addWidget(btn_additional)

        btn_nvidia = QPushButton("  Install NVIDIA Driver")
        btn_nvidia.setObjectName("primaryButton")
        btn_nvidia.setMinimumHeight(44)
        btn_nvidia.setCursor(Qt.PointingHandCursor)
        btn_nvidia.clicked.connect(self._install_nvidia)
        btn_layout.addWidget(btn_nvidia)

        layout.addLayout(btn_layout)

        # Info section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame { background-color: #1e1e2e; border: 1px solid #313244;
                     border-radius: 12px; padding: 16px; }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_text = QLabel(
            "💡 NovaForge Linux includes open-source Mesa drivers by default.\n"
            "For NVIDIA GPUs, proprietary drivers provide better gaming and CUDA performance.\n"
            "Use 'Install NVIDIA Driver' or 'Additional Drivers' to switch."
        )
        info_text.setFont(QFont("Inter", 11))
        info_text.setStyleSheet("color: #7f849c; border: none;")
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        layout.addWidget(info_frame)

        layout.addStretch()

    def _open_additional_drivers(self):
        """Open the Ubuntu Additional Drivers utility."""
        import subprocess
        try:
            subprocess.Popen(["software-properties-kde", "--open-tab=4"])
        except FileNotFoundError:
            try:
                subprocess.Popen(["software-properties-gtk", "--open-tab=4"])
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", "Additional Drivers utility not found.")

    def _install_nvidia(self):
        """Launch NVIDIA driver installation."""
        reply = QMessageBox.question(
            self, "Install NVIDIA Driver",
            "This will install the recommended NVIDIA proprietary driver.\n\n"
            "A reboot will be required. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.driver_manager.install_nvidia_recommended()
            if success:
                QMessageBox.information(
                    self, "Success",
                    "NVIDIA driver installation started.\n"
                    "Please reboot when complete."
                )
            else:
                QMessageBox.warning(
                    self, "Error",
                    "Failed to start installation. Try running with sudo."
                )
