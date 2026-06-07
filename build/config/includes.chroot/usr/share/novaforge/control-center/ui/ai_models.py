"""
NovaForge Control Center — AI Models Page
=========================================
Manage local AI models and check Ollama service status.
"""

import urllib.request
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QFrame, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont


class OllamaWorker(QThread):
    """Background thread to communicate with local Ollama API."""
    output = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, list, str)

    def __init__(self, action="list", model_name=None):
        super().__init__()
        self.action = action
        self.model_name = model_name

    def run(self):
        if self.action == "list":
            try:
                req = urllib.request.Request("http://localhost:11434/api/tags")
                with urllib.request.urlopen(req, timeout=5) as response:
                    res = json.loads(response.read().decode())
                    models = [m['name'] for m in res.get('models', [])]
                    self.finished.emit(True, models, "")
            except Exception as e:
                self.finished.emit(False, [], str(e))
        
        elif self.action == "pull" and self.model_name:
            try:
                self.output.emit(f"Downloading model '{self.model_name}'...\n")
                url = "http://localhost:11434/api/pull"
                data = json.dumps({"name": self.model_name, "stream": False}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                
                with urllib.request.urlopen(req, timeout=600) as response:
                    res = json.loads(response.read().decode())
                    if res.get('status') == 'success':
                        self.finished.emit(True, [], f"Model '{self.model_name}' downloaded successfully!")
                    else:
                        self.finished.emit(False, [], f"Download response: {res.get('status')}")
            except Exception as e:
                self.finished.emit(False, [], f"Failed to download model: {str(e)}")


class AIModelsPage(QWidget):
    """AI models management interface."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._setup_ui()
        self._refresh_models()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("🤖  AI Workspace")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        title.setStyleSheet("color: #cdd6f4;")
        layout.addWidget(title)

        subtitle = QLabel("Manage local LLMs (Large Language Models)")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #7f849c;")
        layout.addWidget(subtitle)

        # Service Status Card
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame { background-color: #1e1e2e; border: 1px solid #313244;
                     border-radius: 12px; padding: 16px; }
        """)
        status_layout = QHBoxLayout(status_frame)
        self.status_label = QLabel("Checking Ollama status...")
        self.status_label.setFont(QFont("Inter", 12))
        self.status_label.setStyleSheet("color: #cdd6f4; border: none;")
        status_layout.addWidget(self.status_label)

        self.btn_refresh = QPushButton(" 🔄 Refresh")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self._refresh_models)
        status_layout.addWidget(self.btn_refresh)
        layout.addWidget(status_frame)

        # Main Workspace Split
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # Left Column: Models list
        left_layout = QVBoxLayout()
        models_label = QLabel("Installed Models")
        models_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        models_label.setStyleSheet("color: #cdd6f4;")
        left_layout.addWidget(models_label)

        self.models_list = QListWidget()
        self.models_list.setStyleSheet("""
            QListWidget { background-color: #1e1e2e; border: 1px solid #313244;
                          border-radius: 12px; padding: 8px; color: #cdd6f4; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #313244; }
            QListWidget::item:selected { background-color: rgba(0, 229, 255, 0.15); color: #00e5ff; }
        """)
        left_layout.addWidget(self.models_list)
        split_layout.addLayout(left_layout, 2)

        # Right Column: Actions and Download
        right_layout = QVBoxLayout()
        download_label = QLabel("Download New Model")
        download_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        download_label.setStyleSheet("color: #cdd6f4;")
        right_layout.addWidget(download_label)

        down_frame = QFrame()
        down_frame.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        down_layout = QVBoxLayout(down_frame)

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Enter model name (e.g., llama3, phi3, mistral)...")
        self.model_input.setStyleSheet("QLineEdit { background-color: #11111b; border: 1px solid #313244; border-radius: 8px; padding: 8px; color: #cdd6f4; }")
        down_layout.addWidget(self.model_input)

        self.btn_download = QPushButton("  Download Model")
        self.btn_download.setObjectName("primaryButton")
        self.btn_download.setMinimumHeight(36)
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.clicked.connect(self._download_model)
        down_layout.addWidget(self.btn_download)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        down_layout.addWidget(self.progress_bar)

        right_layout.addWidget(down_frame)

        # WebUI Card
        webui_label = QLabel("Web Chat Interface")
        webui_label.setFont(QFont("Inter", 14, QFont.DemiBold))
        webui_label.setStyleSheet("color: #cdd6f4; margin-top: 12px;")
        right_layout.addWidget(webui_label)

        webui_frame = QFrame()
        webui_frame.setStyleSheet("QFrame { background-color: #1e1e2e; border: 1px solid #313244; border-radius: 12px; padding: 16px; }")
        webui_layout = QVBoxLayout(webui_frame)

        self.btn_webui = QPushButton("🌐  Launch Open WebUI")
        self.btn_webui.setObjectName("primaryButton")
        self.btn_webui.setMinimumHeight(36)
        self.btn_webui.setCursor(Qt.PointingHandCursor)
        self.btn_webui.clicked.connect(self._launch_webui)
        webui_layout.addWidget(self.btn_webui)

        right_layout.addWidget(webui_frame)
        right_layout.addStretch()
        split_layout.addLayout(right_layout, 1)

        layout.addLayout(split_layout)

    def _refresh_models(self):
        self.status_label.setText("Checking Ollama status...")
        self.status_label.setStyleSheet("color: #cdd6f4; border: none;")
        self.models_list.clear()

        self.worker = OllamaWorker("list")
        self.worker.finished.connect(self._on_list_finished)
        self.worker.start()

    def _on_list_finished(self, success, models, err_msg):
        if success:
            self.status_label.setText("🟢 Ollama Local Service is running")
            self.status_label.setStyleSheet("color: #a6e3a1; border: none;")
            for m in models:
                self.models_list.addItem(m)
        else:
            self.status_label.setText("🔴 Ollama Service offline (Make sure Ollama is started)")
            self.status_label.setStyleSheet("color: #f38ba8; border: none;")

    def _download_model(self):
        model_name = self.model_input.text().strip()
        if not model_name:
            QMessageBox.warning(self, "Input Error", "Please enter a model name.")
            return

        self.btn_download.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0) # Pulsing progress indication

        self.worker = OllamaWorker("pull", model_name)
        self.worker.finished.connect(self._on_pull_finished)
        self.worker.start()

    def _on_pull_finished(self, success, models, msg):
        self.btn_download.setEnabled(True)
        self.progress_bar.hide()
        self.model_input.clear()
        
        if success:
            QMessageBox.information(self, "Download Complete", msg)
            self._refresh_models()
        else:
            QMessageBox.critical(self, "Download Error", msg)

    def _launch_webui(self):
        import subprocess
        try:
            subprocess.Popen(["/usr/bin/novaforge-openwebui"])
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Could not launch WebUI: {str(e)}")
