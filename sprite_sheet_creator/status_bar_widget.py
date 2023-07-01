from PyQt5.QtWidgets import QLabel, QStatusBar

import style_sheet


class StatusBar(QStatusBar):
    def __init__(self):
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
        if value:
            self.label1.setText("Memory Usage: {}".format(str(value)))

    def set_total_frame_text(self, value: str) -> None:
        if value:
            self.label2.setText("Images Loaded: {}".format(str(value)))

    def set_status_text(self, value: str) -> None:
        if value:
            self.label3.setText("Status: {}".format(str(value)))
