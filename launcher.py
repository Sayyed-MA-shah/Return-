import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tracking System Launcher")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.return_button = QPushButton("Return Tracking System")
        self.return_button.clicked.connect(self.launch_return_tracking)
        layout.addWidget(self.return_button)

        self.restock_button = QPushButton("Restock Tracking System")
        self.restock_button.clicked.connect(self.launch_restock_tracking)
        layout.addWidget(self.restock_button)

        self.setLayout(layout)

    def launch_return_tracking(self):
        subprocess.Popen([sys.executable, "return_tracking/main.py"])

    def launch_restock_tracking(self):
        subprocess.Popen([sys.executable, "restock_tracking/restock_main.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec_())
