import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout

import style_sheet


class ImageSequenceWidget(QWidget):
    imageClicked = pyqtSignal(str)

    def __init__(self, control_widget, console_widget):
        super().__init__()
        self.console = console_widget
        self.console.append_text("Loading: Image Sequence Widget.\n")

        self.start_frame = control_widget.get_start_frame_value()
        self.end_frame = control_widget.get_end_frame_value()

        self.image_sequence = []

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QHBoxLayout(self.content_widget)

        self.scroll_area.setWidget(self.content_widget)
        self.scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        self.scroll_area.setMinimumHeight(250)
        self.scroll_area.setMaximumHeight(250)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.console.append_text("Finished Loading Image Sequence Widget.\n")

    def load_sequence(self, image_sequence_list):
        try:
            # Clear existing image widgets
            for i in reversed(range(self.content_layout.count())):
                widget_item = self.content_layout.itemAt(i)
                if widget_item is not None:
                    widget_item.widget().setParent(None)

            # Load new image sequence
            if image_sequence_list:
                for image_path in image_sequence_list:
                    self.console.append_text("Loading Image: {}".format(image_path))
                    image_widget = QWidget()
                    image_layout = QVBoxLayout(image_widget)

                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)

                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)

                    # Connect the clicked signal of the label to the slot function
                    label.mousePressEvent = lambda event, path=image_path: self.handle_image_click(event, path)

                    image_layout.addWidget(label)

                    filename_label = QLabel(os.path.basename(image_path))
                    filename_label.setAlignment(Qt.AlignCenter)

                    image_layout.addWidget(filename_label)

                    self.content_layout.addWidget(image_widget)

            self.scroll_area.setWidget(self.content_widget)
            self.updateGeometry()
        except Exception as err:
            self.console.append_text(str(err.args))

    def handle_image_click(self, event, image_path):
        if event.button() == Qt.LeftButton:
            self.imageClicked.emit(image_path)