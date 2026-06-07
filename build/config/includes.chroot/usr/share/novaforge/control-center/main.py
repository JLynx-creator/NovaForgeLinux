#!/usr/bin/env python3
"""
NovaForge Control Center — Main Entry Point
============================================
System management application for NovaForge Linux.
Provides dashboard, profile switching, driver management, and update center.
"""

import sys
import os

# Ensure we can find our modules
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow


def main():
    """Launch the NovaForge Control Center."""
    # High DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("NovaForge Control Center")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("NovaForge Linux")
    app.setWindowIcon(QIcon(os.path.join(APP_DIR, "assets", "icon.png")))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
