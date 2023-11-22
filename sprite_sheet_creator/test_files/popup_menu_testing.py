import sys
from PIL import Image, ImageSequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QDialog, QLabel, QPushButton, \
    QComboBox, QMessageBox
import apng


class ConvertImageDialog(QDialog):
    def __init__(self, parent=None):
        super(ConvertImageDialog, self).__init__(parent)

        self.setWindowTitle("Convert Image Type")

        # Widgets
        self.image_label = QLabel("Select an image:")
        self.image_path_label = QLabel()
        self.browse_button = QPushButton("Browse")
        self.format_label = QLabel("Select output format:")
        self.format_combobox = QComboBox()
        self.convert_button = QPushButton("Convert")

        # Supported image formats
        self.supported_formats = ["PNG", "JPEG", "APNG", "GIF", "BMP"]

        # Populate combo box with supported formats
        self.format_combobox.addItems(self.supported_formats)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_path_label)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combobox)
        layout.addWidget(self.convert_button)
        self.setLayout(layout)

        # Connect signals
        self.browse_button.clicked.connect(self.browse_image)
        self.convert_button.clicked.connect(self.convert_image)

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.apng *.gif *.bmp)")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                   "Images (*.png *.jpg *.jpeg *.apng *.gif *.bmp)")

        if file_path:
            self.image_path_label.setText(file_path)

    def convert_image(self):
        input_path = self.image_path_label.text()
        output_format = self.format_combobox.currentText()

        if not input_path:
            return

        # Convert image
        try:
            if output_format == "APNG":
                # No need to convert, as APNG is already supported
                output_path = input_path.rsplit('.', 1)[0] + "." + output_format.lower()
                Image.open(input_path).save(output_path, format=output_format)
            elif output_format == "GIF":
                # Convert APNG to GIF using apng2gif
                apng_image = apng.APNG.open(input_path)
                output_path = input_path.rsplit('.', 1)[0] + "." + output_format.lower()
                gif_frames = [frame.to_pil() for frame in apng_image.frames]
                gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:],
                                   duration=apng_image.playtime * 1000, loop=0)
            else:
                # Convert other formats using PIL
                image = Image.open(input_path)
                output_path = input_path.rsplit('.', 1)[0] + "." + output_format.lower()
                image.save(output_path, format=output_format)

            QMessageBox.information(self, "Conversion Successful", "Image converted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error converting image: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Main window setup
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Image Converter")

        # Menu setup
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        # Add action to open Convert Image Type dialog
        convert_action = file_menu.addAction("Convert Image Type")
        convert_action.triggered.connect(self.open_convert_image_dialog)

    def open_convert_image_dialog(self):
        convert_dialog = ConvertImageDialog(self)
        convert_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
