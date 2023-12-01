from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QPen
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QScrollArea, QLabel

import style_sheet


class SpriteSheetWidget(QWidget):
    """Widget for displaying and manipulating sprite sheets."""

    labelClicked = pyqtSignal(str)

    def __init__(self, main_console_widget, control_widget):
        """
        Initializes the SpriteSheetWidget.

        Args:
            main_console_widget: QWidget: the main console widget.
            control_widget: QWidget: the control widget.
        """
        super().__init__()

        self.index_overlay = False
        self.scroll_pos = None
        self.sprite_sheet = None
        self.images = None
        self.grid_overlay = False
        self.use_scale = False
        self.console = main_console_widget
        self.control = control_widget

        self.image_sequence = []

        # Create the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QLabel
        self.label = QLabel("Sprite Sheet Scale:", self)
        self.label.setToolTip("Sprite sheet image dimensions.\nClick to copy to clipboard.")
        self.label.setStyleSheet(style_sheet.folder_path_label_style())
        layout.addWidget(self.label)

        # Create the QGraphicsView and QGraphicsScene
        self.view = QGraphicsView()
        self.view.setStyleSheet(style_sheet.graphics_scene_style())
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.view)

        # Add the scroll area to the layout
        layout.addWidget(scroll_area)

        # Zoom variables
        self.scale_factor = 1.0
        self.min_scale_factor = 0.1
        self.max_scale_factor = 10.0

        # Set the minimum grid size.
        self.minimum_grid_size = 0

        # Enable mouse tracking to receive mouse wheel events
        self.view.setMouseTracking(True)

        # Add a timer with a delay so the images are resized to fit the widget after you release the resize control.
        self.resize_timer = QTimer()
        self.resize_timer.setInterval(500)  # Set the delay in milliseconds
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.report_size)

        self.console.append_text("INFO: Sprite Sheet Widget Loaded.")

    def load_images(self, sequence: list) -> None:
        """Loads the provided image sequence.

        Args:
            sequence: str: a list of file paths to the individual images.
        """
        image_list = []

        start_frame = self.control.get_start_frame_value()
        self.control.set_end_frame_value(len(sequence))

        self.image_sequence = sequence[start_frame:len(sequence)]

        try:
            if self.image_sequence:
                for file_path in self.image_sequence:
                    image = QPixmap(file_path)
                    image_list.append(image)
                self.images = image_list

                if self.images:
                    self.sprite_sheet = self.create_sprite_sheet()

                    # Display the sprite sheet
                    self.display_sprite_sheet()
        except Exception as err:
            self.console.append_text("ERROR: load_images: {}".format(err.args))

    def update_sprite_sheet(self) -> None:
        """
        Updates the sprite sheet based on the current image sequence and settings.
        """
        try:
            if self.image_sequence:
                start = self.control.get_start_frame_value()
                end = self.control.get_end_frame_value()

                if start >= len(self.image_sequence):
                    self.control.set_start_frame_value(len(self.image_sequence))

                if end >= len(self.image_sequence):
                    self.control.set_end_frame_value(len(self.image_sequence))

                image_list = []
                for file_path in self.image_sequence[start:end]:
                    image = QPixmap(file_path)
                    image_list.append(image)
                self.images = image_list

                if self.images:
                    self.sprite_sheet = self.create_sprite_sheet()

                    # Display the sprite sheet
                    self.display_sprite_sheet()
                    self.fit_to_widget()

        except Exception as err:
            self.console.append_text("ERROR: update_sprite_sheet: {}".format(err.args))

    def calculate_rows_columns(self) -> tuple:
        """
        Calculates the number of rows and columns for the sprite sheet grid.

        Returns:
            tuple: the number of rows and columns.
        """
        try:
            minimum_value = 1
            rows = self.control.get_grid_rows_value()
            columns = self.control.get_grid_columns_value()

            if rows <= self.minimum_grid_size:
                self.control.set_grid_rows_value(minimum_value)
                rows = minimum_value
            elif columns <= self.minimum_grid_size:
                self.control.set_grid_columns_value(minimum_value)
                columns = minimum_value

            return rows, columns

        except Exception as err:
            self.console.append_text("ERROR: calculate_rows_columns: {}".format(err.args))

    def calculate_grid_size(self, file_paths, grid_rows, grid_columns):
        """
        Calculates the size of a grid.

        Returns:
            tuple: grid_width, grid_height
        """
        # if len(file_paths) != grid_rows * grid_columns:
        #     raise ValueError("Number of files does not match the grid size")
        try:
            image_width = 0
            image_height = 0

            for file_path in file_paths:
                pixmap = QPixmap(file_path)
                image_width = max(image_width, pixmap.width())
                image_height = max(image_height, pixmap.height())

            grid_width = image_width * grid_columns
            grid_height = image_height * grid_rows

            return grid_width, grid_height

        except Exception as err:
            self.console.append_text("ERROR: calculate_grid_size: {}".format(err.args))

    def toggle_grid_overlay(self):
        try:
            if self.grid_overlay:
                self.grid_overlay = False
            else:
                self.grid_overlay = True

            self.console.append_text("INFO: Grid Overlay set to: {}".format(self.grid_overlay))
            self.update_sprite_sheet()

        except Exception as err:
            self.console.append_text("ERROR: toggle_grid_overlay: {}".format(err.args))

    def toggle_index_overlay(self):
        try:
            if self.index_overlay:
                self.index_overlay = False
            else:
                self.index_overlay = True

            self.console.append_text("INFO: Index Overlay set to: {}".format(self.index_overlay))
            self.update_sprite_sheet()

        except Exception as err:
            self.console.append_text("ERROR: toggle_index_overlay: {}".format(err.args))

    def toggle_use_scale(self):
        try:
            if self.use_scale:
                self.use_scale = False
            else:
                self.use_scale = True

            self.control.toggle_scale_value_control(self.use_scale)
            self.console.append_text("INFO: Use Scale set to: {}".format(self.use_scale))
            self.update_sprite_sheet()

        except Exception as err:
            self.console.append_text("ERROR: toggle_grid_overlay: {}".format(err.args))

    def create_sprite_sheet(self):
        """
        Creates the sprite sheet based on the loaded images and settings.

        Returns:
            QPixmap: the sprite sheet image.
        """
        try:
            # Get the scale values of the image.
            sprite_sheet_width = self.control.get_image_width_value()
            sprite_sheet_height = self.control.get_image_height_value()

            # Get the rows and columns
            rows, columns = self.calculate_rows_columns()

            # Use the source image's full scale for each cell rather than downscaling the images to fit the grid.
            if self.use_scale:
                grid_width, grid_height = self.calculate_grid_size(self.images, rows, columns)
                sprite_sheet_width = grid_width
                sprite_sheet_height = grid_height

                # append this info to the console.
                self.console.append_text(
                    "INFO: Generated Sprite Sheet Scale = {}x{}".format(sprite_sheet_width, sprite_sheet_height))

            # Calculate the target width and height for each image or 'cell'.
            target_width = sprite_sheet_width // columns
            target_height = sprite_sheet_height // rows

            # Update the label showing the current image dimensions.
            self.label.clear()
            self.label.setText("Sprite Sheet Scale: {}x{}, Cell Scale: {}x{}".format(sprite_sheet_width, sprite_sheet_height, target_width, target_height))

            # Connect the clicked signal of the label to the slot function
            self.label.mousePressEvent = lambda event, value=self.label.text(): self.handle_label_click(event, value)

            # Create the QPixmap for the sprite sheet layer.
            sprite_sheet = QPixmap(sprite_sheet_width, sprite_sheet_height)
            sprite_sheet.fill(Qt.transparent)

            # Create a separate QPixmap for the outline layer.
            grid_outline_layer = QPixmap(sprite_sheet_width, sprite_sheet_height)
            grid_outline_layer.fill(Qt.transparent)

            # Create an Outline around images on the sprite sheet.
            grid_painter = QPainter(grid_outline_layer)
            # Set the pen color to cyan for the outline and define the line thickness.
            grid_painter.setPen(QPen(Qt.cyan, 5))

            sprite_painter = QPainter(sprite_sheet)

            # Create a separate QPixmap for the label layer.
            label_layer = QPixmap(sprite_sheet_width, sprite_sheet_height)
            label_layer.fill(Qt.transparent)

            # Create a QPainter for the label layer.
            label_painter = QPainter(label_layer)
            # Set the font and color for the labels.
            label_font = label_painter.font()
            # Adjust the font size as needed
            label_font.setPointSize(28)
            label_painter.setFont(label_font)
            # Set the label text color
            label_painter.setPen(QPen(Qt.green))
            
            x = 0
            y = 0

            index = self.control.get_start_frame_value()

            for image in self.images:
                scaled_image = image.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)
                
                index += 1
                # image_name = str(self.image_sequence[index])
                # print(image_name)
                # self.console.append_text(str(image_name))

                # Calculate the offset to center the images within each cell.
                offset_x = (target_width - scaled_image.width()) // 2
                offset_y = (target_height - scaled_image.height()) // 2

                # Calculate the center coordinates for the current cell.
                cell_center_x = x + offset_x
                cell_center_y = y + offset_y

                # Draw the outline on the outline layer
                if self.grid_overlay:
                    grid_painter.drawRect(x, y, target_width, target_height)
                
                # Draw the label on the label layer.
                if self.index_overlay:
                    label_text = "{}".format(index)
                    label_painter.drawText(x, y + 60, label_text)

                # Draw the scaled image on the sprite sheet at the center of the cell.
                sprite_painter.drawPixmap(cell_center_x, cell_center_y, scaled_image)

                x += target_width
                if x >= sprite_sheet_width:
                    x = 0
                    y += target_height

            # Stop painting.
            grid_painter.end()
            sprite_painter.end()
            label_painter.end()

            # Combine the sprite sheet and the outline layer (required to see the outline)
            sprite_sheet_with_outline = QPixmap(sprite_sheet_width, sprite_sheet_height)
            sprite_sheet_with_outline.fill(Qt.transparent)
            sprite_sheet_with_outline_painter = QPainter(sprite_sheet_with_outline)
            sprite_sheet_with_outline_painter.drawPixmap(0, 0, sprite_sheet)
            sprite_sheet_with_outline_painter.drawPixmap(0, 0, grid_outline_layer)
            sprite_sheet_with_outline_painter.drawPixmap(0, 0, label_layer)
            sprite_sheet_with_outline_painter.end()

            # TODO: Add Masking layer sequence option.

            # return sprite_sheet
            return sprite_sheet_with_outline

        except Exception as err:
            self.console.append_text("ERROR: create_sprite_sheet: {}".format(err.args))

    def display_sprite_sheet(self) -> None:
        """
        Displays the sprite sheet in the QGraphicsView.
        """
        try:
            self.scene.clear()
            self.scene.addPixmap(self.sprite_sheet)
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

        except Exception as err:
            self.console.append_text("ERROR: display_sprite_sheet: {}".format(err.args))

    def get_generated_sprite_sheet(self):
        """
        Gets the generated sprite sheet image.
        """
        try:
            if self.images:
                pixmap = QPixmap(self.sprite_sheet)
                return pixmap

        except Exception as err:
            self.console.append_text("ERROR: display_sprite_sheet: {}".format(err.args))

    def wheelEvent(self, event) -> None:
        """
        Handles the wheel event for zooming the sprite sheet.

        Args:
            event: QWheelEvent: the wheel event object.
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
            self.console.append_text("ERROR: wheelEvent: {}".format(err.args))

    def zoom_image(self, zoom_factor) -> None:
        """
        Zooms the sprite sheet image.

        Args:
            zoom_factor: float: the zoom factor.
            self.scroll_pos: QPoint: the position to zoom around.
        """

        try:
            old_pos = self.view.mapToScene(self.view.viewport().rect().center())
            self.scale_factor *= zoom_factor

            if self.scale_factor < self.min_scale_factor:
                self.scale_factor = self.min_scale_factor
            elif self.scale_factor > self.max_scale_factor:
                self.scale_factor = self.max_scale_factor
                self.fit_to_widget()

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
            # self.view.centerOn(self.cursor().pos())

        except Exception as err:
            self.console.append_text("ERROR: zoom_image: {}".format(err.args))

    def fit_to_widget(self) -> None:
        """
        Fits the sprite sheet image to the widget size.
        """
        try:
            self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        except Exception as err:
            self.console.append_text("ERROR: fit_to_widget: {}".format(err.args))

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

    def handle_label_click(self, event, text_value:str):
        """
        Handle the click event on an image.

        Args:
            event (QMouseEvent): The mouse event.
            text_value (str): The text currently displaying the dimensions of the sprite sheet.
        """
        if event.button() == Qt.LeftButton:
            self.labelClicked.emit(text_value)
