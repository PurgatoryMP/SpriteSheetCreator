from PyQt5.QtWidgets import QLabel, QStatusBar
import style_sheet

class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel("One")
        label1.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(label1)

        label2 = QLabel("two")
        label2.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(label2)

        label3 = QLabel("three")
        label3.setStyleSheet(style_sheet.bubble_label_style())
        self.addWidget(label3)

