import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class GazeSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_directions = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Allowed Gaze Directions")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Label with custom font
        self.label = QLabel("Select Session Allowed Gaze Directions:")
        self.label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(100)
        self.label.setStyleSheet("QLabel { padding: 10px; }")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)


        # Checkboxes with custom font
        checkbox_font = QFont("Segoe UI", 18)
        self.center_checkbox = QCheckBox("CENTER")
        self.center_checkbox.setChecked(True)
        self.center_checkbox.setFont(checkbox_font)
        layout.addWidget(self.center_checkbox)

        self.up_checkbox = QCheckBox("UP")
        self.up_checkbox.setFont(checkbox_font)
        layout.addWidget(self.up_checkbox)

        self.down_checkbox = QCheckBox("DOWN")
        self.down_checkbox.setFont(checkbox_font)
        layout.addWidget(self.down_checkbox)

        self.left_checkbox = QCheckBox("LEFT")
        self.left_checkbox.setFont(checkbox_font)
        layout.addWidget(self.left_checkbox)

        self.right_checkbox = QCheckBox("RIGHT")
        self.right_checkbox.setFont(checkbox_font)
        layout.addWidget(self.right_checkbox)

        # Confirm button with stylesheet
        self.submit_button = QPushButton("Confirm")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #1c3e70;
                color: white;
                font-family: 'Arial Rounded MT Bold';
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        self.submit_button.clicked.connect(self.submit_directions)
        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def submit_directions(self):
        self.selected_directions = []
        if self.center_checkbox.isChecked():
            self.selected_directions.append("CENTER")
        if self.left_checkbox.isChecked():
            self.selected_directions.append("LEFT")
        if self.right_checkbox.isChecked():
            self.selected_directions.append("RIGHT")
        if self.up_checkbox.isChecked():
            self.selected_directions.append("UP")
        if self.down_checkbox.isChecked():
            self.selected_directions.append("DOWN")

        self.close()

    def get_selected_directions(self):
        return self.selected_directions

def select_allowed_gaze_directions():
    app = QApplication(sys.argv)
    window = GazeSelection()
    window.show()
    app.exec_()
    return window.get_selected_directions()
