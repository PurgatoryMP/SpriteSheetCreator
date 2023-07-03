import os
import tempfile

from PyQt5.QtGui import QColor, QImage


class ImageGenerator():
    """A class that generates and manipulates images."""

    def __init__(self):
        """
        Initialize the ImageGenerator object.

        This constructor sets up the necessary directories and file paths for image generation.
        """
        # Define the temp file directory so its easy to clean up temp files when done.
        self.temp_directory = "{}\{}".format(tempfile.gettempdir(), "SuperSpriteTemp")
        if not os.path.exists(self.temp_directory):
            os.mkdir(self.temp_directory)

        self.checker_alpha_save_path = "{}\{}".format(self.temp_directory, "Checkered_Alpha.png")

    def get_checker_pattern(self) -> str:
        """
        Get the path to the checker pattern image.

        Returns:
            str: The file path to the checker pattern image.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            path = self.checker_alpha_save_path
            if not os.path.exists(path):
                self.create_checker_pattern(256, 256, 8)
                return path
            else:
                return path
        except Exception as err:
            print(str(err.args))

    def create_checker_pattern(self, width: int, height: int, square_size: int) -> None:
        """
        Create a checker pattern image.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            square_size (int): The size of each square in the checker pattern.

        Raises:
            Exception: If an error occurs during the process.
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
                image.save(self.checker_alpha_save_path)
        except Exception as err:
            print(str(err.args))
