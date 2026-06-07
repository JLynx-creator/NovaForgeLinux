"""
NovaForge Control Center — Dashboard Page
===========================================
System information overview with CPU, RAM, GPU, disk, and distro info.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QProgressBar, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QPushButton
)
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QFont, QPainter, QPen, QColor, QPainterPath, QLinearGradient

from core.system_info import SystemInfo


class UsageGraph(QWidget):
    """Custom real-time sparkline graph for CPU/RAM usage."""

    def __init__(self, color_hex="#00e5ff", parent=None):
        super().__init__(parent)
        self.color = QColor(color_hex)
        self.history = [0.0] * 30  # Keep 30 data points
        self.setMinimumHeight(50)
        self.setMaximumHeight(80)

    def add_value(self, val):
        self.history.pop(0)
        self.history.append(float(val))
        self.update()  # Trigger repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Draw background and grid lines
        painter.fillRect(0, 0, w, h, QColor("#1e1e2e"))
        
        grid_pen = QPen(QColor("#313244"), 1, Qt.DashLine)
        painter.setPen(grid_pen)
        # Draw 2 horizontal grid lines
        for y_pct in [0.33, 0.66]:
            painter.drawLine(0, int(h * y_pct), w, int(h * y_pct))
            
        # If we have history, draw the graph line and fill
        if len(self.history) < 2:
            return
            
        # Draw graph path
        path = QPainterPath()
        step = w / (len(self.history) - 1)
        
        def get_pt(idx, val):
            x = idx * step
            y = h - (val / 100.0) * (h - 8) - 4
            return QPointF(x, y)
            
        first_pt = get_pt(0, self.history[0])
        path.moveTo(first_pt)
        for i in range(1, len(self.history)):
            pt = get_pt(i, self.history[i])
            path.lineTo(pt)
            
        # Fill path (gradient underneath)
        fill_path = QPainterPath(path)
        fill_path.lineTo(w, h)
        fill_path.lineTo(0, h)
        fill_path.closeSubpath()
        
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0.0, QColor(self.color.red(), self.color.green(), self.color.blue(), 60))
        gradient.setColorAt(1.0, QColor(self.color.red(), self.color.green(), self.color.blue(), 0))
        painter.fillPath(fill_path, gradient)
        
        # Draw main line
        line_pen = QPen(self.color, 2)
        painter.setPen(line_pen)
        painter.drawPath(path)


class InfoCard(QFrame):
    """A card displaying a key-value pair with optional progress bar and graph."""

    def __init__(self, title, value="", show_progress=False, show_graph=False, graph_color="#00e5ff", parent=None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        self.setMinimumHeight(150 if show_graph else 100)

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
            self.progress.setFixedHeight(6)
            self.progress.setTextVisible(False)
            layout.addWidget(self.progress)

        self.graph = None
        if show_graph:
            self.graph = UsageGraph(graph_color)
            layout.addWidget(self.graph)

    def set_value(self, value, progress=None, graph_val=None):
        self.value_label.setText(str(value))
        if self.progress and progress is not None:
            self.progress.setValue(int(progress))
        if self.graph and graph_val is not None:
            self.graph.add_value(graph_val)


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

        self.cpu_card = InfoCard("CPU Usage", "0%", show_progress=True, show_graph=True, graph_color="#00e5ff")
        self.ram_card = InfoCard("RAM Usage", "0 / 0 GB", show_progress=True, show_graph=True, graph_color="#7c3aed")
        self.disk_card = InfoCard("Disk Usage", "0 / 0 GB", show_progress=True)
        self.gpu_card = InfoCard("GPU", "Detecting...")

        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 1, 0)
        grid.addWidget(self.gpu_card, 1, 1)

        layout.addLayout(grid)

        # Split pane at the bottom
        bottom_split = QHBoxLayout()
        bottom_split.setSpacing(16)

        # Left Column: Static System Info
        info_wrapper = QVBoxLayout()
        info_title = QLabel("System Information")
        info_title.setFont(QFont("Inter", 14, QFont.DemiBold))
        info_title.setStyleSheet("color: #cdd6f4;")
        info_wrapper.addWidget(info_title)

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

        info_wrapper.addWidget(info_frame)
        bottom_split.addLayout(info_wrapper, 1)

        # Right Column: Top Running Processes
        proc_wrapper = QVBoxLayout()
        proc_title = QLabel("Top Running Processes")
        proc_title.setFont(QFont("Inter", 14, QFont.DemiBold))
        proc_title.setStyleSheet("color: #cdd6f4;")
        proc_wrapper.addWidget(proc_title)

        proc_frame = QFrame()
        proc_frame.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 12px; }")
        proc_layout = QVBoxLayout(proc_frame)
        proc_layout.setContentsMargins(8, 8, 8, 8)

        self.proc_table = QTableWidget()
        self.proc_table.setColumnCount(4)
        self.proc_table.setHorizontalHeaderLabels(["Name", "CPU %", "RAM MB", "Action"])
        self.proc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.proc_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.proc_table.verticalHeader().setVisible(False)
        self.proc_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.proc_table.setStyleSheet("QTableWidget { border: none; background: transparent; }")
        proc_layout.addWidget(self.proc_table)

        proc_wrapper.addWidget(proc_frame)
        bottom_split.addLayout(proc_wrapper, 1)

        layout.addLayout(bottom_split)
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
            stats['cpu_percent'],
            stats['cpu_percent']
        )
        self.ram_card.set_value(
            f"{stats['ram_used_gb']:.1f} / {stats['ram_total_gb']:.1f} GB",
            stats['ram_percent'],
            stats['ram_percent']
        )
        self.disk_card.set_value(
            f"{stats['disk_used_gb']:.0f} / {stats['disk_total_gb']:.0f} GB",
            stats['disk_percent']
        )
        self.gpu_card.set_value(stats.get('gpu_name', 'N/A'))

        # Update process list table
        procs = self.sys_info.get_top_processes(5)
        self.proc_table.setRowCount(len(procs))
        for i, proc in enumerate(procs):
            self.proc_table.setItem(i, 0, QTableWidgetItem(proc['name']))
            self.proc_table.setItem(i, 1, QTableWidgetItem(f"{proc['cpu']:.1f}%"))
            self.proc_table.setItem(i, 2, QTableWidgetItem(f"{proc['memory']:.1f} MB"))
            
            kill_btn = QPushButton("Kill")
            kill_btn.setObjectName("dangerButton")
            kill_btn.setStyleSheet("QPushButton { padding: 2px 8px; font-size: 11px; }")
            kill_btn.clicked.connect(lambda checked, pid=proc['pid']: self._kill_process(pid))
            self.proc_table.setCellWidget(i, 3, kill_btn)

    def _kill_process(self, pid):
        """Terminate a process and refresh stats."""
        if self.sys_info.kill_process(pid):
            self._update_stats()
        else:
            QMessageBox.warning(self, "Action Failed", f"Could not terminate process with PID {pid}.")
