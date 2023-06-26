import glob
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageGridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        contentWidget = QWidget()
        gridLayout = QHBoxLayout(contentWidget)

        style = """
            QLabel {
                background-color: White;
                color: Black;
                font-size: 16px;
                border: 1px solid Black;
                border-radius: 8px;
                padding: 6px;
            }        
        """

        # Add images to the grid
        images = glob.glob(r'G:/Models/2023/Unicorn Dance/a_sequence/*.png')
        for image_file in images:

            pixmap = QPixmap(image_file)
            pixmap = pixmap.scaledToHeight(100, Qt.SmoothTransformation)

            label = QLabel()
            label.setPixmap(pixmap)
            label.setScaledContents(True)
            label.setStyleSheet(style)

            gridLayout.addWidget(label)

        self.scrollArea.setWidget(contentWidget)
        layout.addWidget(self.scrollArea)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Grid')
        self.setGeometry(100, 100, 800, 600)

        widget = ImageGridWidget()
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
