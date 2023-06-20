import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog


class ImageSequencePlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Sequence Player")
        self.image_label = QLabel(self)
        self.setCentralWidget(self.image_label)
        self.image_paths = []
        self.current_frame = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_next_frame)

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Image Sequence Directory")
        if directory:
            self.image_paths = sorted([os.path.join(directory, filename) for filename in os.listdir(directory)
                                       if filename.lower().endswith(".png")])
            if self.image_paths:
                self.current_frame = 0
                self.play_image_sequence()

    def play_image_sequence(self):
        if self.image_paths:
            image_path = self.image_paths[self.current_frame]
            image = QImage(image_path)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaledToWidth(self.width()))
            self.current_frame += 1
            if self.current_frame >= len(self.image_paths):
                self.current_frame = 0
            self.timer.start(1000 // 24)  # 24 frames per second

    def play_next_frame(self):
        self.play_image_sequence()


if __name__ == "__main__":
    app = QApplication([])
    player = ImageSequencePlayer()
    player.show()
    player.open_directory()
    app.exec()
