import os
import sys

import psutil
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
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


# TODO: Make it so user can modify the order of the frames in the image sequence.
# TODO: Make it so the user can inject or append a frame or sequence into the existing sequence.

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

        # Set window title
        self.image_sequence = None
        self.setWindowTitle("Super Sprite")
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

        # self.generator = ImageGenerator()
        # self.generator.get

        self.table = FileTableWidget(self.main_console_widget)
        table_dock_widget = QDockWidget("Table")
        table_dock_widget.setWidget(self.table)
        table_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        table_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        # Display the application information in the console before anything else.
        self.main_console_widget.append_text("Super Sprite\nVersion: 1.0.0\n\n")

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

        # # Setup the menu bar
        self.menu_bar = MenuBar(self.main_console_widget)
        # Connect the menu bar signal using instance
        self.menu_bar.importimagesequence.connect(self.import_image_sequence)
        self.menu_bar.importgiffile.connect(self.import_gif)

        self.menu_bar.exportspritesheet.connect(self.export_sprite_sheet)

        # TODO: Plugin the functions for these menu options
        # self.menu_bar.importgiffile.connect(self.import_image_sequence)
        # self.menu_bar.exportgiffile.connect(self.import_image_sequence)
        # self.menu_bar.convertgiftosequence.connect(self.import_image_sequence)
        # self.menu_bar.importmp4file.connect(self.import_image_sequence)
        # self.menu_bar.exportmp4file.connect(self.import_image_sequence)
        # self.menu_bar.convertmp4tosequence.connect(self.import_image_sequence)

        self.menu_bar.exitapp.connect(self.exit_application)

        # Add the menu bar to the main window
        menu = self.menu_bar.create_menu_bar()
        self.setMenuBar(menu)

        # Connect the controls here
        self.control_widget.fpsValueChanged.connect(self.playback_widget.set_fps_value)

        self.control_widget.displayframeChanged.connect(self.playback_widget.set_frame_number)

        self.control_widget.startframeValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.endframeValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)

        self.control_widget.checkbox.stateChanged.connect(self.sprite_sheet_widget.toggle_grid_overlay)

        self.control_widget.gridrowValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.gridcolumnValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.imagewidthValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.imageheightValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)

        self.control_widget.playClicked.connect(self.playback_widget.start_playback)
        # self.control_widget.playClicked.connect(self.set_status_text("Playing Sequence"))
        self.control_widget.stopClicked.connect(self.playback_widget.stop_playback)
        # self.control_widget.stopClicked.connect(self.set_status_text("Playback Stopped"))
        self.image_sequence_widget.imageClicked.connect(self.handle_image_clicked)

        self.image_viewer_widget.imagepathClicked.connect(self.open_file_path)

        # add the widgets to the main window.
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_sequence_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, playback_widget_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_viewer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sprite_sheet_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, console_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, table_dock_widget)

        # Add a timer to control the playback.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_memory_usage)
        self.timer.start(1000)

        # Add a timer with a delay so the images are resized to fit the widget after you release the resize control.
        self.resize_timer = QTimer()
        self.resize_timer.setInterval(500)  # Set the delay in milliseconds
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.report_size)

        self.main_console_widget.append_text("INFO: Finished loading all widgets.\n")

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

    def handle_image_clicked(self, image_path) -> None:
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

    def handle_image_path_clicked(self, image_path) -> None:
        """
        Handles the click event for an image path.

        Args:
            self: The instance of the class.
            image_path (str): The path of the image to be opened.

        Returns:
            None

        Raises:
            None
        """
        if image_path:
            try:
                os.startfile(image_path)
            except Exception as err:
                self.main_console_widget.append_text("ERROR: {}".format(err.args))

    def import_image_sequence(self) -> None:
        """Imports an image sequence and populates the widgets.

        This method imports an image sequence using the ImportExporter class.
        The widgets in the application are then populated with the images
        contained in the selected directory.

        Returns:
            None

        Raises:
            <Specify any exceptions that can be raised>

        """
        # Implement the logic to import the image sequence here
        # Populate the widgets with the images contained in the selected directory

        self.image_sequence = self.import_export.import_image_sequence()
        self.populate_image_sequence(self.image_sequence)

    def import_gif(self) -> None:
        """
        Imports an image sequence after converting a selected gif.
        """
        self.image_sequence = self.import_export.import_as_gif()
        self.populate_image_sequence(self.image_sequence)

    def populate_image_sequence(self, image_sequence):

        try:
            if image_sequence:
                self.statusBar.set_total_frame_text(str(len(image_sequence)))

                self.main_console_widget.append_text("INFO: Image Sequence Loaded.")

                self.image_sequence_widget.load_sequence(image_sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Image Sequence Widget.")

                self.image_viewer_widget.load_image(image_sequence, 0)
                self.main_console_widget.append_text("INFO: Image set on Image Viewer Widget")

                self.playback_widget.load_image_sequence(image_sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Playback Widget.")

                self.sprite_sheet_widget.load_images(image_sequence)
                self.main_console_widget.append_text("INFO: Image sequence set on Sprite Sheet Widget.")
            else:
                self.main_console_widget.append_text("WARNING: populate_image_sequence: Nothing selected.")
        except Exception as err:
            self.main_console_widget.append_text("ERROR: populate_image_sequence: {}".format(err.args))

    def export_sprite_sheet(self):
        sprite_sheet = self.sprite_sheet_widget.get_generated_sprite_sheet()
        self.import_export.export_sprite_sheet(sprite_sheet)

    def get_memory_usage(self) -> None:
        """
        Retrieves the current memory usage of the process and displays it in a human-readable format.

        Returns:
            None

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
        # Get the new size of the main window
        # new_size = self.size()
        # print(f"New size: {new_size.width()} x {new_size.height()}")

        # After the window has been resized, fit the images to the new widget size.
        # TODO: Also make it so that the undocked widgets trigger this function when scaled.
        self.sprite_sheet_widget.fit_to_widget()
        self.image_viewer_widget.fit_to_widget()
        self.playback_widget.fit_to_widget()

    def exit_application(self):
        """
        Exit the application gracefully.

        This method is called when the application is exiting.

        """
        self.import_export.clean_up_temp_directory()
        self.close()


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    app.aboutToQuit.connect(window.exit_signal.exit_signal.emit)

    # Start the event loop
    sys.exit(app.exec_())
