import os
from PyQt5.QtWidgets import QFileDialog

class FileUploader:
    def __init__(self):
        self.custom_image_path = None
        self.custom_sound_path = None
    
    def upload_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(parent, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            self.custom_image_path = file_path
            return file_path
        
    def upload_sound(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(parent, "Upload Sound", "", "Sound Files (*.wav *.mp3)", options=options)
        if file_path:
            self.customer_sound_path = file_path
            return file_path
