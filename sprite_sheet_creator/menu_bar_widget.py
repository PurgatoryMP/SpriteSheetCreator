from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenuBar, QAction

import style_sheet


class MenuBar(QMenuBar):
    """
    A custom menu bar widget for the application.

    Signals:
        importimagesequence: Signal emitted when "Import Image Sequence" action is triggered.
        importgiffile: Signal emitted when "Import Gif File" action is triggered.
        exportgiffile: Signal emitted when "Export Gif File" action is triggered.
        convertgiftosequence: Signal emitted when "Convert Gif to Sequence" action is triggered.
        importmp4file: Signal emitted when "Import MP4 File" action is triggered.
        exportmp4file: Signal emitted when "Export MP4 File" action is triggered.
        convertmp4tosequence: Signal emitted when "Convert MP4 to Sequence" action is triggered.
        exitapp: Signal emitted when "Exit" action is triggered.

    Args:
        main_console_widget: The main console widget.

    Attributes:
        console: The main console widget.
        import_image_sequence_action: QAction for "Import Image Sequence" action.
        import_gif_file_action: QAction for "Import Gif File" action.
        export_gif_file_action: QAction for "Export Gif File" action.
        convert_gif_to_sequence_action: QAction for "Convert Gif to Sequence" action.
        import_mp4_file_action: QAction for "Import MP4 File" action.
        export_mp4_file_action: QAction for "Export MP4 File" action.
        convert_mp4_to_sequence_action: QAction for "Convert MP4 to Sequence" action.
        exit_action: QAction for "Exit" action.
    """
    lsl_script_1 = pyqtSignal()
    lsl_script_2 = pyqtSignal()
    importimagesequence = pyqtSignal()
    exportimagesequence = pyqtSignal()
    exportspritesheet = pyqtSignal()
    importgiffile = pyqtSignal()
    exportgiffile = pyqtSignal()
    importmp4file = pyqtSignal()
    exportmp4file = pyqtSignal()
    exportwebmfile = pyqtSignal()
    exitapp = pyqtSignal()

    def __init__(self, main_console_widget):
        """
        Initialize the MenuBar widget.

        Args:
            main_console_widget: The main console widget.
        """
        super().__init__()

        # Add the console widget.
        self.console = main_console_widget
        self.console.append_text("INFO: Loading Menu Bar Widget.----------------")
        self.create_menu_bar()

    def create_menu_bar(self):
        """
        Create the menu bar with all the actions.

        Returns:
            menubar: The created QMenuBar.
        """
        menubar = QMenuBar()

        file_menu = menubar.addMenu("File")
        script_menu = menubar.addMenu("Scripts")

        # Create the file menu items.
        self.import_image_sequence_action = QAction("Import Image Sequence", menubar)
        self.export_image_sequence_action = QAction("Export Image Sequence", menubar)
        self.export_sprite_sheet_action = QAction("Export Sprite Sheet", menubar)
        self.import_gif_file_action = QAction("Import Gif File", menubar)
        self.export_gif_file_action = QAction("Export Gif File", menubar)
        self.export_webm_file_action = QAction("Export Webm File", menubar)
        self.import_mp4_file_action = QAction("Import MP4 File", menubar)
        self.export_mp4_file_action = QAction("Export MP4 File", menubar)
        # self.convert_mp4_to_sequence_action = QAction("Convert MP4 to Sequence", menubar)
        self.exit_action = QAction("Exit", menubar)

        self.lsl_script_1_action = QAction("Save Single Animated Texture lsl script", menubar)
        self.lsl_script_2_action = QAction("Save Sequenced Animated Texture lsl script", menubar)

        # Connect to a separate method
        self.import_image_sequence_action.triggered.connect(self.emit_import_image_sequence)
        self.export_image_sequence_action.triggered.connect(self.emit_export_image_sequence)
        self.export_sprite_sheet_action.triggered.connect(self.emit_export_sprite_sheet)
        self.import_gif_file_action.triggered.connect(self.emit_import_gif_file)
        self.export_gif_file_action.triggered.connect(self.emit_export_gif_file)
        self.export_webm_file_action.triggered.connect(self.emit_export_webm_file)
        self.import_mp4_file_action.triggered.connect(self.emit_import_mp4_file)
        self.export_mp4_file_action.triggered.connect(self.emit_export_mp4_file)
        self.exit_action.triggered.connect(self.emit_exit_application)

        self.lsl_script_1_action.triggered.connect(self.emit_lsl_script_1)
        self.lsl_script_2_action.triggered.connect(self.emit_lsl_script_2)

        # Add the actions to the menu
        file_menu.addAction(self.import_image_sequence_action)
        file_menu.addAction(self.export_image_sequence_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_sprite_sheet_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_gif_file_action)
        file_menu.addAction(self.export_gif_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.import_mp4_file_action)
        file_menu.addAction(self.export_mp4_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_webm_file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        script_menu.addAction(self.lsl_script_1_action)
        script_menu.addAction(self.lsl_script_2_action)

        file_menu.setStyleSheet(style_sheet.menu_bar_style())
        script_menu.setStyleSheet(style_sheet.menu_bar_style())

        self.console.append_text("INFO: Finished Loading Menu Bar Widget.")

        return menubar

    def emit_lsl_script_1(self):
        """
        Emit the importimagesequence signal.
        """
        self.lsl_script_1.emit()

    def emit_lsl_script_2(self):
        """
        Emit the exportimagesequence signal.
        """
        self.lsl_script_2.emit()

    def emit_import_image_sequence(self):
        """
        Emit the importimagesequence signal.
        """
        self.importimagesequence.emit()

    def emit_export_image_sequence(self):
        """
        Emit the exportimagesequence signal.
        """
        self.exportimagesequence.emit()

    def emit_export_sprite_sheet(self):
        """
        Emit the importimagesequence signal.
        """
        self.exportspritesheet.emit()

    def emit_import_gif_file(self):
        """
        Emit the importgiffile signal.
        """
        self.importgiffile.emit()

    def emit_import_mp4_file(self):
        """
        Emit the importmp4file signal.
        """
        self.importmp4file.emit()

    def emit_export_gif_file(self):
        """
        Emit the exportgiffile signal.
        """
        self.exportgiffile.emit()

    def emit_export_webm_file(self):
        """
        Emit the exportgiffile signal.
        """
        self.exportwebmfile.emit()

    def emit_export_mp4_file(self):
        """
        Emit the exportmp4file signal.
        """
        self.exportmp4file.emit()

    def emit_exit_application(self):
        """
        Emit the exitapp signal.
        """
        self.exitapp.emit()