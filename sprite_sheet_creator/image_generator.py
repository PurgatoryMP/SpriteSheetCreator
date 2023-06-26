import os
import tempfile

from PyQt5.QtCore import QPoint

from PyQt5.QtGui import QPixmap, QPainter, QColor, QPolygon, QImage


def create_checker_pattern(width: int, height: int, square_size: int) -> str:
    """
    Create a checker pattern image.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        square_size (int): The size of each square in pixels.

    Returns:
        str: The file path of the generated checker pattern image.
    """
    try:
        image = QImage(width, height, QImage.Format_RGBA8888)
        color1 = QColor(50, 50, 50, 255)  # Dark grey color
        color2 = QColor(50, 50, 50, 0)  # Transparent color

        for y in range(height):
            for x in range(width):
                if (x // square_size) % 2 == (y // square_size) % 2:
                    image.setPixelColor(x, y, color1)
                else:
                    image.setPixelColor(x, y, color2)

        # Save the image to a temporary file.
        temp_file_path = tempfile.mktemp(suffix='.png')
        image.save(temp_file_path)

        # convert the path.
        image_path = temp_file_path.replace("\\", "/")

        return image_path
    except Exception as err:
        self.debug(str(err.args))


def generate_arrow_image():
    try:
        temp_file_path = os.path.join(tempfile.gettempdir(), 'arrow_image.png')
        if os.path.exists(temp_file_path):
            return temp_file_path
        else:

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

            # Convert the QPixmap to QImage
            image = pixmap.toImage()

            # Save the QImage to a temporary file
            temp_file_path = os.path.join(tempfile.gettempdir(), 'arrow_image.png')

            image.save(temp_file_path)
            temp_file_path = temp_file_path.replace("\\", "/")

            return temp_file_path

    except Exception as err:
        print(err.args)
