import os
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea
from console_widget import ConsoleWidget
from controls_widget import ControlWidget

class PlaybackWidget(QWidget):
    def __init__(self, directory_path, console_widget, control_widget, parent=None):
        super(PlaybackWidget, self).__init__(parent)
        self.console = console_widget
        self.console.append_text("Loading Playback Widget.")

        self.image_list = []
        self.current_frame = 0
        self.zoom_factor = 1.0
        self.zoom_origin = None
        self.drag_origin = None
        self.dragging = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.load_image_sequence(directory_path)
        self.setup_ui()

        self.control = control_widget
        self.control.update_frame_number(self.current_frame)

        self.console.append_text(str(self.control.get_fps_value()))

        self.start_playback()

    def load_image_sequence(self, directory_path):
        for file_name in sorted(os.listdir(directory_path)):
            if file_name.endswith('.png'):
                image_path = os.path.join(directory_path, file_name)
                self.image_list.append(QImage(image_path))

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

    def stop_playback(self):
        self.timer.stop()

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
        if self.zoom_factor != 1.0:
            transform = QTransform()
            transform.translate(self.zoom_origin.x(), self.zoom_origin.y())
            transform.scale(self.zoom_factor, self.zoom_factor)
            transform.translate(-self.zoom_origin.x(), -self.zoom_origin.y())
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        return pixmap

    @property
    def minimum_zoom(self):
        return 0.1  # Adjust the minimum zoom factor as desired

    @property
    def maximum_zoom(self):
        return 5.0  # Adjust the maximum zoom factor as desired
