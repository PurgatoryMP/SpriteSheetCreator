import os
from PyQt5.QtCore import Qt, pyqtSignal, QFileInfo
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout

import style_sheet


class ImageSequenceWidget(QWidget):
    """A widget for displaying an image sequence."""

    imageClicked = pyqtSignal(str)

    def __init__(self, table_widget, control_widget, main_console_widget):
        """
        Initialize the ImageSequenceWidget.

        Args:
            table_widget (QWidget): The table widget for displaying image information.
            control_widget (QWidget): The control widget for setting start and end frames.
            main_console_widget (QWidget): The console widget for displaying messages.
        """
        super().__init__()
        self.table = table_widget

        self.console = main_console_widget

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

        self.console.append_text("INFO: Image Sequence Widget Loaded.")

    def load_sequence(self, image_sequence_list):
        """
        Load a new image sequence.

        Args:
            image_sequence_list (list): A list of image paths for the sequence.
        """
        try:
            # Clear existing image widgets
            for i in reversed(range(self.content_layout.count())):
                widget_item = self.content_layout.itemAt(i)
                if widget_item is not None:
                    widget_item.widget().setParent(None)

            # Load new image sequence
            if image_sequence_list:
                for image_path in image_sequence_list:
                    self.set_table_info(image_path)
                    self.console.append_text("INFO: Adding Image to grid: {}".format(image_path))
                    image_widget = QWidget()
                    image_layout = QVBoxLayout(image_widget)

                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)

                    label = QLabel()
                    label.setStyleSheet(style_sheet.image_grid_image_style())
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)

                    # Connect the clicked signal of the label to the slot function
                    label.mousePressEvent = lambda event, path=image_path: self.handle_image_click(event, path)

                    image_layout.addWidget(label)

                    filename_label = QLabel(os.path.basename(image_path))
                    filename_label.setStyleSheet(style_sheet.image_grid_label_style())
                    filename_label.setAlignment(Qt.AlignCenter)

                    # Connect the clicked signal of the label to the slot function
                    filename_label.mousePressEvent = lambda event, path=image_path: self.handle_image_click(event, path)

                    image_layout.addWidget(filename_label)

                    self.content_layout.addWidget(image_widget)

            self.scroll_area.setWidget(self.content_widget)
            self.updateGeometry()
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def set_table_info(self, file_path):
        """
        Set image information in the table.

        Args:
            file_path (str): The path of the image file.
        """

        file_info = QFileInfo(file_path)

        # Extract file creation time
        creation_time = file_info.created().toString(Qt.ISODate)

        # Extract file name and file path
        file_name = file_info.fileName()
        file_path = file_info.filePath()

        # Extract file size
        file_size = file_info.size()
        file_size_gb = file_size / (1024 * 1024)
        formatted_file_size_gb = "{:.3f}GB".format(file_size_gb)

        # Extract image width and height
        pixmap = QPixmap(file_path)
        image_width = pixmap.width()
        image_height = pixmap.height()
        bit_depth = pixmap.depth()

        self.table.append_data(
            creation_time, file_name, file_path, formatted_file_size_gb, image_width, image_height,
            "{}bit".format(bit_depth))

    def handle_image_click(self, event, image_path):
        """
        Handle the click event on an image.

        Args:
            event (QMouseEvent): The mouse event.
            image_path (str): The path of the clicked image.
        """
        if event.button() == Qt.LeftButton:
            self.imageClicked.emit(image_path)
