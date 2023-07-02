from PyQt5.QtGui import QTextCursor, QColor, QTextOption
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QScrollArea

import style_sheet


class ConsoleWidget(QWidget):
    def __init__(self):
        """
        Initialize the ConsoleWidget.
        """
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """
        Initialize the user interface of the ConsoleWidget.
        """
        layout = QVBoxLayout()

        # Create a QScrollArea widget
        scroll_area = QScrollArea(self)
        scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        scroll_area.setWidgetResizable(True)  # Allow the widget to be resizable

        # Create the QTextEdit widget for the console window
        self.console = QTextEdit()
        self.console.setStyleSheet(style_sheet.console_style())
        self.console.setReadOnly(True)  # Set the console window to read-only

        # Disable word wrap in the QTextEdit widget
        self.console.setWordWrapMode(QTextOption.NoWrap)

        # Set the QTextEdit widget as the scroll area's widget
        scroll_area.setWidget(self.console)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def append_text(self, text):
        """
        Append text to the console window.

        Args:
            text (str): The text to be appended to the console window.

        Returns:
            None
        """
        # Append text to the console window
        self.console.append(text)
        self.console.moveCursor(QTextCursor.End)  # Move cursor to the end

        # Define color formats for specific words
        color_formats = {
            'ERROR': QColor('red'),
            'WARNING': QColor('orange'),
            'INFO': QColor('cyan'),
            'STDOUT': QColor('lightgreen'),
            'PYTHON': QColor('mediumpurple'),
            'SyntaxError': QColor('red'),
            'NameError': QColor('red'),
            'TypeError': QColor('red'),
            'IndexError': QColor('red'),
            'ValueError': QColor('red'),
            'KeyError': QColor('red'),
            'AttributeError': QColor('red'),
            'ImportError': QColor('red'),
            'FileNotFoundError': QColor('red'),
            'ZeroDivisionError': QColor('red'),
            'IOError': QColor('red'),
            'AssertionError': QColor('red'),
            'KeyboardInterrupt': QColor('red'),
            'MemoryError': QColor('red'),
            'OverflowError': QColor('red'),
            'RecursionError': QColor('red'),
            'NotImplementedError': QColor('red'),
            'IndentationError': QColor('red'),
            'DeprecationWarning': QColor('red'),
            'BaseException': QColor('red'),
            'Exception': QColor('red'),
            'ArithmeticError': QColor('red'),
            'StopIteration': QColor('red'),
            'OSError': QColor('red'),
            'RuntimeError': QColor('red'),
            'SystemExit': QColor('red'),
            'ValueWarning': QColor('orange'),
            'PermissionError': QColor('purple'),
            'SyntaxWarning': QColor('yellow'),
            'RuntimeWarning': QColor('pink'),
            'UserWarning': QColor('green'),
            'PendingDeprecationWarning': QColor('brown'),
        }

        for word, color in color_formats.items():
            format_start = self.console.document().find(word)
            while not format_start.isNull():
                format_end = QTextCursor(format_start)
                format_end.movePosition(QTextCursor.EndOfWord)
                format_text = format_start.charFormat()
                format_text.setForeground(color)
                format_start.mergeCharFormat(format_text)
                format_start = self.console.document().find(word, format_end)

        # Move the cursor to the end after formatting
        self.console.moveCursor(QTextCursor.End)

