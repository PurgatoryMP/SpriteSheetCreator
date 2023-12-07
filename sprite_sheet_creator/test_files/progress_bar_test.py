import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)

    def run(self):
        for i in range(1, 101):
            # Simulating the loading process
            time.sleep(0.1)
            self.update_progress.emit(i)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Progress Bar Demo')

        # Create QListWidget to display the loaded items
        self.list_widget = QListWidget(self)

        # Create QProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # Create QPushButton to start loading
        self.load_button = QPushButton('Load Items', self)
        self.load_button.clicked.connect(self.load_items)

        # Create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.load_button)

        self.worker_thread = WorkerThread()
        self.worker_thread.update_progress.connect(self.update_progress_bar)

        self.show()

    def load_items(self):
        # Clear the list widget before loading new items
        self.list_widget.clear()

        # Start the worker thread to load items
        self.worker_thread.start()

    def update_progress_bar(self, value):
        # Update the progress bar value
        self.progress_bar.setValue(value)

        # Add the loaded item to the list widget
        item_text = f'Item {value}'
        self.list_widget.addItem(item_text)

        # Scroll to the bottom of the list widget to show the latest item
        self.list_widget.scrollToBottom()

        # If loading is complete, reset the progress bar
        if value == 100:
            self.progress_bar.reset()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
