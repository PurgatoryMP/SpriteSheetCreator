import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Console Output")
        self.setGeometry(100, 100, 800, 600)

        # Create the QTextEdit widget for console output
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)

        # Create a layout and add the console output widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.console_output)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Example: Print some text to the console output
        self.print_to_console("Hello, console!")

    def print_to_console(self, text):
        # Append text to the console output widget
        self.console_output.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())