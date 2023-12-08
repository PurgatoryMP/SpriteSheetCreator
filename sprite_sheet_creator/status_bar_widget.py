from PyQt5.QtWidgets import QLabel, QStatusBar, QProgressBar

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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setStyleSheet(style_sheet.progress_bar_style())
        self.addWidget(self.progress_bar)

    def progressbar_visibility(self, value: bool) -> None:
        """Toggles the visibility state of the progress bar.

        Args:
            value (bool): True or False
        """
        self.progress_bar.setVisible(value)

    def set_progress_maximum(self, value: int) -> None:
        """Sets the max value the progress bar can use.

        Args:
            value ():
        """
        self.progress_bar.setMaximum(value)

    def get_progress_value(self) -> int:
        """Gets the current value of the progress bar.

        Returns: (int): The value of the progress bar.
        """
        progress_value = self.progress_bar.value()
        return progress_value

    def update_progressbar(self, value: int) -> None:
        """Sets the value of the progress bar.

        Resets the progress bar if the value is greater than the maximum value.

        Args:
            value (int): The value representing the percentage of completion.
        """
        self.progress_bar.setValue(value)

        if value > self.progress_bar.maximum():
            self.progress_bar.reset()

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
