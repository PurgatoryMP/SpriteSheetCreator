from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenuBar, QAction

import style_sheet

from importer import ImportExporter


class MenuBar(QMenuBar):
    importimagesequence = pyqtSignal()
    importgiffile = pyqtSignal()
    exportgiffile = pyqtSignal()
    convertgiftosequence = pyqtSignal()
    importmp4file = pyqtSignal()
    exportmp4file = pyqtSignal()
    convertmp4tosequence = pyqtSignal()
    exitapp = pyqtSignal()

    def __init__(self, main_console_widget):
        super().__init__()

        # Add the console widget.
        self.console = main_console_widget
        self.console.append_text("Loading: Menu Bar Widget.")

        # self.image_sequence = []
        # self.importer = ImportExporter(main_console_widget)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = QMenuBar()

        file_menu = menubar.addMenu("File")

        # Create the file menu items.
        self.import_image_sequence_action = QAction("Import Image Sequence", menubar)
        self.import_gif_file_action = QAction("Import Gif File", menubar)
        self.export_gif_file_action = QAction("Export Gif File", menubar)
        self.convert_gif_to_sequence_action = QAction("Convert Gif to Sequence", menubar)
        self.import_mp4_file_action = QAction("Import MP4 File", menubar)
        self.export_mp4_file_action = QAction("Export MP4 File", menubar)
        self.convert_mp4_to_sequence_action = QAction("Convert MP4 to Sequence", menubar)
        self.exit_action = QAction("Exit", menubar)

        # Connect to a separate method
        self.import_image_sequence_action.triggered.connect(self.emit_import_image_sequence)
        self.import_gif_file_action.triggered.connect(self.emit_import_gif_file)
        self.export_gif_file_action.triggered.connect(self.emit_export_gif_file)
        self.convert_gif_to_sequence_action.triggered.connect(self.emit_convert_gif_to_sequence)
        self.import_mp4_file_action.triggered.connect(self.emit_import_mp4_file)
        self.export_mp4_file_action.triggered.connect(self.emit_export_mp4_file)
        self.convert_mp4_to_sequence_action.triggered.connect(self.emit_convert_mp4_to_sequence)
        self.exit_action.triggered.connect(self.emit_exit_application)

        # Add the actions to the menu
        file_menu.addAction(self.import_image_sequence_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_gif_file_action)
        file_menu.addAction(self.export_gif_file_action)
        file_menu.addAction(self.convert_gif_to_sequence_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_mp4_file_action)
        file_menu.addAction(self.export_mp4_file_action)
        file_menu.addAction(self.convert_mp4_to_sequence_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        file_menu.setStyleSheet(style_sheet.menu_bar_style())

        return menubar

    def emit_import_image_sequence(self):
        self.importimagesequence.emit()

    def emit_import_gif_file(self):
        self.importgiffile.emit()

    def emit_import_mp4_file(self):
        self.importmp4file.emit()

    def emit_export_gif_file(self):
        self.exportgiffile.emit()

    def emit_export_mp4_file(self):
        self.exportmp4file.emit()

    def emit_convert_gif_to_sequence(self):
        self.convertgiftosequence.emit()

    def emit_convert_mp4_to_sequence(self):
        self.convertmp4tosequence.emit()

    def emit_exit_application(self):
        self.exitapp.emit()