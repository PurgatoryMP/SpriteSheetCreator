import sys

from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QMovie, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QGraphicsOpacityEffect


class GifPopup(QDialog):
    def __init__(self, gif_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.draggable = False
        self.old_pos = QPoint()

        # Create a QLabel to display the GIF
        gif_label = QLabel(self)
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)

        # Set the size of the popup based on the GIF size
        size = QSize(movie.frameRect().size().width(), movie.frameRect().size().height())
        self.setFixedSize(size)

        # Set the central widget of the QDialog to the QLabel
        layout = QVBoxLayout(self)
        layout.addWidget(gif_label)

        # Start the GIF animation
        movie.start()

        # Make the background of the QLabel transparent
        opacity_effect = QGraphicsOpacityEffect(self)
        opacity_effect.setOpacity(0.5)  # Adjust the opacity as needed
        gif_label.setGraphicsEffect(opacity_effect)

        # Enable mouse tracking to detect mouse hover
        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(QColor(0, 0, 0, 0))  # Transparent background
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False

    def stop_animation(self):
        self.movie.stop()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Replace 'path_to_your_gif.gif' with the actual path to your GIF file
    gif_path = r'G:/Models/2023/Unicorn Dance/itsallcomingtogether.gif'

    popup = GifPopup(gif_path)
    popup.show()

    sys.exit(app.exec_())


























# r'G:/Models/2023/Unicorn Dance/itsallcomingtogether.gif'