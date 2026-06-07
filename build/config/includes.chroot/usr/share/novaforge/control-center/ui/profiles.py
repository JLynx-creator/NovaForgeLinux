"""
NovaForge Control Center — Profiles Page
==========================================
Switch between Gaming, Development, and AI performance profiles.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from core.profile_manager import ProfileManager


class ProfileCard(QPushButton):
    """Clickable profile card with icon, name, and description."""

    def __init__(self, icon, name, description, features, parent=None):
        super().__init__(parent)
        self.profile_name = name.lower()
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(240, 200)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1e1e2e;
                border: 2px solid #313244;
                border-radius: 16px;
                padding: 20px;
                text-align: left;
            }
            QPushButton:hover {
                border-color: #00e5ff;
                background-color: rgba(0, 229, 255, 0.05);
            }
            QPushButton:checked {
                border-color: #00e5ff;
                background-color: rgba(0, 229, 255, 0.10);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Inter", 32))
        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label)

        name_label = QLabel(name)
        name_label.setFont(QFont("Inter", 16, QFont.Bold))
        name_label.setStyleSheet("color: #cdd6f4; border: none; background: transparent;")
        layout.addWidget(name_label)

        desc_label = QLabel(description)
        desc_label.setFont(QFont("Inter", 11))
        desc_label.setStyleSheet("color: #7f849c; border: none; background: transparent;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        for feat in features:
            feat_label = QLabel(f"  • {feat}")
            feat_label.setFont(QFont("Inter", 10))
            feat_label.setStyleSheet("color: #a6e3a1; border: none; background: transparent;")
            layout.addWidget(feat_label)


class ProfilesPage(QWidget):
    """Performance profile management page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_manager = ProfileManager()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("⚡  Performance Profiles")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Optimize your system for different workloads")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        # Current profile indicator
        current = self.profile_manager.get_current_profile()
        self.status_label = QLabel(f"Current Profile: {current.title()}")
        self.status_label.setFont(QFont("Inter", 13, QFont.DemiBold))
        self.status_label.setStyleSheet("color: #00e5ff; padding: 8px 0;")
        layout.addWidget(self.status_label)

        layout.addSpacing(8)

        # Profile cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        self.gaming_card = ProfileCard(
            "🎮", "Gaming",
            "Maximum performance for games",
            ["CPU: Performance governor", "Swappiness: 10", "GameMode active"]
        )
        self.dev_card = ProfileCard(
            "💻", "Development",
            "Balanced for coding workflows",
            ["CPU: Powersave governor", "Swappiness: 60", "Docker enabled"]
        )
        self.ai_card = ProfileCard(
            "🤖", "AI",
            "Optimized for ML training",
            ["CPU: Performance governor", "Swappiness: 10", "GPU compute priority"]
        )

        # Set current active
        profile_cards = {
            "gaming": self.gaming_card,
            "development": self.dev_card,
            "ai": self.ai_card
        }
        if current in profile_cards:
            profile_cards[current].setChecked(True)

        self.gaming_card.clicked.connect(lambda: self._switch_profile("gaming"))
        self.dev_card.clicked.connect(lambda: self._switch_profile("development"))
        self.ai_card.clicked.connect(lambda: self._switch_profile("ai"))

        cards_layout.addWidget(self.gaming_card)
        cards_layout.addWidget(self.dev_card)
        cards_layout.addWidget(self.ai_card)

        layout.addLayout(cards_layout)
        layout.addStretch()

    def _switch_profile(self, profile):
        """Switch to the selected profile."""
        reply = QMessageBox.question(
            self, "Switch Profile",
            f"Switch to {profile.title()} profile?\n\n"
            "This will change CPU governor, memory settings, and services.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.profile_manager.switch_profile(profile)
            if success:
                self.status_label.setText(f"Current Profile: {profile.title()}")
                # Update card states
                self.gaming_card.setChecked(profile == "gaming")
                self.dev_card.setChecked(profile == "development")
                self.ai_card.setChecked(profile == "ai")
                QMessageBox.information(
                    self, "Profile Switched",
                    f"Successfully switched to {profile.title()} profile!"
                )
            else:
                QMessageBox.warning(
                    self, "Error",
                    "Failed to switch profile. Are you running as administrator?"
                )
