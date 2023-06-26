from PyQt5.QtCore import QPoint

from PyQt5.QtGui import QPixmap, QPainter, QColor, QPolygon
from PyQt5.QtWidgets import QApplication, QLabel


def generate_arrow_image():
    # Create a QPixmap with a transparent background
    pixmap = QPixmap(16, 16)
    pixmap.fill(QColor(0, 0, 0, 0))  # Transparent color

    # Create a QPainter to draw on the QPixmap
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Define the arrow shape as a polygon
    arrow_polygon = QPolygon([
        QPoint(6, 4),
        QPoint(6, 12),
        QPoint(2, 8)
    ])

    # Set the pen and brush for drawing the arrow
    painter.setPen(QColor(0, 0, 0))  # Black pen color
    painter.setBrush(QColor(0, 0, 0))  # Black brush color

    # Draw the arrow polygon
    painter.drawPolygon(arrow_polygon)

    # Finish painting
    painter.end()

    return pixmap


# Example usage
if __name__ == "__main__":
    app = QApplication([])

    arrow_pixmap = generate_arrow_image()

    # Create a QLabel to display the arrow image
    label = QLabel()
    label.setPixmap(arrow_pixmap)

    # Show the QLabel
    label.show()

    app.exec_()
