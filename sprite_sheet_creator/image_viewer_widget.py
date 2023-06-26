import style_sheet
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGraphicsView, QGraphicsScene


class ImageViewerWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()

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
        layout.addWidget(self.scroll_area)

        self.setMouseTracking(True)

        self.original_pixmap = None
        self.load_image(image_path)
        self.scale_factor = 1.0
        self.min_scale_factor = 0.2
        self.max_scale_factor = 3.0

    def load_image(self, image_path):
        self.original_pixmap = QPixmap(image_path)
        self.scene.clear()
        self.scene.addPixmap(self.original_pixmap)

        self.fit_to_widget()

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
