from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenuBar, QAction

import style_sheet

from importer import ImportExporter


class MenuBar(QMenuBar):
    import_image_sequence = pyqtSignal()

    def __init__(self, console_widget):
        super().__init__()
        self.image_sequence = []
        self.importer = ImportExporter(console_widget)
        self.console = console_widget
        self.console.append_text("Loading: Menu Bar Widget.")
        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = QMenuBar()

        file_menu = menubar.addMenu("File")

        new_action = QAction("Import Image Sequence", menubar)
        new_action.triggered.connect(self.emit_import_image_sequence)  # Connect to a separate method

        file_menu.addAction(new_action)

        file_menu.setStyleSheet(style_sheet.menu_bar_style())

        return menubar

    def emit_import_image_sequence(self):
        self.import_image_sequence.emit()
