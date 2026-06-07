"""
NovaForge Control Center — Qt Stylesheet
==========================================
Dark theme matching the NovaForge color palette.
"""

STYLESHEET = """
/* ── Global ─────────────────────────────────────────── */
QWidget {
    background-color: #11111b;
    color: #cdd6f4;
    font-family: "Inter", "Noto Sans", sans-serif;
    font-size: 13px;
}

/* ── Sidebar ────────────────────────────────────────── */
QFrame#sidebar {
    background-color: #0a0a1a;
    border-right: 1px solid #313244;
}

QLabel#sidebarTitle {
    color: #00e5ff;
    padding: 4px;
}

QLabel#sidebarSubtitle {
    color: #7f849c;
    padding-bottom: 8px;
}

QLabel#versionLabel {
    color: #585b70;
}

/* ── Sidebar Buttons ────────────────────────────────── */
SidebarButton {
    background-color: transparent;
    color: #7f849c;
    border: none;
    border-radius: 10px;
    text-align: left;
    padding: 8px 16px;
}

SidebarButton:hover {
    background-color: #1e1e2e;
    color: #cdd6f4;
}

SidebarButton:checked {
    background-color: rgba(0, 229, 255, 0.12);
    color: #00e5ff;
    border-left: 3px solid #00e5ff;
}

/* ── Content Area ───────────────────────────────────── */
QStackedWidget#contentArea {
    background-color: #11111b;
}

/* ── Cards ──────────────────────────────────────────── */
QFrame.card {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 12px;
    padding: 16px;
}

QFrame.card:hover {
    border-color: rgba(0, 229, 255, 0.3);
}

/* ── Section Title ──────────────────────────────────── */
QLabel.sectionTitle {
    color: #cdd6f4;
    font-size: 20px;
    font-weight: 600;
    padding: 8px 0;
}

QLabel.sectionSubtitle {
    color: #7f849c;
    font-size: 13px;
    padding-bottom: 16px;
}

/* ── Info Labels ────────────────────────────────────── */
QLabel.infoKey {
    color: #7f849c;
    font-size: 12px;
}

QLabel.infoValue {
    color: #cdd6f4;
    font-size: 14px;
    font-weight: 500;
}

QLabel.accentValue {
    color: #00e5ff;
    font-size: 14px;
    font-weight: 600;
}

/* ── Buttons ────────────────────────────────────────── */
QPushButton {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #313244;
    border-color: #00e5ff;
}

QPushButton:pressed {
    background-color: #45475a;
}

QPushButton#primaryButton {
    background-color: #00e5ff;
    color: #11111b;
    border: none;
    font-weight: 600;
}

QPushButton#primaryButton:hover {
    background-color: #33ebff;
}

QPushButton#dangerButton {
    border-color: #f38ba8;
    color: #f38ba8;
}

QPushButton#dangerButton:hover {
    background-color: rgba(243, 139, 168, 0.15);
}

/* ── Profile Cards ──────────────────────────────────── */
QPushButton.profileCard {
    background-color: #1e1e2e;
    border: 2px solid #313244;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    min-height: 120px;
}

QPushButton.profileCard:hover {
    border-color: #00e5ff;
    background-color: rgba(0, 229, 255, 0.05);
}

QPushButton.profileCard:checked {
    border-color: #00e5ff;
    background-color: rgba(0, 229, 255, 0.10);
}

/* ── Progress Bar ───────────────────────────────────── */
QProgressBar {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    border-radius: 6px;
    height: 12px;
    text-align: center;
    color: #cdd6f4;
    font-size: 10px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00e5ff, stop:1 #7c3aed);
    border-radius: 5px;
}

/* ── Scroll Area ────────────────────────────────────── */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #11111b;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #313244;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #45475a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ── Text Edit / Output ─────────────────────────────── */
QTextEdit {
    background-color: #0a0a1a;
    color: #a6e3a1;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 8px;
    font-family: "JetBrains Mono", monospace;
    font-size: 12px;
}
"""
