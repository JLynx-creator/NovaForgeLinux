"""
NovaForge Control Center — Updates Page
=========================================
Graphical apt update/upgrade interface.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QProgressBar, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from core.update_manager import UpdateManager


class UpdateWorker(QThread):
    """Background thread for running apt operations."""
    output = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, action="check"):
        super().__init__()
        self.action = action
        self.manager = UpdateManager()

    def run(self):
        if self.action == "check":
            self.output.emit("Checking for updates...\n")
            updates = self.manager.check_updates(
                progress_callback=self.progress.emit,
                output_callback=self.output.emit
            )
            self.finished.emit(True, f"Found {updates} available updates.")
        elif self.action == "upgrade":
            self.output.emit("Upgrading system packages...\n")
            success = self.manager.upgrade(
                progress_callback=self.progress.emit,
                output_callback=self.output.emit
            )
            if success:
                self.finished.emit(True, "System upgraded successfully!")
            else:
                self.finished.emit(False, "Upgrade failed. Check output for details.")


class UpdatesPage(QWidget):
    """System update management page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("🔄  System Updates")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Keep your system up to date")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        # Status card
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame { background-color: #1e1e2e; border: 1px solid #313244;
                     border-radius: 12px; padding: 16px; }
        """)
        status_layout = QVBoxLayout(status_frame)

        self.status_label = QLabel("Click 'Check Updates' to scan for available updates")
        self.status_label.setFont(QFont("Inter", 13))
        self.status_label.setStyleSheet("color: #cdd6f4; border: none;")
        status_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        status_layout.addWidget(self.progress_bar)

        layout.addWidget(status_frame)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.check_btn = QPushButton("  Check for Updates")
        self.check_btn.setMinimumHeight(44)
        self.check_btn.setCursor(Qt.PointingHandCursor)
        self.check_btn.clicked.connect(self._check_updates)
        btn_layout.addWidget(self.check_btn)

        self.upgrade_btn = QPushButton("  Upgrade System")
        self.upgrade_btn.setObjectName("primaryButton")
        self.upgrade_btn.setMinimumHeight(44)
        self.upgrade_btn.setCursor(Qt.PointingHandCursor)
        self.upgrade_btn.clicked.connect(self._upgrade_system)
        btn_layout.addWidget(self.upgrade_btn)

        layout.addLayout(btn_layout)

        # Output log
        output_label = QLabel("Output Log")
        output_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        output_label.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(200)
        self.output_text.setPlaceholderText("Update output will appear here...")
        layout.addWidget(self.output_text)

    def _check_updates(self):
        """Run apt update to check for available updates."""
        self._run_action("check")

    def _upgrade_system(self):
        """Run apt upgrade to update all packages."""
        self._run_action("upgrade")

    def _run_action(self, action):
        if self.worker and self.worker.isRunning():
            return

        self.output_text.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.check_btn.setEnabled(False)
        self.upgrade_btn.setEnabled(False)

        self.worker = UpdateWorker(action)
        self.worker.output.connect(self._append_output)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _append_output(self, text):
        self.output_text.append(text.strip())

    def _on_finished(self, success, message):
        color = "#a6e3a1" if success else "#f38ba8"
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; border: none;")
        self.progress_bar.setValue(100 if success else 0)
        self.check_btn.setEnabled(True)
        self.upgrade_btn.setEnabled(True)
