import os
import sys

from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QPixmap, QDrag, QMouseEvent, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGridLayout, QWidget, QLabel, QFileDialog


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create the file menu
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        # Add actions to the file menu
        openAction = QAction('Open', self)
        openAction.triggered.connect(self.openDirectory)
        fileMenu.addAction(openAction)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Create the central widget with a horizontal grid layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.gridLayout = QGridLayout(centralWidget)

        self.setGeometry(100, 100, 800, 600)  # Set the window size
        self.setWindowTitle('Python PyQt5 Example')  # Set the window title

    def openDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Open Directory', '.')

        if directory:
            self.loadImages(directory)

    def loadImages(self, directory):
        files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        row = 0
        col = 0

        for file in files:
            filePath = os.path.join(directory, file)
            pixmap = QPixmap(filePath)

            label = DraggableLabel(self)
            label.setPixmap(pixmap)
            label.setAlignment(1)  # Align center

            self.gridLayout.addWidget(label, row, col)

            col += 1
            if col == 3:  # Adjust the number of columns as needed
                col = 0
                row += 1


class DraggableLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == 1:  # Left mouse button
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setImageData(self.pixmap().toImage())
            drag.setMimeData(mime_data)

            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasImage():
            image = QImage(mime_data.imageData())
            pixmap = QPixmap.fromImage(image)
            self.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
