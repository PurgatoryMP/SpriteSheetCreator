import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

# Asset list
assets = {
    'background': "G:/Models/Refrences/FuyW-zdaYAAimQt.jpg",
    'button': "G:/Models/Refrences/CryptikittyLogotransparent.png",
    'button_up': "G:/Models/Refrences/CryptikittyLogotransparent.png",
    'button_pressed': "G:/Models/Refrences/CryptikittyLogo.png",
    # 'cursor': "G:/Models/Refrences/CryptikittyLogotransparent.png",
    # Add more image assets as needed
}


class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        background_path = assets['background']
        pixmap = QPixmap(background_path)

        label = QLabel(self)
        label.setPixmap(pixmap)

        self.resize(pixmap.width(), pixmap.height())

        self.draggable = False
        self.offset = None

        # Create the close button
        close_button = QPushButton(self)
        close_button.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); }}')
        close_button.setGeometry(self.width() - 30, 10, 30, 30)
        close_button.clicked.connect(self.close)

        # Create four small buttons
        button1 = QPushButton(self)
        button1.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); color: red;}}')
        button1.setGeometry(10, 10, 60, 30)
        button1.setText("Button 1")
        button1.pressed.connect(self.button_pressed)
        button1.released.connect(self.button_released)

        button2 = QPushButton(self)
        button2.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); }}')
        button2.setGeometry(80, 10, 60, 30)
        button2.pressed.connect(self.button_pressed)
        button2.released.connect(self.button_released)

        button3 = QPushButton(self)
        button3.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); }}')
        button3.setGeometry(150, 10, 60, 30)
        button3.pressed.connect(self.button_pressed)
        button3.released.connect(self.button_released)

        button4 = QPushButton(self)
        button4.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); }}')
        button4.setGeometry(220, 10, 60, 30)
        button4.pressed.connect(self.button_pressed)
        button4.released.connect(self.button_released)

        # Set custom cursor
        # cursor_image_path = assets['cursor']
        # cursor_pixmap = QPixmap(cursor_image_path)
        # cursor = QCursor(cursor_pixmap)
        # self.setCursor(cursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and event.buttons() == Qt.LeftButton:
            self.move(self.mapToParent(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            self.offset = None

    def button_pressed(self):
        print("pressed.")
        button = self.sender()
        button.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_pressed"]}); }}')

    def button_released(self):
        print("Released.")
        button = self.sender()
        button.setStyleSheet(f'QPushButton {{ border-image: url({assets["button_up"]}); }}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
