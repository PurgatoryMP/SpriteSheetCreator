from PyQt5.QtWidgets import QLabel, QStatusBar

import style_sheet


class StatusBar(QStatusBar):
    """A custom status bar widget with memory usage, total frames, and status information."""

    def __init__(self):
        """Initialize the StatusBar object.

        Sets up the status bar with QLabel widgets for memory usage, total frames, and status.
        """
        super().__init__()

        self.setStyleSheet(style_sheet.status_bar_style())

        self.label1 = QLabel()
        self.label1.setText("Memory Usage: {}")
        self.label1.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label1)

        self.label2 = QLabel()
        self.label2.setText("Total Frames: {}")
        self.label2.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label2)

        self.label3 = QLabel()
        self.label3.setText("Status: {}")
        self.label3.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label3)

    def set_mem_usage_text(self, value: str) -> None:
        """Set the text for the memory usage label.

        Args:
            value (str): The value to be displayed as memory usage.

        """
        if value:
            self.label1.setText(r"Memory Usage: {}".format(value))

    def set_total_frame_text(self, value: str) -> None:
        """Set the text for the total frames label.

        Args:
            value (str): The value to be displayed as the total number of frames.

        """
        if value:
            self.label2.setText(r"Images Loaded: {}".format(value))

    def set_status_text(self, value: str) -> None:
        """Set the text for the status label.

        Args:
            value (str): The value to be displayed as the status.

        """
        if value:
            self.label3.setText(r"Status: {}".format(value))
