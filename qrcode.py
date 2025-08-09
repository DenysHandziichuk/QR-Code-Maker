from PyQt6.QtWidgets import QPushButton, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QApplication, QFileDialog
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
import webbrowser
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle("QR Code Generator and Reader")

        layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        self.label = QLabel("Enter URL to generate QR code:")
        self.entry = QLineEdit(self)
        self.button = QPushButton("Generate and Save QR Code", self)
        self.button1 = QPushButton("Open QR Code Image", self)
        self.button2 = QPushButton("Open website from QR", self)

        self.button.clicked.connect(self.generate_qr_code)
        self.button1.clicked.connect(self.open_picture)
        self.button2.clicked.connect(self.open_website)

        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.button)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.saved_file_path = None

    def generate_qr_code(self):
        url = self.entry.text()
        if url:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save QR Code",
                "",
                "PNG Image (*.png);;All Files (*)"
            )

            if file_path:
                qr_object = pyqrcode.create(url)
                qr_object.png(file_path, scale=6)
                self.saved_file_path = file_path
                print(f"QR code saved to: {file_path}")
            else:
                print("Save operation cancelled.")
        else:
            print("No URL provided. Please enter a URL.")

    def open_picture(self):
        if self.saved_file_path and os.path.exists(self.saved_file_path):
            image = Image.open(self.saved_file_path)
            image.show()
        else:
            print("No QR code has been saved yet. Please generate one first.")

    def open_website(self):
        if self.saved_file_path and os.path.exists(self.saved_file_path):
            try:
                image = Image.open(self.saved_file_path)
                qr_data = decode(image)
                if qr_data:
                    url = qr_data[0].data.decode("utf-8")
                    print("Opening URL:", url)
                    webbrowser.open(url)
                else:
                    print("No valid QR code found in the image.")
            except FileNotFoundError:
                print(f"QR Code file not found at: {self.saved_file_path}")
        else:
            print("No QR code has been saved yet. Please generate one first.")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()