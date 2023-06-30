import os

import style_sheet
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QScrollArea, QWidget, QGraphicsView, QGraphicsScene, QPushButton, \
    QHBoxLayout


class ImageViewerWidget(QWidget):
    imagepathClicked = pyqtSignal(str)

    def __init__(self, main_console_widget):
        """Initialize the ImageViewerWidget.

        Args:
            main_console_widget (QWidget): The console widget for displaying messages.
        """
        super().__init__()

        self.console = main_console_widget
        self.console.append_text("INFO: Loading Image Viewer Widget.----------------")

        self.setMouseTracking(True)
        self.scroll_pos = None
        self.original_pixmap = None

        self.display_name_label = QLabel("File Name:")
        self.display_name_label.setStyleSheet(style_sheet.folder_path_label_style())

        self.display_name_button = QPushButton("Explore Folder")
        self.display_name_button.setFixedSize(150, 30)  # Set the width to 80 pixels and height to 30 pixels
        self.display_name_button.setStyleSheet(style_sheet.explore_folder_btn_style())

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        self.scroll_area.setWidgetResizable(True)

        self.view = QGraphicsView()
        self.view.setStyleSheet(style_sheet.graphics_scene_style())
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.scroll_area.setWidget(self.view)

        layout = QVBoxLayout(self)
        layout_header = QHBoxLayout()
        layout_header.addWidget(self.display_name_label)
        layout_header.addWidget(self.display_name_button)
        layout.addLayout(layout_header)
        layout.addWidget(self.scroll_area)

        self.scale_factor = 1.0
        self.min_scale_factor = 0.2
        self.max_scale_factor = 3.0

        # Call the method to update the display name label with an empty file name
        self.set_display_name_label("")
        self.console.append_text("INFO: Finished Loading Image Viewer Widget.")

    def load_image(self, image_sequence: list, frame_index: int) -> None:
        """Load and display an image from an image sequence.

        Args:
            image_sequence (list): The list of image paths in the sequence.
            frame_index (int): The index of the frame to display.
        """
        try:
            image_path = image_sequence[frame_index]
            self.original_pixmap = QPixmap(image_path)
            self.scene.clear()
            self.scene.addPixmap(self.original_pixmap)
            self.fit_to_widget()
            self.set_display_name_label(image_path)
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def set_select_image(self, file_path) -> None:
        """Set and display a selected image.

        Args:
            file_path (str): The path of the selected image file.
        """
        try:
            if file_path:
                self.set_display_name_label(file_path)
                self.console.append_text("Selected image: {}".format(os.path.basename(file_path)))
                self.original_pixmap = QPixmap(file_path)
                self.scene.clear()
                self.scene.addPixmap(self.original_pixmap)
                self.fit_to_widget()
            else:
                self.console.append_text("ERROR: File Not Found: {}".format(file_path))


        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def wheelEvent(self, event) -> None:
        """Handle wheel events for zooming the image.

        Args:
            event (QWheelEvent): The wheel event object.
        """
        try:
            if event.modifiers() == Qt.ControlModifier:
                # Only zoom when the Ctrl key is pressed
                scroll_delta = event.angleDelta().y()
                zoom_factor = 1.1 if scroll_delta > 0 else 0.9

                cursor_pos = event.pos()
                self.scroll_pos = self.view.mapToScene(cursor_pos)

                self.zoom_image(zoom_factor)
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def zoom_image(self, zoom_factor) -> None:
        """Zoom the displayed image.

        Args:
            zoom_factor (float): The zoom factor.
        """
        try:
            old_pos = self.view.mapToScene(self.view.viewport().rect().center())

            self.scale_factor *= zoom_factor
            if self.scale_factor < self.min_scale_factor:
                self.scale_factor = self.min_scale_factor
            elif self.scale_factor > self.max_scale_factor:
                self.scale_factor = self.max_scale_factor

            self.view.setTransform(QTransform().scale(self.scale_factor, self.scale_factor))

            new_pos = self.view.mapToScene(self.view.viewport().rect().center())

            scroll_adjustment = new_pos - old_pos
            self.view.horizontalScrollBar().setValue(
                int(self.view.horizontalScrollBar().value()) + int(scroll_adjustment.x())
            )
            self.view.verticalScrollBar().setValue(
                int(self.view.verticalScrollBar().value()) + int(scroll_adjustment.y())
            )

            if self.scroll_pos is not None:
                self.view.centerOn(self.scroll_pos)
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def fit_to_widget(self) -> None:
        """Fit the image to the size of the widget."""
        try:
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def set_display_name_label(self, file_path) -> None:
        """Set the text of the QLabel to the name of the file currently being displayed.

        Args:
            file_path (str): The path of the file being displayed.
        """
        try:
            if self.display_name_label is not None and file_path:
                self.display_name_label.setText("{}".format(file_path))
                self.display_name_button.clicked.connect(lambda: self.handle_image_path_click(file_path))
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))

    def handle_image_path_click(self, image_path):
        try:
            self.imagepathClicked.emit(image_path)
        except Exception as err:
            self.console.append_text("ERROR: {}".format(err.args))


