import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QColor, QPalette, QPainter, QBrush

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

class FileUpload(QWidget):
    def __init__(self):
        super().__init__()
        self.uploaded_image_path = None
        self.uploaded_sound_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cyberpunk File Upload')
        self.setGeometry(100, 100, 600, 400)
        
        # Set the cyberpunk theme palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 15))
        palette.setColor(QPalette.WindowText, QColor(230, 0, 255))
        palette.setColor(QPalette.Base, QColor(20, 20, 30))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 60))
        palette.setColor(QPalette.ToolTipBase, QColor(230, 0, 255))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 20, 80))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, QColor(255, 0, 100))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #ffffff;
                font-family: 'Rajdhani', 'Roboto', sans-serif;
            }
            QPushButton {
                background-color: #3c1450;
                color: #e600ff;
                font-size: 16px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #8a2be2;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #4b0082;
                border: 2px solid #e600ff;
            }
            QLabel {
                font-size: 14px;
                color: #b19cd9;
            }
        """)

        # Create and set up the background
        self.background = DotBackground(self)

        layout = QVBoxLayout()
        layout.setSpacing(20)

        title = QLabel("Upload Negative Stimulus Files")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #ffffff; margin-bottom: 30px; font-weight: bold;")
        layout.addWidget(title)

        self.upload_image_button = QPushButton("Upload Image")
        self.upload_image_button.setIcon(QIcon.fromTheme("image-x-generic"))
        self.upload_image_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_image_button, alignment=Qt.AlignCenter)

        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: #b19cd9; margin-bottom: 10px;")
        layout.addWidget(self.image_label)

        self.upload_sound_button = QPushButton("Upload Sound")
        self.upload_sound_button.setIcon(QIcon.fromTheme("audio-x-generic"))
        self.upload_sound_button.clicked.connect(self.upload_sound)
        layout.addWidget(self.upload_sound_button, alignment=Qt.AlignCenter)

        self.sound_label = QLabel("No sound selected")
        self.sound_label.setAlignment(Qt.AlignCenter)
        self.sound_label.setStyleSheet("color: #b19cd9; margin-bottom: 10px;")
        layout.addWidget(self.sound_label)

        self.submit_button = QPushButton("Confirm")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4b0082;
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #e600ff;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #8a2be2;
            }
        """)
        self.submit_button.clicked.connect(self.submit_files)
        layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    def upload_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.custom_image_path = file_path
            self.image_label.setText(f"Selected: {file_path.split('/')[-1]}")
            self.image_label.setStyleSheet("color: #e600ff;")

    def upload_sound(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Sound", "", "Sound Files (*.wav *.mp3)", options=options)
        if file_path:
            self.custom_sound_path = file_path
            self.sound_label.setText(f"Selected: {file_path.split('/')[-1]}")
            self.sound_label.setStyleSheet("color: #e600ff;")
    
    def submit_files(self):
        self.uploaded_image = self.custom_image_path if hasattr(self, 'custom_image_path') else None
        self.uploaded_sound = self.custom_sound_path if hasattr(self, 'custom_sound_path') else None
        self.close()

    def get_files(self):
        return self.uploaded_image, self.uploaded_sound
        
def select_files():
    app = QApplication(sys.argv)
    window = FileUpload()
    window.show()
    app.exec_()
    return window.get_files()