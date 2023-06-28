from PyQt5.QtWidgets import QLabel, QStatusBar
import style_sheet

class StatusBar(QStatusBar):
    def __init__(self, console_widget):
        super().__init__()

        self.console = console_widget
        self.console.append_text("Loading: Status Bar Widget.\n")

        self.label1 = QLabel("One")
        self.label1.setText("Memory Usage: {}")
        self.label1.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label1)

        self.label2 = QLabel("two")
        self.label2.setText("Total Frames: {}")
        self.label2.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label2)

        self.label3 = QLabel("three")
        self.label3.setText("State: {}")
        self.label3.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(self.label3)

        self.console.append_text("Finished Loading: Status Bar Widget.\n")

    def set_mem_usage_text(self, value: str) -> None:
        self.label1.setText("Memory Usage: {}".format(str(value)))

    def set_total_frame_text(self, value: str) -> None:
        self.label2.setText(str(value))

    def set_state_text(self, value: str) -> None:
        self.label3.setText(str(value))
