import os
import style_sheet
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QApplication, QVBoxLayout
from console_widget import ConsoleWidget


class ImageSequenceWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()

        console = ConsoleWidget()

        self.image_sequence = []

        image_files = list(Path(image_path).glob("*.png")) + list(Path(image_path).glob("*.jpg"))
        console.append_text(str(image_files))
        console.append_text("---------------------------------")
        self.image_sequence = [str(file) for file in image_files]
        console.append_text(str(self.image_sequence))

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)

        for image_path in self.image_sequence:
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)

            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaledToHeight(200, Qt.SmoothTransformation)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(label)

            filename_label = QLabel(os.path.basename(image_path))
            filename_label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(filename_label)

            content_layout.addWidget(image_widget)

        scroll_area.setWidget(content_widget)
        scroll_area.setStyleSheet(style_sheet.scroll_bar_style())

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)