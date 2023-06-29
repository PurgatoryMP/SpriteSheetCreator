import os
import style_sheet

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QTransform
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QScrollArea


class SpriteSheetWidget(QWidget):
    def __init__(self, main_console_widget, control_widget):
        super().__init__()

        self.sprite_sheet = None
        self.images = None
        self.console = main_console_widget
        self.control = control_widget

        self.console.append_text("Loading: Sprite Sheet Widget.\n")

        self.image_sequence = []

        # Create the main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

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
        self.minimum_grid_size = 2

        # Enable mouse tracking to receive mouse wheel events
        self.view.setMouseTracking(True)

        self.console.append_text("Finished Loading: Sprite Sheet Widget.\n")

    def load_images(self, sequence: list):
        """Loads the provided image sequence.

        Args:
            sequence: str: a list of file paths to the individual images.
        """
        image_list = []
        self.image_sequence = sequence
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
            self.console.append_text(str(err.args))

    def update_sprite_sheet(self) -> None:
        try:
            image_list = []
            if self.image_sequence:
                for file_path in self.image_sequence:
                    image = QPixmap(file_path)
                    image_list.append(image)
                self.images = image_list

                if self.images:
                    self.sprite_sheet = self.create_sprite_sheet()

                    # Display the sprite sheet
                    self.display_sprite_sheet()
                    self.fit_to_widget()
        except Exception as err:
            self.console.append_text(str(err.args))

    def calculate_rows_columns(self):
        # total_images = len(self.images)

        rows = self.control.get_grid_rows_value()
        columns = self.control.get_grid_columns_value()
        if rows <= self.minimum_grid_size:
            rows = 2
        elif columns <= self.minimum_grid_size:
            columns = 2

        # rows = int(total_images ** 0.5)  # Square root rounded down for rows
        # columns = (total_images + rows - 1) // rows  # Ceiling division for columns
        return rows, columns

    def create_sprite_sheet(self):
        sprite_sheet_width = self.control.get_image_width_value()
        sprite_sheet_height = self.control.get_image_height_value()

        rows, columns = self.calculate_rows_columns()

        # Calculate the target width and height for each image
        target_width = sprite_sheet_width // columns
        target_height = sprite_sheet_height // rows

        sprite_sheet = QPixmap(sprite_sheet_width, sprite_sheet_height)
        sprite_sheet.fill(Qt.transparent)

        # Create a separate QPixmap for the outline layer
        outline_layer = QPixmap(sprite_sheet_width, sprite_sheet_height)
        outline_layer.fill(Qt.transparent)
        painter = QPainter(outline_layer)
        painter.setPen(Qt.black)  # Set the pen color to black for the outline

        sprite_painter = QPainter(sprite_sheet)
        x = 0
        y = 0

        for image in self.images:
            scaled_image = image.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)

            # Draw the outline on the outline layer
            painter.drawRect(x, y, target_width, target_height)

            # Draw the scaled image on the sprite sheet
            sprite_painter.drawPixmap(x, y, scaled_image)

            x += target_width

            if x >= sprite_sheet_width:
                x = 0
                y += target_height

        painter.end()
        sprite_painter.end()

        # Combine the sprite sheet and the outline layer
        sprite_sheet_with_outline = QPixmap(sprite_sheet_width, sprite_sheet_height)
        sprite_sheet_with_outline.fill(Qt.transparent)
        sprite_sheet_with_outline_painter = QPainter(sprite_sheet_with_outline)
        sprite_sheet_with_outline_painter.drawPixmap(0, 0, sprite_sheet)
        sprite_sheet_with_outline_painter.drawPixmap(0, 0, outline_layer)
        sprite_sheet_with_outline_painter.end()

        return sprite_sheet_with_outline

    def display_sprite_sheet(self):
        self.scene.clear()
        self.scene.addPixmap(self.sprite_sheet)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            # Only zoom when the Ctrl key is pressed
            scroll_delta = event.angleDelta().y()
            zoom_factor = 1.1 if scroll_delta > 0 else 0.9

            cursor_pos = event.pos()
            scroll_pos = self.view.mapToScene(cursor_pos)

            self.zoom_image(zoom_factor, scroll_pos)

    def zoom_image(self, zoom_factor, scroll_pos):
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

    def fit_to_widget(self):
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
