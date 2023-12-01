import sys

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtCore import Qt, QTimer
import pygame
from pygame.locals import QUIT, KEYDOWN, K_w, K_a, K_s, K_d, K_SPACE

class Tank(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.speed = 5

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.rect, self.image)

    def boundingRect(self):
        return self.rect

    def move(self, direction):
        if direction == Qt.Key_W:
            self.rect.moveTop(self.rect.top() - self.speed)
        elif direction == Qt.Key_A:
            self.rect.moveLeft(self.rect.left() - self.speed)
        elif direction == Qt.Key_S:
            self.rect.moveBottom(self.rect.bottom() + self.speed)
        elif direction == Qt.Key_D:
            self.rect.moveRight(self.rect.right() + self.speed)

class Bullet(QGraphicsItem):
    def __init__(self, tank):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.speed = 10
        self.tank = tank

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.rect, self.image)

    def boundingRect(self):
        return self.rect

    def move(self):
        self.rect.moveTop(self.rect.top() - self.speed)

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing, True)
        self.view.setSceneRect(0, 0, 800, 800)
        self.setCentralWidget(self.view)

        self.tank = Tank()
        self.scene.addItem(self.tank)

        self.bullets = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # Update every 16 milliseconds (roughly 60 FPS)

        self.setWindowTitle("Tank Game")
        self.setGeometry(100, 100, 800, 800)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D):
            self.tank.move(event.key())
        elif event.key() == Qt.Key_Space:
            bullet = Bullet(self.tank)
            bullet.rect.moveCenter(self.tank.rect.center())
            self.scene.addItem(bullet)
            self.bullets.append(bullet)

    def update(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.top() < 0:
                self.scene.removeItem(bullet)
                self.bullets.remove(bullet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
