import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QColor, QPalette, QPainter, QBrush, QFont

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

class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Crastinus Start')
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(300, 150, 900, 600)

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
                color: #b19cd9;
            }
        """)

        # Create and set up the background
        self.background = DotBackground(self)
        self.background.setGeometry(self.rect())  # Ensure background covers the whole window

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)  # Center layout items

        title = QLabel("CRASTINUS")
        title.setFont(QFont("Rajdhani", 40, QFont.Bold))  # Set font size and bold
        title.setAlignment(Qt.AlignCenter)  # Center the title
        layout.addWidget(title)

        layout.addSpacing(40)
        
        start_button = QPushButton("FOCUS")
        start_button.clicked.connect(self.pressed)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
    
    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    def pressed(self):
        self.close()

def start():
    app = QApplication(sys.argv)
    window = StartPage()
    window.show()
    app.aboutToQuit.connect(app.quit)  # Quit the entire program when the start page is closed
    sys.exit(app.exec_())
    window = StartPage()
    window.show()
    app.exec_()