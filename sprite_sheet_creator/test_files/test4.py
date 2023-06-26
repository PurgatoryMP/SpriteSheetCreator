import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton("Open Second Window")
        self.button.clicked.connect(self.open_second_window)
        self.setCentralWidget(self.button)

        self.second_window = None

    def open_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow()
            self.second_window.show()
        else:
            self.second_window.show()

        self.print_to_console("Updated from Main Window")

    def print_to_console(self, text):
        if self.second_window is not None:
            self.second_window.console_output.append(text)


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Console Output")
        self.setGeometry(100, 100, 800, 600)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.console_output)
        self.setLayout(layout)

        self.print_to_console("Hello, console!")

    def print_to_console(self, text):
        self.console_output.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())