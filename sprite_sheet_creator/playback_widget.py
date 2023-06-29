import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea


class PlaybackWidget(QWidget):
    def __init__(self, main_console_widget, control_widget, parent=None):
        super(PlaybackWidget, self).__init__(parent)
        self.console = main_console_widget
        self.console.append_text("Loading: Playback Widget.\n")

        self.image_list = []
        self.current_frame = 0
        self.zoom_factor = 1.0
        self.zoom_origin = None
        self.drag_origin = None
        self.dragging = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.image_sequence = []
        self.setup_ui()

        self.control = control_widget
        self.control.update_frame_number(self.current_frame)

        self.console.append_text(str(self.control.get_fps_value()))

        self.console.append_text("Finished Loading: Playback Widget.\n")

    def load_image_sequence(self, image_sequence_list):
        if image_sequence_list:
            for file_path in image_sequence_list:
                self.console.append_text("Playback Widget: Loading Image: {}".format(file_path))
                self.image_list.append(QImage(file_path))
            # start the playback after the image sequence is done loading.
            self.start_playback()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        layout.addWidget(scroll_area)

    def start_playback(self):
        if self.image_list:
            self.timer.start(1000 / self.control.get_fps_value())  # 30 frames per second
            self.console.append_text("Playback Started.")

    def stop_playback(self):
        self.timer.stop()
        self.console.append_text("Playback Stopped.")

    def set_fps_value(self, value: int) -> None:
        """Sets the playback frame rate.

        Args:
            value: (str): The integer value to apply to the playback fps.
        """
        self.stop_playback()
        self.console.append_text("Playback FPS changed to {}".format(value))
        if value:
            self.timer.setInterval(1000 / value)
            self.start_playback()

    def update_frame(self):
        if self.current_frame >= len(self.image_list):
            self.current_frame = 0
        image = self.image_list[self.current_frame]
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(self.zoomed_pixmap(pixmap))
        self.current_frame += 1

        # Update the control.
        self.control.update_frame_number(self.current_frame)

    def wheelEvent(self, event):
        try:
            if event.modifiers() == Qt.ControlModifier:
                delta = event.angleDelta().y() / 120
                zoom_factor = 1.1 ** delta
                new_zoom_factor = self.zoom_factor * zoom_factor
                if self.minimum_zoom <= new_zoom_factor <= self.maximum_zoom:
                    self.zoom_factor = new_zoom_factor

                cursor_pos = self.label.mapFromGlobal(event.globalPos())
                self.zoom_origin = cursor_pos

                image = self.image_list[self.current_frame]
                pixmap = QPixmap.fromImage(image)
                self.label.setPixmap(self.zoomed_pixmap(pixmap))
        except Exception as err:
            self.console.append_text(str(err.args))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_origin = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.drag_origin
            self.drag_origin = event.pos()

            self.label.scroll(-delta.x(), -delta.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def zoomed_pixmap(self, pixmap):
        try:
            if self.zoom_factor != 1.0:
                transform = QTransform()
                transform.translate(self.zoom_origin.x(), self.zoom_origin.y())
                transform.scale(self.zoom_factor, self.zoom_factor)
                transform.translate(-self.zoom_origin.x(), -self.zoom_origin.y())
                pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            return pixmap
        except Exception as err:
            self.console.append_text(str(err.args))

    @property
    def minimum_zoom(self):
        return 0.1  # Adjust the minimum zoom factor as desired

    @property
    def maximum_zoom(self):
        return 5.0  # Adjust the maximum zoom factor as desired
