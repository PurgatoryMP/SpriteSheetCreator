import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create dock widgets
        dock1 = QDockWidget("Dock 1", self)
        dock2 = QDockWidget("Dock 2", self)
        dock3 = QDockWidget("Dock 3", self)
        dock4 = QDockWidget("Dock 4", self)

        # Create central widget (e.g., a QTextEdit)
        # text_edit = QTextEdit()
        # self.setCentralWidget(text_edit)

        # Set dock areas
        self.addDockWidget(Qt.LeftDockWidgetArea, dock1)

        # Arrange dock2 and dock3 vertically
        self.splitDockWidget(dock1, dock2, Qt.Horizontal)
        self.splitDockWidget(dock1, dock2, Qt.Vertical)
        self.splitDockWidget(dock2, dock3, Qt.Vertical)
        self.splitDockWidget(dock2, dock3, Qt.Horizontal)

        # Arrange dock4 to the right
        self.addDockWidget(Qt.RightDockWidgetArea, dock4)

        # Set the main window properties
        self.setWindowTitle("Dockable Areas Example")
        self.setGeometry(100, 100, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
