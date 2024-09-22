import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class FileUpload(QWidget):
    def __init__(self):
        super().__init__()
        self.uploaded_image_path = None
        self.uploaded_sound_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Upload')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Upload buttons
        self.upload_image_button = QPushButton("Upload Custom Image")
        self.upload_image_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_image_button, alignment=Qt.AlignCenter)

        self.upload_sound_button = QPushButton("Upload Custom Sound")
        self.upload_sound_button.clicked.connect(self.upload_sound)
        layout.addWidget(self.upload_sound_button, alignment=Qt.AlignCenter)

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
        self.submit_button.clicked.connect(self.submit_image)
        self.submit_button.clicked.connect(self.submit_sound)
        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def upload_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.custom_image_path = file_path
            # Update button text to the name of the uploaded file
            self.upload_image_button.setText(file_path.split('/')[-1])  # Get the filename

    def upload_sound(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Sound", "", "Sound Files (*.wav *.mp3)", options=options)
        if file_path:
            self.custom_sound_path = file_path
            # Update button text to the name of the uploaded file
            self.upload_sound_button.setText(file_path.split('/')[-1])  # Get the filename
    
    def submit_image(self):
        self.uploaded_image = self.custom_image_path

    def submit_sound(self):
        self.uploaded_sound = self.custom_sound_path
        self.close()
    
    def get_image(self):
        return self.uploaded_image
    
    def get_sound(self):
        return self.uploaded_sound
        
def get_image():
    app = QApplication(sys.argv)
    window = FileUpload()
    window.show()
    app.exec_()
    return window.get_image()

def get_sound():
    app = QApplication(sys.argv)
    window = FileUpload()
    window.show()
    app.exec_()
    return window.get_sound()