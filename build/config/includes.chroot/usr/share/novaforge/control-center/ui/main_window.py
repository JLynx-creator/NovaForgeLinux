"""
NovaForge Control Center — Main Window
========================================
Sidebar navigation with stacked widget pages.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

from ui.styles import STYLESHEET
from ui.dashboard import DashboardPage
from ui.profiles import ProfilesPage
from ui.drivers import DriversPage
from ui.ai_models import AIModelsPage
from ui.gaming import GamingPage
from ui.updates import UpdatesPage


class SidebarButton(QPushButton):
    """Custom sidebar navigation button."""

    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}  {text}")
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Inter", 11))


class MainWindow(QMainWindow):
    """NovaForge Control Center main window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NovaForge Control Center")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)
        self.setStyleSheet(STYLESHEET)

        self._setup_ui()

    def _setup_ui(self):
        """Build the UI layout."""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Sidebar ───────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(4)

        # Logo / Title
        title = QLabel("🔥 NovaForge")
        title.setObjectName("sidebarTitle")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)

        subtitle = QLabel("Control Center")
        subtitle.setObjectName("sidebarSubtitle")
        subtitle.setFont(QFont("Inter", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(24)

        # Navigation buttons
        self.nav_buttons = []
        pages = [
            ("Dashboard", "📊"),
            ("Profiles", "⚡"),
            ("Drivers", "🖥️"),
            ("AI Workspace", "🤖"),
            ("Gaming Tools", "🎮"),
            ("Updates", "🔄"),
        ]

        for text, icon in pages:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, t=text: self._navigate(t))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Version label
        version_label = QLabel("v1.0.0")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Inter", 9))
        sidebar_layout.addWidget(version_label)

        layout.addWidget(sidebar)

        # ── Content Area ──────────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setObjectName("contentArea")

        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(ProfilesPage())
        self.stack.addWidget(DriversPage())
        self.stack.addWidget(AIModelsPage())
        self.stack.addWidget(GamingPage())
        self.stack.addWidget(UpdatesPage())

        layout.addWidget(self.stack)

        # Select first page
        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    def _navigate(self, page_name):
        """Switch to the selected page."""
        pages = ["Dashboard", "Profiles", "Drivers", "AI Workspace", "Gaming Tools", "Updates"]
        index = pages.index(page_name) if page_name in pages else 0

        self.stack.setCurrentIndex(index)

        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
