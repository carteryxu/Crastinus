import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPoint

class DotBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the base dark background
        painter.fillRect(self.rect(), QColor(10, 10, 15))
        
        # Set up the grid of dots
        dot_color = QColor(30, 30, 40)  # Slightly lighter than the background
        dot_size = 2
        spacing = 10
        
        for x in range(0, self.width(), spacing):
            for y in range(0, self.height(), spacing):
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(dot_color))
                painter.drawEllipse(QPoint(x, y), dot_size // 2, dot_size // 2)

class GazeSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_directions = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Gaze Preferences")
        self.setGeometry(300, 150, 1000, 600)

        # Create and set up the background
        self.background = DotBackground(self)
        self.background.resize(self.size())

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Label with custom font
        self.label = QLabel("Select Allowed Gaze Directions:")
        self.label.setFont(QFont("Rajdhani", 24, QFont.Bold))
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(100)
        self.label.setStyleSheet("QLabel { color: #fffff; padding: 10px; }")
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Checkboxes with custom font
        checkbox_font = QFont("Rajdhani", 18)
        checkbox_style = """
            QCheckBox {
                color: #b19cd9;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #8a2be2;
                background-color: #0a0a0f;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #e600ff;
                background-color: #8a2be2;
            }
        """

        self.center_checkbox = QCheckBox("CENTER")
        self.center_checkbox.setChecked(True)
        self.center_checkbox.setFont(checkbox_font)
        self.center_checkbox.setStyleSheet(checkbox_style)
        layout.addWidget(self.center_checkbox)

        self.up_checkbox = QCheckBox("UP")
        self.up_checkbox.setFont(checkbox_font)
        self.up_checkbox.setStyleSheet(checkbox_style)
        layout.addWidget(self.up_checkbox)

        self.down_checkbox = QCheckBox("DOWN")
        self.down_checkbox.setFont(checkbox_font)
        self.down_checkbox.setStyleSheet(checkbox_style)
        layout.addWidget(self.down_checkbox)

        self.left_checkbox = QCheckBox("LEFT")
        self.left_checkbox.setFont(checkbox_font)
        self.left_checkbox.setStyleSheet(checkbox_style)
        layout.addWidget(self.left_checkbox)

        self.right_checkbox = QCheckBox("RIGHT")
        self.right_checkbox.setFont(checkbox_font)
        self.right_checkbox.setStyleSheet(checkbox_style)
        layout.addWidget(self.right_checkbox)

        # Confirm button with stylesheet
        self.submit_button = QPushButton("Confirm")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4b0082;
                color: #ffffff;
                font-family: 'Rajdhani';
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: 2px solid #e600ff;
            }
            QPushButton:hover {
                background-color: #8a2be2;
            }
        """)
        self.submit_button.clicked.connect(self.submit_directions)
        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Set the widget background to transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

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