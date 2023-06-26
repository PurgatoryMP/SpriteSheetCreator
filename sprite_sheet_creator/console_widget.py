import style_sheet
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class ConsoleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the QTextEdit widget for the console window
        self.console = QTextEdit()
        self.console.setStyleSheet(style_sheet.console_style())
        self.console.setReadOnly(True)  # Set the console window to read-only
        layout.addWidget(self.console)

        self.setLayout(layout)

    def append_text(self, text):
        print(text)
        # Append text to the console window
        self.console.append(text)
