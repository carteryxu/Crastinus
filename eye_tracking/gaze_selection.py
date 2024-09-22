import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel

class GazeSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_directions = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Select Allowed Gaze Directions")
        layout = QVBoxLayout()

        self.label = QLabel("Select allowed gaze directions:")
        layout.addWidget(self.label)

        self.center_checkbox = QCheckBox("CENTER")
        self.center_checkbox.setChecked(True)
        layout.addWidget(self.center_checkbox)

        self.up_checkbox = QCheckBox("UP")
        layout.addWidget(self.up_checkbox)

        self.down_checkbox = QCheckBox("DOWN")
        layout.addWidget(self.down_checkbox)

        self.left_checkbox = QCheckBox("LEFT")
        layout.addWidget(self.left_checkbox)

        self.right_checkbox = QCheckBox("RIGHT")
        layout.addWidget(self.right_checkbox)

        self.submit_button = QPushButton("Confirm")
        self.submit_button.clicked.connect(self.submit_directions)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_directions(self):
        # Gather selected directions
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

        # Close window after selection
        self.close()

    def get_selected_directions(self):
        return self.selected_directions
    
    def select_allowed_gaze_directions():
        app = QApplication(sys.argv)
        window = GazeSelection()
        window.show()
        app.exec_()
        return window.get_selected_directions()