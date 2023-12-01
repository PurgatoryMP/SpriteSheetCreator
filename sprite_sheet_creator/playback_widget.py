from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea, QScrollBar, QGraphicsView, QGraphicsScene
import style_sheet
import datetime


# TODO: Fit the playback to the widget on scale
# TODO: Fix the zoom to match the image viewer.
# TODO: Fix Checker Alpha Background not appearing.

class PlaybackWidget(QWidget):
    """
    A widget for playing back an image sequence.

    Args:
        main_console_widget (QWidget): The main console widget.
        control_widget (QWidget): The control widget.
        status_bar (QWidget): The status bar widget.
        parent (QWidget, optional): The parent widget. Defaults to None.
    """

    def __init__(self, main_console_widget, control_widget, status_bar, parent=None):
        """
        Initializes the PlaybackWidget.

        Args:
            main_console_widget (QWidget): The main console widget.
            control_widget (QWidget): The control widget.
            status_bar (QWidget): The status bar widget.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super(PlaybackWidget, self).__init__(parent)
        self.Playtime_label = None
        self.label = None
        self.scene = None
        self.view = None
        self.console = main_console_widget
        self.is_playing = False
        self.status = status_bar
        self.status.set_status_text("N/A")

        self.image_sequence = []
        self.current_frame = 0
        self.zoom_factor = 1.0
        self.zoom_origin = None
        self.drag_origin = None
        self.dragging = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.setup_ui()

        self.control = control_widget
        self.control.update_frame_number(self.current_frame)

        # Add a timer with a delay so the images are resized to fit the widget after you release the resize control.
        self.resize_timer = QTimer()
        self.resize_timer.setInterval(500)  # Set the delay in milliseconds
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.report_size)

        self.console.append_text("INFO: Playback Widget Loaded.")

    def setup_ui(self):
        """
        Sets up the user interface for the widget.
        """
        try:
            layout = QVBoxLayout(self)
            self.view = QGraphicsView(self)
            self.scene = QGraphicsScene(self)
            self.view.setScene(self.scene)
            self.view.setStyleSheet(style_sheet.graphics_scene_style())
            layout.addWidget(self.view)

            scroll_area = QScrollArea(self)
            scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.view)
            layout.addWidget(scroll_area)

            # Create a QLabel
            self.Playtime_label = QLabel("Playtime:", self)
            self.Playtime_label.setStyleSheet(style_sheet.folder_path_label_style())
            self.Playtime_label.setToolTip("Sprite sheet animation length: Duration = cells/fps")
            layout.addWidget(self.Playtime_label)

        except Exception as err:
            self.console.append_text("ERROR: setup_ui: {}".format(err.args))

    def load_image_sequence(self, image_sequence_list):
        """
        Loads an image sequence.

        Args:
            image_sequence_list (list): A list of image file paths.
        """
        try:
            self.image_sequence = []
            if image_sequence_list:
                for file_path in image_sequence_list:
                    self.console.append_text("INFO: Playback Widget: Loading Image: {}".format(file_path))
                    self.image_sequence.append(QImage(file_path))
                # start the playback after the image sequence is done loading.
                self.start_playback()
                self.display_playtime()
                self.resize(2, 2)
        except Exception as err:
            self.console.append_text("ERROR: load_image_sequence: {}".format(err.args))

    def fit_to_widget(self) -> None:
        """
        Fits the image to the size of the widget.
        """
        try:
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        except Exception as err:
            self.console.append_text("ERROR: fit_to_widget: {}".format(err.args))

    def start_playback(self):
        """
        Starts the playback of the image sequence.
        """
        try:
            if self.image_sequence:

                playback_speed = 1000 / self.control.get_fps_value()

                self.timer.start(int(playback_speed))  # 30 frames per second
                self.is_playing = True
                self.console.append_text("INFO: Playback Started.")
                self.status.set_status_text("Playing Sequence.")
        except Exception as err:
            self.console.append_text("ERROR: start_playback: {}".format(err.args))

    def stop_playback(self):
        """
        Stops the playback of the image sequence.
        """
        self.timer.stop()
        self.is_playing = False
        self.display_playtime()
        self.console.append_text("INFO: Playback Stopped.")
        self.status.set_status_text("Playback Stopped.")

    def set_fps_value(self, value: int) -> None:
        """Sets the playback frame rate.

        Args:
            value: (str): The integer value to apply to the playback fps.
        """
        self.stop_playback()
        self.console.append_text("INFO: FPS set to: {}".format(value))
        self.display_playtime()
        if value:
            self.timer.setInterval(1000 / value)
            self.start_playback()

    def set_frame_number(self):
        """
        Sets the current frame number.
        """
        try:
            if not self.is_playing:
                if self.current_frame >= len(self.image_sequence):
                    self.current_frame = len(self.image_sequence) - 1

                image = self.image_sequence[self.control.get_display_value()]
                pixmap = QPixmap.fromImage(image)
                self.scene.clear()
                self.scene.addPixmap(pixmap)
                self.display_playtime()
        except Exception as err:
            self.console.append_text("ERROR: set_frame_number: {}".format(err.args))

    def display_playtime(self):
        """
        Display the current length of the sprite sheet if played at the defined settings.
        """
        try:
            fps = self.control.get_fps_value()
            cell_count = self.control.get_grid_rows_value() * self.control.get_grid_columns_value()

            if fps:
                playtime = cell_count/fps

                duration = datetime.timedelta(seconds=playtime)

                # Extract hours, minutes, and seconds from the duration
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                microseconds = duration.microseconds

                self.Playtime_label.clear()
                self.Playtime_label.setText(
                    "Playtime: {}:{}:{}.{}s".format(hours, minutes, seconds, microseconds))
            else:
                self.Playtime_label.clear()
                self.Playtime_label.setText("None")
        except Exception as err:
            self.console.append_text("ERROR: display_playtime: {}".format(err.args))

    def update_frame(self):
        """
        Updates the current frame.
        """
        try:
            # if self.current_frame >= len(self.image_sequence):
            if self.current_frame >= len(self.image_sequence):
                self.current_frame = self.control.get_start_frame_value()

            if self.current_frame >= self.control.get_end_frame_value():
                self.current_frame = self.control.get_start_frame_value()

            image = self.image_sequence[self.current_frame]
            pixmap = QPixmap.fromImage(image)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
            self.current_frame += 1

            # Update the control.
            self.control.update_frame_number(self.current_frame)
        except Exception as err:
            self.console.append_text("ERROR: update_frame: {}".format(err.args))

    # def wheelEvent(self, event):
    #     """
    #     Handles the wheel event.
    #
    #     Args:
    #         event (QWheelEvent): The wheel event object.
    #     """
    #     try:
    #         if event.modifiers() == Qt.ControlModifier:
    #             if not self.image_sequence:
    #                 return
    #
    #             delta = event.angleDelta().y() / 120
    #             zoom_factor = 1.1 ** delta
    #             new_zoom_factor = self.zoom_factor * zoom_factor
    #
    #             if self.minimum_zoom <= new_zoom_factor <= self.maximum_zoom:
    #                 self.zoom_factor = new_zoom_factor
    #
    #             cursor_pos = self.view.mapFromGlobal(event.globalPos())
    #             self.zoom_origin = cursor_pos
    #
    #             if 0 <= self.current_frame < len(self.image_sequence):
    #                 image = self.image_sequence[self.current_frame]
    #                 pixmap = QPixmap.fromImage(image)
    #
    #                 self.scene.clear()
    #                 self.scene.addPixmap(self.zoomed_pixmap(pixmap))
    #
    #                 # Apply the zoom factor to the view
    #                 self.view.setTransform(QTransform().scale(self.zoom_factor, self.zoom_factor))
    #
    #                 # Adjust the scroll bars to keep the view centered
    #                 scroll_area = self.view.parentWidget()
    #                 horizontal_bar = scroll_area.horizontalScrollBar()
    #                 vertical_bar = scroll_area.verticalScrollBar()
    #
    #                 # Calculate the center point of the view
    #                 view_rect = self.view.viewport().rect()
    #                 center_point = view_rect.center()
    #
    #                 # Adjust the scroll bars to keep the center point visible
    #                 horizontal_bar.setValue(horizontal_bar.value() + cursor_pos.x() - center_point.x())
    #                 vertical_bar.setValue(vertical_bar.value() + cursor_pos.y() - center_point.y())
    #
    #     except Exception as err:
    #         self.console.append_text("ERROR: wheelEvent: {}".format(err.args))
    #
    # def mousePressEvent(self, event):
    #     """
    #     Handles the mouse press event.
    #
    #     Args:
    #         event (QMouseEvent): The mouse event object.
    #     """
    #     try:
    #         if event.button() == Qt.LeftButton:
    #             self.drag_origin = event.pos()
    #             self.dragging = True
    #     except Exception as err:
    #         self.console.append_text("ERROR: mousePressEvent: {}".format(err.args))
    #
    # def mouseMoveEvent(self, event):
    #     """
    #     Handles the mouse move event.
    #
    #     Args:
    #         event (QMouseEvent): The mouse event object.
    #     """
    #     try:
    #         if self.dragging:
    #             delta = event.pos() - self.drag_origin
    #             self.drag_origin = event.pos()
    #
    #             self.label.scroll(-delta.x(), -delta.y())
    #     except Exception as err:
    #         self.console.append_text("ERROR: mouseMoveEvent: {}".format(err.args))
    #
    # def mouseReleaseEvent(self, event):
    #     """
    #     Handles the mouse release event.
    #
    #     Args:
    #         event (QMouseEvent): The mouse event object.
    #     """
    #     try:
    #         if event.button() == Qt.LeftButton:
    #             self.dragging = False
    #     except Exception as err:
    #         self.console.append_text("ERROR: mouseReleaseEvent: {}".format(err.args))
    #
    # def zoomed_pixmap(self, pixmap):
    #     """
    #     Applies zooming to the pixmap.
    #
    #     Args:
    #         pixmap (QPixmap): The pixmap object.
    #
    #     Returns:
    #         QPixmap: The zoomed pixmap.
    #     """
    #     try:
    #         if self.zoom_factor != 1.0:
    #             transform = QTransform()
    #             transform.translate(self.zoom_origin.x(), self.zoom_origin.y())
    #             transform.scale(self.zoom_factor, self.zoom_factor)
    #             transform.translate(-self.zoom_origin.x(), -self.zoom_origin.y())
    #             pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
    #         return pixmap
    #     except Exception as err:
    #         self.console.append_text("ERROR: zoomed_pixmap: {}".format(err.args))
    #
    # @property
    # def minimum_zoom(self):
    #     """
    #     float: The minimum zoom factor.
    #     """
    #     return 0.1  # Adjust the minimum zoom factor as desired
    #
    # @property
    # def maximum_zoom(self):
    #     """
    #     float: The maximum zoom factor.
    #     """
    #     return 5.0  # Adjust the maximum zoom factor as desired

    def resizeEvent(self, event) -> None:
        """
        Triggered when the main window is resized by the user.
        """
        # Call the base class resizeEvent method
        super().resizeEvent(event)
        # Start or restart the resize timer
        self.resize_timer.start()

    def report_size(self) -> None:
        """
        Report the current size of the main window.

        After the window has been resized, this function fits the images to the new widget size.

        """
        self.fit_to_widget()
