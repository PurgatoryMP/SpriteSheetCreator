import os
import sys

import psutil
import pyperclip
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget

import style_sheet
from console_widget import ConsoleWidget
from controls_widget import ControlWidget
from higherarchy_widget import FileTableWidget
from image_grid_widget import ImageSequenceWidget
from image_viewer_widget import ImageViewerWidget
from importer import ImportExporter
from menu_bar_widget import MenuBar
from playback_widget import PlaybackWidget
from sprite_sheet_widget import SpriteSheetWidget
from status_bar_widget import StatusBar
from script_generator import ScriptGenerator
from converter import DirectConverter


# TODO: Make it so user can modify the order of the frames in the image sequence.
# TODO: Make it so the user can inject or append a frame or sequence into the existing sequence.
# TODO: Add a new layer option so users can create layered sequences.
# TODO: Add masking layer option so users can import masking images or sequences. (maybe out of scope for tool)?

# Custom class to define a signal
class ExitSignal(QObject):
    exit_signal = pyqtSignal()


class MainWindow(QMainWindow):
    """The main window of the application."""

    def __init__(self):
        """
        Create the main application window for Super Sprite.

        This class defines the main application window and sets up the various widgets and dock areas.

        Attributes:
            image_sequence (list): A list containing image file paths for the loaded image sequence.

        """
        super().__init__()

        # Create an instance of the custom signal class
        self.exit_signal = ExitSignal()

        # Connect the custom signal to your desired function
        self.exit_signal.exit_signal.connect(self.exit_application)

        # Set the application version number
        self.version_number = "v1.0.4"

        # Set window title
        self.image_sequence = []
        self.setWindowTitle("Super Sprite {}".format(self.version_number))
        self.resize(1200, 800)

        # Define main window and docked widget style sheets
        self.setStyleSheet(style_sheet.dock_widget_style())
        self.setStyleSheet(style_sheet.main_window_style())

        # Define dock options
        self.setDockOptions(QMainWindow.AllowTabbedDocks |
                            QMainWindow.AllowNestedDocks)

        # Set up the status bar
        self.statusBar = StatusBar()
        self.setStatusBar(self.statusBar)

        # Define the console first so we can print out messages to it while loading other widgets.
        self.main_console_widget = ConsoleWidget()
        console_dock_widget = QDockWidget("Console")
        console_dock_widget.setWidget(self.main_console_widget)
        console_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        console_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        # Display the application information in the console before anything else.
        self.main_console_widget.append_text("Super Sprite {}".format(self.version_number))
        self.main_console_widget.append_text("")

        self.table = FileTableWidget(self.main_console_widget)
        table_dock_widget = QDockWidget("Table")
        table_dock_widget.setWidget(self.table)
        table_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        table_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        # Define the controls, so we can add them to the other widgets
        self.control_widget = ControlWidget(self.main_console_widget)
        control_dock_widget = QDockWidget("Controls")
        control_dock_widget.setWidget(self.control_widget)
        control_dock_widget.setMinimumWidth(250)
        control_dock_widget.setMaximumWidth(300)
        control_dock_widget.setMaximumHeight(600)
        control_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        control_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.image_sequence_widget = ImageSequenceWidget(self.table, self.control_widget, self.main_console_widget)
        image_sequence_dock_widget = QDockWidget("Image Sequence")
        image_sequence_dock_widget.setWidget(self.image_sequence_widget)
        image_sequence_dock_widget.setMaximumHeight(300)
        image_sequence_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_sequence_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.image_viewer_widget = ImageViewerWidget(self.main_console_widget)
        image_viewer_dock_widget = QDockWidget("Image Viewer")
        image_viewer_dock_widget.setWidget(self.image_viewer_widget)
        image_viewer_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_viewer_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.sprite_sheet_widget = SpriteSheetWidget(self.main_console_widget, self.control_widget)
        sprite_sheet_dock_widget = QDockWidget("Sprite Sheet")
        sprite_sheet_dock_widget.setWidget(self.sprite_sheet_widget)
        sprite_sheet_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        sprite_sheet_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.playback_widget = PlaybackWidget(self.main_console_widget, self.control_widget, self.statusBar)
        playback_widget_dock_widget = QDockWidget("Playback")
        playback_widget_dock_widget.setWidget(self.playback_widget)
        playback_widget_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        playback_widget_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.import_export = ImportExporter(self.main_console_widget, self.control_widget)
        self.direct_converter = DirectConverter(self.main_console_widget)

        # Setup the menu bar
        self.menu_bar = MenuBar(self.main_console_widget)

        # Connect the menu bar signal using instance for file menu
        self.menu_bar.importimagesequence.connect(lambda: self.import_sequence("seq"))
        self.menu_bar.exportimagesequence.connect(lambda: self.export_sequence("seq"))
        self.menu_bar.exportspritesheet.connect(lambda: self.export_sequence("sprite"))
        self.menu_bar.importgiffile.connect(lambda: self.import_sequence("gif"))
        self.menu_bar.exportgiffile.connect(lambda: self.export_sequence("gif"))
        self.menu_bar.importmp4file.connect(lambda: self.import_sequence("mp4"))
        self.menu_bar.exportmp4file.connect(lambda: self.export_sequence("mp4"))
        self.menu_bar.exportwebmfile.connect(lambda: self.export_sequence("web"))
        self.menu_bar.exitapp.connect(self.exit_application)

        # Connect the menu bar signal using instance for scripts menu
        self.menu_bar.lsl_script_1.connect(lambda: self.provide_script("LSL"))
        self.menu_bar.lsl_script_2.connect(lambda: self.provide_script("LSL_Seq"))
        self.menu_bar.unity_script.connect(lambda: self.provide_script("Unity"))
        self.menu_bar.godot_script.connect(lambda: self.provide_script("Godot"))
        self.menu_bar.pygame_script.connect(lambda: self.provide_script("PyGame"))

        # Connect the menu bar signal for the converter menu
        self.menu_bar.image_convert.connect(lambda: self.convert_type("image"))
        self.menu_bar.seq_convert.connect(lambda: self.convert_type("seq"))
        self.menu_bar.gif_convert.connect(lambda: self.convert_type("gif"))
        self.menu_bar.mp4_convert.connect(lambda: self.convert_type("video"))
        self.menu_bar.webm_convert.connect(lambda: self.convert_type("web"))
        self.menu_bar.icon_convert.connect(lambda: self.convert_type("icon"))

        # Add the menu bar to the main window
        menu = self.menu_bar.create_menu_bar()
        self.setMenuBar(menu)

        # Connect the controls here
        self.control_widget.fpsValueChanged.connect(self.playback_widget.set_fps_value)
        self.control_widget.display_frame_Changed.connect(self.playback_widget.set_frame_number)
        self.control_widget.start_frame_Value_Changed.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.end_frame_Value_Changed.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.use_grid_checkbox.stateChanged.connect(self.sprite_sheet_widget.toggle_grid_overlay)
        self.control_widget.use_index_checkbox.stateChanged.connect(self.sprite_sheet_widget.toggle_index_overlay)
        self.control_widget.use_scale_checkbox.stateChanged.connect(self.sprite_sheet_widget.toggle_use_scale)
        self.control_widget.grid_row_Value_Changed.connect(self.update_playback_display)
        self.control_widget.grid_column_Value_Changed.connect(self.update_playback_display)
        self.control_widget.image_width_Value_Changed.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.image_height_Value_Changed.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.playClicked.connect(self.playback_widget.start_playback)
        self.control_widget.stopClicked.connect(self.playback_widget.stop_playback)
        self.image_sequence_widget.imageClicked.connect(self.handle_image_clicked)
        self.sprite_sheet_widget.labelClicked.connect(self.copy_to_clipboard)
        self.image_viewer_widget.imagepathClicked.connect(self.open_file_path)

        # add the widgets to the main window.
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_sequence_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, playback_widget_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_viewer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sprite_sheet_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, table_dock_widget)

        # Hide the table and console by default
        console_dock_widget.setVisible(False)
        table_dock_widget.setVisible(False)

        # Set which widgets we want to start out as floating free of the main window
        console_dock_widget.setFloating(True)
        table_dock_widget.setFloating(True)

        # Add a timer to control the playback.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_memory_usage)
        self.timer.start(1000)

        # Add a timer with a delay so the images are resized to fit the widget after you release the resize control.
        self.resize_timer = QTimer()
        self.resize_timer.setInterval(500)  # Set the delay in milliseconds
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.report_size)

        self.main_console_widget.append_text("INFO: All Widgets Loaded Successfully.")

    def open_file_path(self, file_path) -> None:
        """
        Open the file path in the default system application.

        Args:
            file_path (str): The path of the file to open.

        """
        if file_path:
            directory = os.path.dirname(file_path)
            if directory:
                os.startfile(directory)

    def update_playback_display(self) -> None:
        """
        updates the playback and sprite sheet controls.
        """
        try:
            self.sprite_sheet_widget.update_sprite_sheet()
            self.playback_widget.display_playtime()
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def copy_to_clipboard(self, text_value: str) -> None:
        """
        Copies the provided string to the clipboard.
        """
        pyperclip.copy(text_value)

    def handle_image_clicked(self, image_path: str) -> None:
        """
        Handle the image click event.

        Args:
            image_path (str): The path of the clicked image.

        """
        try:
            if image_path:
                self.image_viewer_widget.set_select_image(image_path)
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def handle_image_path_clicked(self, image_path: str) -> None:
        """
        Handles the click event for an image path.

        Args:
            self: The instance of the class.
            image_path (str): The path of the image to be opened.
        """
        if image_path:
            try:
                os.startfile(image_path)
            except Exception as err:
                self.main_console_widget.append_text("ERROR: {}".format(err.args))

    def import_sequence(self, file_type: str) -> None:
        """Imports an image sequence and populates the widgets.

        This method imports an image sequence using the ImportExporter class.
        The widgets in the application are then populated with the images.
        """
        self.image_sequence = []

        if file_type == "seq":
            self.image_sequence = self.import_export.import_image_sequence()
        elif file_type == "mp4":
            self.image_sequence = self.import_export.import_as_mp4()
        elif file_type == "gif":
            self.image_sequence = self.import_export.import_as_gif()
        # elif file_type == "web":
        # self.image_sequence = self.import_export.import_as_webm()

        # Populated list populate widgets.
        if self.image_sequence:
            self.populate_image_sequence(self.image_sequence)

    def export_sequence(self, file_type: str) -> None:
        """Exports the image sequence to a selected format."""
        if file_type == "seq":
            self.import_export.export_image_sequence(self.image_sequence)
        elif file_type == "mp4":
            self.import_export.export_as_mp4(self.image_sequence)
        elif file_type == "gif":
            self.import_export.export_as_gif(self.image_sequence)
        elif file_type == "web":
            self.import_export.export_as_webm(self.image_sequence)
        elif file_type == "sprite":
            sprite_sheet = self.sprite_sheet_widget.get_generated_sprite_sheet()
            self.import_export.export_sprite_sheet(sprite_sheet)

    def convert_type(self, file_type: str) -> None:
        """
        Converts files from one type to another.
        Args:
            file_type (str): The file type to handle.
        """
        if file_type == "image":
            self.direct_converter.convert_image()
        elif file_type == "seq":
            self.direct_converter.convert_sequence()
        elif file_type == "video":
            self.direct_converter.convert_video()
        elif file_type == "gif":
            self.direct_converter.convert_gif()
        elif file_type == "web":
            self.direct_converter.convert_web()
        elif file_type == "icon":
            self.direct_converter.convert_icon()

    def provide_script(self, script_type: str) -> None:
        """
        Provides the user with the selected script type.
        Args:
            script_type (str): The type of script to provide to the user.
        """
        scripts = ScriptGenerator()
        if script_type == "LSL":
            self.import_export.save_script(script_type, scripts.generate_lsl_script_option_1())
        elif script_type == "LSL_Seq":
            self.import_export.save_script(script_type, scripts.generate_lsl_script_option_2())
        elif script_type == "Unity":
            self.import_export.save_script(script_type, scripts.generate_Unity_script())
        elif script_type == "Godot":
            self.import_export.save_script(script_type, scripts.generate_godot_script())
        elif script_type == "PyGame":
            self.import_export.save_script(script_type, scripts.generate_pygame_script())

    def populate_image_sequence(self, sequence) -> None:
        """
        Populates all the widgets with the image sequence.

        Args:
            sequence: (list): The list containing the image sequence.
        """
        try:
            if sequence:
                self.statusBar.set_total_frame_text(str(len(sequence)))

                self.main_console_widget.append_text("INFO: Image Sequence Loaded.")

                self.image_sequence_widget.load_sequence(sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Image Sequence Widget.")

                self.image_viewer_widget.load_image(sequence, 0)
                self.main_console_widget.append_text("INFO: Image set on Image Viewer Widget")

                self.playback_widget.load_image_sequence(sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Playback Widget.")

                self.sprite_sheet_widget.load_images(sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Sprite Sheet Widget.")
            else:
                self.main_console_widget.append_text("WARNING: populate_image_sequence: Nothing selected.")
        except Exception as err:
            self.main_console_widget.append_text("ERROR: populate_image_sequence: {}".format(err.args))

    def get_memory_usage(self) -> None:
        """
        Retrieves the current memory usage of the process and displays it in a human-readable format.

        Raises:
            Exception: If an error occurs while retrieving or displaying the memory usage.
        """
        try:
            # Get the current process ID
            pid = psutil.Process()

            # Get the memory information
            memory_info = pid.memory_full_info()

            # Memory usage in bytes
            memory_usage = memory_info.uss

            # Convert to a human-readable format
            memory_usage_readable = psutil._common.bytes2human(memory_usage)

            # Display memory usage
            self.statusBar.set_mem_usage_text(str(memory_usage_readable))
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def resizeEvent(self, event) -> None:
        """
        Triggered when the main window is resized by the user.
        """
        # Call the base class resizeEvent method
        super().resizeEvent(event)
        # Start or restart the resize timer
        self.resize_timer.start()

    def report_size(self) -> None:
        """
        Report the current size of the main window.
        After the window has been resized, this function fits the images to the new widget size.
        """
        self.sprite_sheet_widget.fit_to_widget()
        self.image_viewer_widget.fit_to_widget()
        self.playback_widget.fit_to_widget()

    def exit_application(self) -> None:
        """
        Exit the application gracefully.
        This method is called when the application is exiting.
        """
        self.import_export.clean_up_temp_directory()
        self.close()


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("G:/sprite_sheet_creator/SpriteSheetCreator/sprite_sheet_creator/main_window_widget.ico"))

    # Create and show the main window
    window = MainWindow()
    window.show()

    app.aboutToQuit.connect(window.exit_signal.exit_signal.emit)

    # Start the event loop
    sys.exit(app.exec_())
