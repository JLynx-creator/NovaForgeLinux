// ============================================================
// NovaForge Linux — KDE Plasma Desktop Layout
// ============================================================
// Creates a hybrid layout:
//   - Top Panel: Global menu, spacer, system tray, clock
//   - Bottom Panel: Floating dock with app launcher + icon tasks
// ============================================================

// ── Top Panel (macOS-style menu bar) ──────────────────────
var topPanel = new Panel;
topPanel.location = "top";
topPanel.height = Math.round(gridUnit * 1.6);
topPanel.alignment = "fill";

// Application launcher (compact)
var kickoff = topPanel.addWidget("org.kde.plasma.kickoff");
kickoff.currentConfigGroup = ["General"];
kickoff.writeConfig("icon", "start-here-kde-plasma");
kickoff.writeConfig("favoriteSystemActions", "logout,reboot,shutdown");
kickoff.currentConfigGroup = ["Shortcuts"];
kickoff.writeConfig("global", "Meta+F1");

// Global application menu
topPanel.addWidget("org.kde.plasma.appmenu");

// Flexible spacer
topPanel.addWidget("org.kde.plasma.panelspacer");

// System tray
var systray = topPanel.addWidget("org.kde.plasma.systemtray");

// Digital clock
var clock = topPanel.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", true);
clock.writeConfig("dateFormat", "shortDate");
clock.writeConfig("use24hFormat", 2);

// ── Bottom Panel (Windows/macOS-style floating dock) ──────
var bottomPanel = new Panel;
bottomPanel.location = "bottom";
bottomPanel.height = Math.round(gridUnit * 3.2);
bottomPanel.alignment = "center";
bottomPanel.hiding = "dodgewindows";
bottomPanel.floating = 1;

// Icon-only task manager (dock style)
var tasks = bottomPanel.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", [
    "applications:systemsettings.desktop",
    "applications:org.kde.dolphin.desktop",
    "applications:org.kde.konsole.desktop",
    "applications:org.kde.kate.desktop",
    "preferred://browser",
    "applications:novaforge-control-center.desktop"
]);
tasks.writeConfig("maxStripes", 1);
tasks.writeConfig("showOnlyCurrentDesktop", false);
tasks.writeConfig("showOnlyCurrentActivity", false);

// Separator
bottomPanel.addWidget("org.kde.plasma.marginsseparator");

// Trash
bottomPanel.addWidget("org.kde.plasma.trash");

// ── Virtual Desktops ──────────────────────────────────────
// Configure 4 virtual desktops in a 2x2 grid
var desktopsArray = [];
for (var i = 0; i < 4; i++) {
    desktopsArray.push({
        "name": "Desktop " + (i + 1),
        "id": "desktop-" + (i + 1)
    });
}
