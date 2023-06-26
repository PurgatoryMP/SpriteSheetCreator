import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDockWidget, QVBoxLayout, QScrollArea, QWidget, \
    QPushButton, QSizePolicy, QGraphicsView, QGraphicsScene


class FirstWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the labels
        layout = QVBoxLayout()

        # Add labels to the layout
        for i in range(10):
            label = QLabel(f"Label {i + 1}")

            btn = QPushButton(f"Label {i + 1}")
            layout.addWidget(label)
            layout.addWidget(btn)

        # Create a scroll area and set the layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        # Set the scroll area as the main widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)


class SecondWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the labels
        layout = QVBoxLayout()

        # Add labels to the layout
        for i in range(10):
            label = QLabel(f"Label {i + 1}")

            btn = QPushButton(f"Label {i + 1}")
            layout.addWidget(label)
            layout.addWidget(btn)

        # Create a scroll area and set the layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        # Set the scroll area as the main widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)


class ThirdWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the labels
        layout = QVBoxLayout()

        # Add labels to the layout
        for i in range(10):
            label = QLabel(f"Label {i + 1}")

            btn = QPushButton(f"Label {i + 1}")
            layout.addWidget(label)
            layout.addWidget(btn)

        # Create a scroll area and set the layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        # Set the scroll area as the main widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)


class FourthWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.view = QGraphicsView()
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
        scroll_delta = event.angleDelta().y()
        zoom_factor = 1.1 if scroll_delta > 0 else 0.9

        cursor_pos = event.pos()
        scroll_pos = self.view.mapFrom(self, cursor_pos)

        self.zoom_image(zoom_factor, scroll_pos)

    def zoom_image(self, zoom_factor, scroll_pos):
        old_pos = self.view.horizontalScrollBar().value()

        self.scale_factor *= zoom_factor
        if self.scale_factor < self.min_scale_factor:
            self.scale_factor = self.min_scale_factor
        elif self.scale_factor > self.max_scale_factor:
            self.scale_factor = self.max_scale_factor

        self.view.setTransform(QTransform().scale(self.scale_factor, self.scale_factor))

        new_pos = self.view.horizontalScrollBar().value()

        scroll_adjustment = (scroll_pos.x() / self.view.width()) * (new_pos - old_pos)
        self.view.horizontalScrollBar().setValue(old_pos + scroll_adjustment)

    def fit_to_widget(self):
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("My Main Window")

        # Create a dockable widget for controls
        controls_widget = FirstWidget()
        controls_dock_widget = QDockWidget("One")
        controls_dock_widget.setWidget(controls_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, controls_dock_widget)

        Second_widget = SecondWidget()
        Second_dock_widget = QDockWidget("Two")
        Second_dock_widget.setWidget(Second_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, Second_dock_widget)

        Third_widget = ThirdWidget()
        Third_dock_widget = QDockWidget("Three")
        Third_dock_widget.setWidget(Third_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, Third_dock_widget)

        file_path = r"G:\Models\Refrences\baa5937331e47556b7a5d6ddab28f41d.jpg"
        Fourth_widget = FourthWidget(file_path)
        Fourth_dock_widget = QDockWidget("Four")
        Fourth_dock_widget.setWidget(Fourth_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, Fourth_dock_widget)


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
