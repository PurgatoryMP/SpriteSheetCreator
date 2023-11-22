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
    unity_script = pyqtSignal()
    godot_script = pyqtSignal()
    pygame_script = pyqtSignal()
    image_convert = pyqtSignal()
    seq_convert = pyqtSignal()
    gif_convert = pyqtSignal()
    mp4_convert = pyqtSignal()
    webm_convert = pyqtSignal()
    icon_convert = pyqtSignal()
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

        self.icon_convert_action = None
        self.image_convert_action = None
        self.webm_convert_action = None
        self.mp4_convert_action = None
        self.gif_convert_action = None
        self.seq_convert_action = None
        self.pygame_script_action = None
        self.godot_script_action = None
        self.unity_script_action = None
        self.lsl_script_2_action = None
        self.lsl_script_1_action = None
        self.exit_action = None
        self.export_mp4_file_action = None
        self.import_mp4_file_action = None
        self.export_webm_file_action = None
        self.export_gif_file_action = None
        self.import_gif_file_action = None
        self.export_sprite_sheet_action = None
        self.export_image_sequence_action = None
        self.import_image_sequence_action = None

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
        # Create the menu bar.
        menubar = QMenuBar()

        # Create the menu bar options.
        file_menu = menubar.addMenu("File")
        script_menu = menubar.addMenu("Scripts")
        convert_menu = menubar.addMenu("Converters")

        # Create the file menu items.
        self.import_image_sequence_action = QAction("Import Image Sequence", menubar)
        self.export_image_sequence_action = QAction("Export Image Sequence", menubar)
        self.export_sprite_sheet_action = QAction("Export Sprite Sheet", menubar)
        self.import_gif_file_action = QAction("Import Gif File", menubar)
        self.export_gif_file_action = QAction("Export Gif File", menubar)
        self.export_webm_file_action = QAction("Export Webm File", menubar)
        self.import_mp4_file_action = QAction("Import MP4 File", menubar)
        self.export_mp4_file_action = QAction("Export MP4 File", menubar)
        self.exit_action = QAction("Exit", menubar)

        # Create the script menu items.
        self.lsl_script_1_action = QAction("Save Single LSL Script", menubar)
        self.lsl_script_2_action = QAction("Save Seq. LSL Script", menubar)
        self.unity_script_action = QAction("Save Unity C# Script", menubar)
        self.godot_script_action = QAction("Save Godot GDScript", menubar)
        self.pygame_script_action = QAction("Save PyGame PyScript", menubar)

        # Create the script menu items.
        self.image_convert_action = QAction("Convert to Image Type", menubar)
        self.seq_convert_action = QAction("Convert to Image Sequence", menubar)
        self.gif_convert_action = QAction("Convert to Gif", menubar)
        self.mp4_convert_action = QAction("Convert to Video", menubar)
        self.webm_convert_action = QAction("Convert to Web", menubar)
        self.icon_convert_action = QAction("Convert to Icon", menubar)

        # Connect to a separate method.
        self.import_image_sequence_action.triggered.connect(self.emit_import_image_sequence)
        self.export_image_sequence_action.triggered.connect(self.emit_export_image_sequence)
        self.export_sprite_sheet_action.triggered.connect(self.emit_export_sprite_sheet)
        self.import_gif_file_action.triggered.connect(self.emit_import_gif_file)
        self.export_gif_file_action.triggered.connect(self.emit_export_gif_file)
        self.export_webm_file_action.triggered.connect(self.emit_export_webm_file)
        self.import_mp4_file_action.triggered.connect(self.emit_import_mp4_file)
        self.export_mp4_file_action.triggered.connect(self.emit_export_mp4_file)
        self.exit_action.triggered.connect(self.emit_exit_application)

        # connect the script options.
        self.lsl_script_1_action.triggered.connect(self.emit_lsl_script_1)
        self.lsl_script_2_action.triggered.connect(self.emit_lsl_script_2)
        self.unity_script_action.triggered.connect(self.emit_unity_script)
        self.godot_script_action.triggered.connect(self.emit_godot_script)
        self.pygame_script_action.triggered.connect(self.emit_pygame_script)

        # connect the convert options.
        self.image_convert_action.triggered.connect(self.emit_image_convert)
        self.seq_convert_action.triggered.connect(self.emit_seq_convert)
        self.gif_convert_action.triggered.connect(self.emit_gif_convert)
        self.mp4_convert_action.triggered.connect(self.emit_mp4_convert)
        self.webm_convert_action.triggered.connect(self.emit_webm_convert)
        self.icon_convert_action.triggered.connect(self.emit_icon_convert)

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

        # Add the script actions to the menu
        script_menu.addAction(self.lsl_script_1_action)
        script_menu.addAction(self.lsl_script_2_action)
        script_menu.addAction(self.unity_script_action)
        script_menu.addAction(self.godot_script_action)
        script_menu.addAction(self.pygame_script_action)

        # Add the convert actions to the menu
        convert_menu.addAction(self.image_convert_action)
        convert_menu.addAction(self.seq_convert_action)
        convert_menu.addAction(self.gif_convert_action)
        convert_menu.addAction(self.mp4_convert_action)
        convert_menu.addAction(self.webm_convert_action)
        convert_menu.addAction(self.icon_convert_action)

        # Apply the style settings to each of the menus
        file_menu.setStyleSheet(style_sheet.menu_bar_style())
        script_menu.setStyleSheet(style_sheet.menu_bar_style())
        convert_menu.setStyleSheet(style_sheet.menu_bar_style())

        self.console.append_text("INFO: Finished Loading Menu Bar Widget.")

        return menubar

    def emit_icon_convert(self) -> None:
        """
        Emit the icon_convert signal.
        """
        self.icon_convert.emit()

    def emit_image_convert(self) -> None:
        """
        Emit the image_convert signal.
        """
        self.image_convert.emit()

    def emit_webm_convert(self) -> None:
        """
        Emit the webm_convert signal.
        """
        self.webm_convert.emit()

    def emit_mp4_convert(self) -> None:
        """
        Emit the gif_convert signal.
        """
        self.mp4_convert.emit()

    def emit_gif_convert(self) -> None:
        """
        Emit the gif_convert signal.
        """
        self.gif_convert.emit()

    def emit_seq_convert(self) -> None:
        """
        Emit the seq_convert signal.
        """
        self.seq_convert.emit()

    def emit_pygame_script(self) -> None:
        """
        Emit the pygame_script signal.
        """
        self.pygame_script.emit()

    def emit_godot_script(self) -> None:
        """
        Emit the godot_script signal.
        """
        self.godot_script.emit()

    def emit_unity_script(self) -> None:
        """
        Emit the unity_script signal.
        """
        self.unity_script.emit()

    def emit_lsl_script_1(self) -> None:
        """
        Emit the lsl_script_1 signal.
        """
        self.lsl_script_1.emit()

    def emit_lsl_script_2(self) -> None:
        """
        Emit the lsl_script_2 signal.
        """
        self.lsl_script_2.emit()

    def emit_import_image_sequence(self) -> None:
        """
        Emit the importimagesequence signal.
        """
        self.importimagesequence.emit()

    def emit_export_image_sequence(self) -> None:
        """
        Emit the exportimagesequence signal.
        """
        self.exportimagesequence.emit()

    def emit_export_sprite_sheet(self) -> None:
        """
        Emit the importimagesequence signal.
        """
        self.exportspritesheet.emit()

    def emit_import_gif_file(self) -> None:
        """
        Emit the importgiffile signal.
        """
        self.importgiffile.emit()

    def emit_import_mp4_file(self) -> None:
        """
        Emit the importmp4file signal.
        """
        self.importmp4file.emit()

    def emit_export_gif_file(self) -> None:
        """
        Emit the exportgiffile signal.
        """
        self.exportgiffile.emit()

    def emit_export_webm_file(self) -> None:
        """
        Emit the exportgiffile signal.
        """
        self.exportwebmfile.emit()

    def emit_export_mp4_file(self) -> None:
        """
        Emit the exportmp4file signal.
        """
        self.exportmp4file.emit()

    def emit_exit_application(self) -> None:
        """
        Emit the exitapp signal.
        """
        self.exitapp.emit()
