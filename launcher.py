import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tracking System Launcher")
        self.setGeometry(100, 100, 400, 250)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)  # fixed size

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        # Title Label
        title = QLabel("Welcome to Tracking Systems")
        title_font = QFont("Segoe UI", 18, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Return Tracking Button
        self.return_button = QPushButton("Return Tracking System")
        self.return_button.setFixedHeight(50)
        self.return_button.clicked.connect(self.launch_return_tracking)
        layout.addWidget(self.return_button)

        # Restock Tracking Button
        self.restock_button = QPushButton("Restock Tracking System")
        self.restock_button.setFixedHeight(50)
        self.restock_button.clicked.connect(self.launch_restock_tracking)
        layout.addWidget(self.restock_button)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                background-color: #0078d4;
                color: white;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)
    def launch_return_tracking(self):
        subprocess.Popen([sys.executable, "return_tracking/main.py"])

    def launch_restock_tracking(self):
        subprocess.Popen([sys.executable, "restock_tracking/restock_main.py"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec_())
