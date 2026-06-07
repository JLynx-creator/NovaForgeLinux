"""
NovaForge Control Center — Dashboard Page
===========================================
System information overview with CPU, RAM, GPU, disk, and distro info.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from core.system_info import SystemInfo


class InfoCard(QFrame):
    """A card displaying a key-value pair with optional progress bar."""

    def __init__(self, title, value="", show_progress=False, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Inter", 11))
        self.title_label.setStyleSheet("color: #7f849c; border: none;")
        layout.addWidget(self.title_label)

        self.value_label = QLabel(str(value))
        self.value_label.setFont(QFont("Inter", 18, QFont.Bold))
        self.value_label.setStyleSheet("color: #00e5ff; border: none;")
        layout.addWidget(self.value_label)

        self.progress = None
        if show_progress:
            self.progress = QProgressBar()
            self.progress.setFixedHeight(8)
            self.progress.setTextVisible(False)
            layout.addWidget(self.progress)

    def set_value(self, value, progress=None):
        self.value_label.setText(str(value))
        if self.progress and progress is not None:
            self.progress.setValue(int(progress))


class DashboardPage(QWidget):
    """System dashboard showing real-time system information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sys_info = SystemInfo()
        self._setup_ui()
        self._start_updates()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel("📊  System Dashboard")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Real-time system overview")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # Cards grid
        grid = QGridLayout()
        grid.setSpacing(16)

        self.cpu_card = InfoCard("CPU Usage", "0%", show_progress=True)
        self.ram_card = InfoCard("RAM Usage", "0 / 0 GB", show_progress=True)
        self.disk_card = InfoCard("Disk Usage", "0 / 0 GB", show_progress=True)
        self.gpu_card = InfoCard("GPU", "Detecting...")

        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)

        layout.addLayout(grid)

        # System info section
        layout.addSpacing(8)
        info_title = QLabel("System Information")
        info_title.setFont(QFont("Inter", 16, QFont.DemiBold))
        info_title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(info_title)

        info_frame = QFrame()
        info_frame.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        info_layout = QGridLayout(info_frame)
        info_layout.setSpacing(12)

        static_info = self.sys_info.get_static_info()
        fields = [
            ("Distribution", static_info.get("distro", "NovaForge Linux")),
            ("Kernel", static_info.get("kernel", "Unknown")),
            ("Desktop", static_info.get("desktop", "KDE Plasma")),
            ("CPU Model", static_info.get("cpu_model", "Unknown")),
            ("Architecture", static_info.get("arch", "x86_64")),
            ("Hostname", static_info.get("hostname", "novaforge")),
        ]

        for i, (key, value) in enumerate(fields):
            row, col = divmod(i, 2)
            key_label = QLabel(key)
            key_label.setFont(QFont("Inter", 11))
            key_label.setStyleSheet("color: #7f849c; border: none;")

            val_label = QLabel(str(value))
            val_label.setFont(QFont("Inter", 11, QFont.DemiBold))
            val_label.setStyleSheet("color: #cdd6f4; border: none;")

            info_layout.addWidget(key_label, row, col * 2)
            info_layout.addWidget(val_label, row, col * 2 + 1)

        layout.addWidget(info_frame)
        layout.addStretch()

    def _start_updates(self):
        """Start periodic system info updates."""
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_stats)
        self.update_timer.start(2000)  # Update every 2 seconds
        self._update_stats()  # Initial update

    def _update_stats(self):
        """Fetch and display current system stats."""
        stats = self.sys_info.get_live_stats()

        self.cpu_card.set_value(
            f"{stats['cpu_percent']}%",
            stats['cpu_percent']
        )
        self.ram_card.set_value(
            f"{stats['ram_used_gb']:.1f} / {stats['ram_total_gb']:.1f} GB",
            stats['ram_percent']
        )
        self.disk_card.set_value(
            f"{stats['disk_used_gb']:.0f} / {stats['disk_total_gb']:.0f} GB",
            stats['disk_percent']
        )
        self.gpu_card.set_value(stats.get('gpu_name', 'N/A'))
